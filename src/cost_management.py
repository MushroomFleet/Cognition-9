"""
Cost management and token budgeting
Tracks and limits token usage across executions
"""

import json
from typing import Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timedelta

@dataclass
class TokenBudget:
    """Token budget for a user or project"""
    budget_id: str
    total_budget: int  # Total tokens allocated
    used_tokens: int  # Tokens used so far
    period_start: float
    period_end: float
    
    def remaining(self) -> int:
        """Get remaining tokens"""
        return max(0, self.total_budget - self.used_tokens)
    
    def utilization(self) -> float:
        """Get budget utilization percentage"""
        if self.total_budget == 0:
            return 0.0
        return (self.used_tokens / self.total_budget) * 100.0
    
    def is_exceeded(self) -> bool:
        """Check if budget exceeded"""
        return self.used_tokens >= self.total_budget

class CostManager:
    """
    Manages token budgets and cost tracking
    """
    
    # Pricing per 1M tokens (example rates)
    MODEL_COSTS = {
        "opus": {"input": 15.0, "output": 75.0},
        "sonnet": {"input": 3.0, "output": 15.0},
        "haiku": {"input": 0.25, "output": 1.25}
    }
    
    def __init__(self, storage_path: str = "data/budgets"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.budgets: Dict[str, TokenBudget] = {}
        self._load_budgets()
    
    def create_budget(
        self,
        budget_id: str,
        total_tokens: int,
        period_days: int = 30
    ) -> TokenBudget:
        """Create new token budget"""
        now = datetime.utcnow().timestamp()
        
        budget = TokenBudget(
            budget_id=budget_id,
            total_budget=total_tokens,
            used_tokens=0,
            period_start=now,
            period_end=now + (period_days * 86400)
        )
        
        self.budgets[budget_id] = budget
        self._save_budget(budget)
        
        return budget
    
    def check_budget(
        self,
        budget_id: str,
        requested_tokens: int
    ) -> tuple[bool, str]:
        """
        Check if budget allows requested tokens
        
        Returns:
            (allowed, message)
        """
        budget = self.budgets.get(budget_id)
        if not budget:
            return False, f"Budget not found: {budget_id}"
        
        # Check if period expired
        now = datetime.utcnow().timestamp()
        if now > budget.period_end:
            return False, "Budget period expired"
        
        # Check if sufficient tokens
        if budget.used_tokens + requested_tokens > budget.total_budget:
            remaining = budget.remaining()
            return False, f"Insufficient tokens (have: {remaining}, need: {requested_tokens})"
        
        return True, "OK"
    
    def consume_tokens(
        self,
        budget_id: str,
        tokens_used: int,
        model: str = "sonnet"
    ) -> Dict:
        """
        Record token usage
        
        Returns:
            Usage details including cost
        """
        budget = self.budgets.get(budget_id)
        if not budget:
            raise ValueError(f"Budget not found: {budget_id}")
        
        budget.used_tokens += tokens_used
        self._save_budget(budget)
        
        # Calculate cost
        cost = self._calculate_cost(tokens_used, model)
        
        return {
            "tokens_used": tokens_used,
            "budget_remaining": budget.remaining(),
            "budget_utilization": budget.utilization(),
            "estimated_cost_usd": cost
        }
    
    def get_budget_status(self, budget_id: str) -> Dict:
        """Get current budget status"""
        budget = self.budgets.get(budget_id)
        if not budget:
            return {"error": "Budget not found"}
        
        now = datetime.utcnow().timestamp()
        days_remaining = (budget.period_end - now) / 86400.0
        
        return {
            "budget_id": budget_id,
            "total_budget": budget.total_budget,
            "used_tokens": budget.used_tokens,
            "remaining_tokens": budget.remaining(),
            "utilization_percent": round(budget.utilization(), 2),
            "days_remaining": round(days_remaining, 1),
            "status": "exceeded" if budget.is_exceeded() else "active"
        }
    
    def _calculate_cost(self, tokens: int, model: str) -> float:
        """Calculate cost in USD"""
        if model not in self.MODEL_COSTS:
            model = "sonnet"  # Default
        
        # Simplified: assume 50/50 input/output split
        input_tokens = tokens // 2
        output_tokens = tokens - input_tokens
        
        rates = self.MODEL_COSTS[model]
        cost = (
            (input_tokens / 1_000_000) * rates["input"] +
            (output_tokens / 1_000_000) * rates["output"]
        )
        
        return round(cost, 4)
    
    def _save_budget(self, budget: TokenBudget):
        """Persist budget"""
        filepath = self.storage_path / f"{budget.budget_id}.json"
        with open(filepath, 'w') as f:
            json.dump(asdict(budget), f, indent=2)
    
    def _load_budgets(self):
        """Load existing budgets"""
        if not self.storage_path.exists():
            return
        
        for filepath in self.storage_path.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    budget = TokenBudget(**data)
                    self.budgets[budget.budget_id] = budget
            except Exception as e:
                print(f"Error loading budget from {filepath}: {e}")


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("COST MANAGEMENT DEMO")
    print("=" * 60)
    
    cost_mgr = CostManager()
    
    # Create budget
    print("\n--- Creating Budget ---")
    budget = cost_mgr.create_budget(
        budget_id="project_alpha",
        total_tokens=1_000_000,
        period_days=30
    )
    print(f"Created budget: {budget.budget_id}")
    print(f"Total tokens: {budget.total_budget:,}")
    
    # Check budget
    print("\n--- Checking Budget ---")
    allowed, msg = cost_mgr.check_budget("project_alpha", 50_000)
    print(f"Request 50k tokens: {msg}")
    
    # Consume tokens
    print("\n--- Consuming Tokens ---")
    usage = cost_mgr.consume_tokens("project_alpha", 50_000, model="opus")
    print(f"Tokens used: {usage['tokens_used']:,}")
    print(f"Estimated cost: ${usage['estimated_cost_usd']}")
    print(f"Remaining: {usage['budget_remaining']:,}")
    print(f"Utilization: {usage['budget_utilization']:.1f}%")
    
    # Get status
    print("\n--- Budget Status ---")
    status = cost_mgr.get_budget_status("project_alpha")
    print(json.dumps(status, indent=2))
