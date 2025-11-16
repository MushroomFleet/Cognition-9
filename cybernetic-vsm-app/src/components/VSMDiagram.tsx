import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faGavel,
  faBrain,
  faClipboardCheck,
  faHandshake,
  faArrowDown,
} from '@fortawesome/free-solid-svg-icons';
import type { AgentType } from '../types';

interface VSMDiagramProps {
  currentAgent?: AgentType;
  currentPhase?: string;
}

export const VSMDiagram: React.FC<VSMDiagramProps> = ({ currentAgent, currentPhase }) => {
  const agents: Array<{
    type: AgentType;
    name: string;
    system: string;
    icon: any;
    color: string;
  }> = [
    {
      type: 'policy',
      name: 'Policy Agent',
      system: 'System 5',
      icon: faGavel,
      color: 'bg-accent',
    },
    {
      type: 'intelligence',
      name: 'Intelligence Agent',
      system: 'System 4',
      icon: faBrain,
      color: 'bg-primary',
    },
    {
      type: 'control',
      name: 'Control Agent',
      system: 'System 3',
      icon: faClipboardCheck,
      color: 'bg-blue-400',
    },
    {
      type: 'coordination',
      name: 'Coordination Agent',
      system: 'System 2',
      icon: faHandshake,
      color: 'bg-teal-400',
    },
  ];

  return (
    <div className="bg-card rounded-lg p-6 shadow-elegant">
      <h3 className="text-xl font-semibold mb-4">VSM Hierarchy Pipeline</h3>
      <div className="space-y-3">
        {agents.map((agent, index) => (
          <div key={agent.type}>
            <div
              className={`p-4 rounded-lg border-2 transition-smooth ${
                currentAgent === agent.type
                  ? `${agent.color} border-current shadow-glow animate-pulse-glow`
                  : 'bg-secondary/30 border-border'
              }`}
            >
              <div className="flex items-center gap-3">
                <div
                  className={`w-10 h-10 rounded-full ${agent.color} flex items-center justify-center`}
                >
                  <FontAwesomeIcon icon={agent.icon} className="text-white" />
                </div>
                <div className="flex-1">
                  <div className="font-semibold text-sm">{agent.name}</div>
                  <div className="text-xs text-muted-foreground">{agent.system}</div>
                </div>
                {currentAgent === agent.type && currentPhase && (
                  <div className="text-xs bg-background px-2 py-1 rounded">
                    {currentPhase}
                  </div>
                )}
              </div>
            </div>
            {index < agents.length - 1 && (
              <div className="flex justify-center">
                <FontAwesomeIcon
                  icon={faArrowDown}
                  className="text-muted-foreground text-xl"
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
