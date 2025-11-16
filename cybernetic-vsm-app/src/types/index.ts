// VSM Agent Types
export type AgentType = 'policy' | 'intelligence' | 'control' | 'coordination';

export interface AgentMessage {
  id: string;
  agentType: AgentType;
  timestamp: string;
  content: string;
  metadata?: Record<string, any>;
}

export interface VSMExecutionPlan {
  taskDescription: string;
  strategicPlan: string;
  qualityThreshold: number;
  estimatedDuration: string;
  subtasks: Subtask[];
}

export interface Subtask {
  id: string;
  name: string;
  description: string;
  dependencies: string[];
  priority: 'critical' | 'high' | 'medium' | 'low';
  estimatedEffort: string;
  successCriteria: string;
}

export interface ExecutionStatus {
  status: 'idle' | 'planning' | 'executing' | 'completed' | 'error';
  currentAgent?: AgentType;
  currentPhase?: string;
  progress: number;
  messages: AgentMessage[];
  result?: string;
  error?: string;
}

export interface QualityGate {
  name: string;
  criteria: string;
  threshold: number;
  actualScore?: number;
  status: 'pending' | 'passed' | 'failed';
  timestamp?: string;
}

// Settings Types
export interface Settings {
  apiKey: string;
  model: string;
}

export const DEFAULT_MODEL = 'x-ai/grok-beta';

// OpenRouter Types
export interface OpenRouterMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface OpenRouterRequest {
  model: string;
  messages: OpenRouterMessage[];
  temperature?: number;
  max_tokens?: number;
}

export interface OpenRouterResponse {
  id: string;
  choices: Array<{
    message: {
      role: string;
      content: string;
    };
    finish_reason: string;
  }>;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}
