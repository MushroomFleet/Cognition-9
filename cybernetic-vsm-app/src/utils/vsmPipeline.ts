import type {
  AgentMessage,
  AgentType,
  OpenRouterMessage,
} from '../types';
import { OpenRouterAPI } from './openrouter';

// Agent System Prompts based on the VSM hierarchy
const AGENT_PROMPTS = {
  policy: `You are the Policy Agent (System 5) responsible for governance and ethical boundaries.

Core Responsibilities:
1. Policy Definition: Establish permissible vs prohibited actions
2. Ethical Boundaries: Define ethical constraints
3. Strategic Objectives: Set high-level organizational goals
4. Compliance Monitoring: Ensure operations within policy
5. Algedonic Alerts: Respond to critical system deviations

When invoked, review the task for ethical compliance, policy alignment, and strategic fit. Provide governance guidance.`,

  intelligence: `You are the Intelligence Agent (System 4) responsible for strategic planning and intelligence.

Core Responsibilities:
1. Environmental Scanning: Analyze context and constraints
2. Task Decomposition: Break complex tasks into subtasks
3. Strategy Selection: Choose optimal execution approach
4. Resource Planning: Estimate required resources
5. Adaptation: Adjust plans based on conditions

When given a task, create a detailed strategic execution plan with:
- Context analysis
- Task decomposition into subtasks
- Resource requirements
- Quality gates
- Success metrics

Return your response as a structured plan in markdown format.`,

  control: `You are the Control Agent (System 3) responsible for execution management and quality enforcement.

Core Responsibilities:
1. Execution Management: Coordinate activities per strategic plan
2. Quality Enforcement: Apply quality gates and thresholds
3. Performance Monitoring: Track progress and resource usage
4. Issue Resolution: Handle errors and deviations
5. Reporting: Provide status updates

When given a strategic plan, simulate execution and provide:
- Execution timeline
- Quality gate results
- Performance metrics
- Final status and recommendations`,

  coordination: `You are the Coordination Agent (System 2) responsible for conflict prevention and resource management.

Core Responsibilities:
1. Conflict Detection: Identify potential collisions
2. Resource Allocation: Manage shared resources
3. Deduplication: Prevent redundant work
4. Synchronization: Coordinate timing of tasks
5. Communication Facilitation: Enable information sharing

When monitoring execution, provide:
- Active worker status
- Resource allocation
- Conflict detection and resolution
- Synchronization points`,
};

export class VSMPipeline {
  private api: OpenRouterAPI;
  private messages: AgentMessage[] = [];

  constructor(apiKey: string, model: string) {
    this.api = new OpenRouterAPI(apiKey, model);
  }

  private addMessage(agentType: AgentType, content: string, metadata?: Record<string, any>): AgentMessage {
    const message: AgentMessage = {
      id: `${agentType}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      agentType,
      timestamp: new Date().toISOString(),
      content,
      metadata,
    };
    this.messages.push(message);
    return message;
  }

  private async callAgent(
    agentType: AgentType,
    userPrompt: string,
    context?: string
  ): Promise<string> {
    const systemPrompt = AGENT_PROMPTS[agentType];
    const messages: OpenRouterMessage[] = [
      { role: 'system', content: systemPrompt },
    ];

    if (context) {
      messages.push({ role: 'user', content: `Context:\n${context}` });
    }

    messages.push({ role: 'user', content: userPrompt });

    const response = await this.api.sendMessage(messages, {
      temperature: 0.7,
      max_tokens: 2000,
    });

    this.addMessage(agentType, response);
    return response;
  }

  async executeTask(
    taskDescription: string,
    onProgress?: (agent: AgentType, phase: string, progress: number) => void
  ): Promise<{ messages: AgentMessage[]; result: string }> {
    this.messages = [];

    try {
      // Step 1: Intelligence Agent - Strategic Planning
      onProgress?.('intelligence', 'Creating strategic plan...', 10);
      const strategicPlan = await this.callAgent(
        'intelligence',
        `Analyze this task and create a detailed strategic execution plan:\n\n${taskDescription}\n\nProvide a comprehensive plan including context analysis, task decomposition, resource planning, and success metrics.`
      );

      // Step 2: Policy Agent - Governance Check
      onProgress?.('policy', 'Checking policy compliance...', 30);
      const policyCheck = await this.callAgent(
        'policy',
        `Review this task and strategic plan for policy compliance and ethical considerations:\n\nTask: ${taskDescription}\n\nStrategic Plan:\n${strategicPlan}\n\nProvide governance guidance and approval status.`,
        strategicPlan
      );

      // Check if policy approved
      if (policyCheck.toLowerCase().includes('not approved') ||
          policyCheck.toLowerCase().includes('rejected') ||
          policyCheck.toLowerCase().includes('violation')) {
        throw new Error(`Policy check failed: ${policyCheck}`);
      }

      // Step 3: Coordination Agent - Resource Planning
      onProgress?.('coordination', 'Planning resource allocation...', 50);
      const coordinationPlan = await this.callAgent(
        'coordination',
        `Based on this strategic plan, identify potential conflicts, resource requirements, and coordination needs:\n\n${strategicPlan}\n\nProvide a coordination strategy.`,
        strategicPlan
      );

      // Step 4: Control Agent - Execution Simulation
      onProgress?.('control', 'Simulating execution...', 70);
      const executionReport = await this.callAgent(
        'control',
        `Execute this strategic plan (simulated) and provide a detailed execution report:\n\n${strategicPlan}\n\nCoordination Plan:\n${coordinationPlan}\n\nProvide execution timeline, quality gates, and final results.`,
        `${strategicPlan}\n\nCoordination: ${coordinationPlan}`
      );

      // Step 5: Final Quality Check
      onProgress?.('policy', 'Final quality validation...', 90);
      await this.callAgent(
        'policy',
        `Perform final quality validation on this execution:\n\nOriginal Task: ${taskDescription}\n\nExecution Report:\n${executionReport}\n\nProvide final approval and any recommendations.`,
        executionReport
      );

      onProgress?.('control', 'Complete', 100);

      return {
        messages: this.messages,
        result: executionReport,
      };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      this.addMessage('policy', `ALGEDONIC ALERT: ${errorMessage}`, { error: true });
      throw error;
    }
  }

  getMessages(): AgentMessage[] {
    return [...this.messages];
  }

  updateCredentials(apiKey: string, model: string): void {
    this.api.updateCredentials(apiKey, model);
  }
}
