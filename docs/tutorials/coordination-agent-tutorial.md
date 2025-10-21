# Coordination Agent - Tutorial Guide

**Agent Type**: VSM System 2 - Conflict Prevention  
**System Level**: System 2  
**Model**: Claude Sonnet  
**Color**: Teal  

---

## Overview

The **Coordination Agent** (System 2) prevents conflicts between parallel workers by managing shared resources, detecting potential collisions, preventing duplicate work, and facilitating smooth synchronization.

### What It Does

- Monitors all active worker activities in real-time
- Detects potential resource conflicts before they occur
- Manages access to shared resources (files, APIs, tools)
- Prevents duplicate work across agents
- Coordinates timing of interdependent tasks
- Maintains shared coordination board

### When to Use

✅ **Use coordination agent when**:
- Multiple agents working in parallel
- Shared resources need management
- Risk of duplicate work
- Complex dependencies requiring synchronization
- Need conflict prevention not just resolution

❌ **Don't use for**:
- Single-agent tasks
- Purely sequential workflows (no conflicts possible)
- Simple tasks without resource contention

---

## Usage Example

**Your Request**:
```
"Coordinate these parallel agents to prevent conflicts while researching and writing"
```

**What Coordination Agent Does**:

1. **Activity Monitoring**:
   ```
   Active Workers:
   - researcher: Writing to artifacts/research.md (ACTIVE)
   - writer: Waiting for artifacts/research.md (BLOCKED)
   - critic: Idle (WAITING)
   ```

2. **Resource Management**:
   ```
   File: artifacts/research.md
   - Status: LOCKED (write)
   - Held by: researcher
   - Queue: writer (read access pending)
   ```

3. **Conflict Detection**:
   ```
   Potential Conflict: Writer attempting to read file still being written
   Resolution: Block writer until researcher completes
   Notification: "Writer, research.md not ready. ETA: 15 minutes"
   ```

4. **Synchronization**:
   ```
   Sync Point: Writer needs research output
   - Provider: researcher
   - Expected ready: 11:30
   - Status: WAITING
   
   At 11:30:
   - Signal sent: "Writer, dependency satisfied. Proceed."
   ```

**Result**: Smooth coordination without conflicts or race conditions

---

## Coordination Board

The agent maintains a shared state board:

```markdown
# Coordination Board
Updated: 2024-01-15T12:00:00Z

## Active Workers
- researcher: ACTIVE (writing artifacts/research.md)
- writer: BLOCKED (waiting for research.md)
- critic: IDLE

## Resource Registry
- artifacts/research.md: LOCKED by researcher
- artifacts/guide.md: AVAILABLE

## Task Registry
Completed: 0
Pending: 3 (1 in-progress, 2 waiting)

## Conflicts: None
## Synchronization Points: 2
```

---

## Conflict Resolution Strategies

### 1. Defer
**Minor conflicts**: Delay one agent until resolved

### 2. Redirect
**Duplicate work**: Point to existing artifact

### 3. Serialize
**Shared resource**: Queue access requests

### 4. Synchronize
**Dependencies**: Block until prerequisites met

### 5. Abort
**Critical conflict**: Halt and escalate to System 3

---

## Tips & Best Practices

### 1. Let Coordination Happen Automatically

Coordination agent monitors continuously - no manual intervention needed

### 2. Check Coordination Board

For debugging: Review coordination board in logs to see what's happening

### 3. Design for Minimal Conflicts

Best practice: Structure tasks to minimize resource sharing

### 4. Trust Synchronization

Agent ensures proper execution order for dependent tasks

---

## Working in VSM Hierarchy

```
System 3 (Control)
    ↓ Delegates tasks
System 2 (Coordination) ← You are here
    ↓ Prevents conflicts
System 1 (Workers)
    ↓ Execute tasks
```

Coordination agent sits between control (which delegates) and workers (who execute), ensuring smooth cooperation.

---

## Summary

The **Coordination Agent** prevents conflicts, manages resources, and ensures smooth cooperation between parallel workers.

**Perfect for**: Parallel workflows, resource management, conflict prevention, and maintaining system stability during concurrent execution.

---

**Typical Usage**:
Coordination happens automatically - the agent monitors and intervenes only when conflicts detected.
