import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faGavel,
  faBrain,
  faClipboardCheck,
  faHandshake,
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import type { AgentMessage as AgentMessageType, AgentType } from '../types';

interface AgentMessageProps {
  message: AgentMessageType;
}

const AGENT_CONFIG: Record<
  AgentType,
  {
    name: string;
    icon: any;
    color: string;
    bgColor: string;
    description: string;
  }
> = {
  policy: {
    name: 'Policy Agent',
    icon: faGavel,
    color: 'text-accent',
    bgColor: 'bg-accent/10',
    description: 'System 5 - Governance & Ethics',
  },
  intelligence: {
    name: 'Intelligence Agent',
    icon: faBrain,
    color: 'text-primary',
    bgColor: 'bg-primary/10',
    description: 'System 4 - Strategic Planning',
  },
  control: {
    name: 'Control Agent',
    icon: faClipboardCheck,
    color: 'text-blue-400',
    bgColor: 'bg-blue-400/10',
    description: 'System 3 - Execution Management',
  },
  coordination: {
    name: 'Coordination Agent',
    icon: faHandshake,
    color: 'text-teal-400',
    bgColor: 'bg-teal-400/10',
    description: 'System 2 - Conflict Prevention',
  },
};

export const AgentMessage: React.FC<AgentMessageProps> = ({ message }) => {
  const config = AGENT_CONFIG[message.agentType];
  const isError = message.metadata?.error;

  return (
    <div
      className={`rounded-lg p-4 ${config.bgColor} border border-border transition-smooth
                  hover:shadow-elegant animate-slide-up`}
    >
      {/* Agent Header */}
      <div className="flex items-center gap-3 mb-3">
        <div className={`${config.color}`}>
          <FontAwesomeIcon icon={config.icon} className="text-xl" />
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-sm">{config.name}</h3>
            {isError && (
              <FontAwesomeIcon
                icon={faExclamationTriangle}
                className="text-destructive text-sm"
              />
            )}
          </div>
          <p className="text-xs text-muted-foreground">{config.description}</p>
        </div>
        <div className="text-xs text-muted-foreground">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>

      {/* Message Content */}
      <div
        className={`prose prose-invert prose-sm max-w-none ${
          isError ? 'text-destructive' : 'text-foreground'
        }`}
      >
        <div className="whitespace-pre-wrap break-words">{message.content}</div>
      </div>
    </div>
  );
};
