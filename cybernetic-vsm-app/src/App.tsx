import { useState, useEffect, useRef } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faCog,
  faPaperPlane,
  faSpinner,
  faRobot,
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import { SettingsModal } from './components/SettingsModal';
import { AgentMessage } from './components/AgentMessage';
import { VSMDiagram } from './components/VSMDiagram';
import type { Settings, ExecutionStatus, AgentType } from './types';
import { DEFAULT_MODEL } from './types';
import { storage } from './utils/storage';
import { VSMPipeline } from './utils/vsmPipeline';

function App() {
  const [settings, setSettings] = useState<Settings>({
    apiKey: '',
    model: DEFAULT_MODEL,
  });
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [taskDescription, setTaskDescription] = useState('');
  const [executionStatus, setExecutionStatus] = useState<ExecutionStatus>({
    status: 'idle',
    progress: 0,
    messages: [],
  });
  const [pipeline, setPipeline] = useState<VSMPipeline | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load settings on mount
  useEffect(() => {
    const savedSettings = storage.getSettings();
    setSettings(savedSettings);
    if (savedSettings.apiKey) {
      setPipeline(new VSMPipeline(savedSettings.apiKey, savedSettings.model));
    }
  }, []);

  // Auto-scroll messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [executionStatus.messages]);

  const handleSettingsSave = (newSettings: Settings) => {
    setSettings(newSettings);
    if (newSettings.apiKey) {
      setPipeline(new VSMPipeline(newSettings.apiKey, newSettings.model));
    }
  };

  const handleExecuteTask = async () => {
    if (!taskDescription.trim()) {
      return;
    }

    if (!settings.apiKey) {
      alert('Please configure your OpenRouter API key in settings');
      setIsSettingsOpen(true);
      return;
    }

    if (!pipeline) {
      setPipeline(new VSMPipeline(settings.apiKey, settings.model));
      return;
    }

    setExecutionStatus({
      status: 'executing',
      progress: 0,
      messages: [],
    });

    try {
      const result = await pipeline.executeTask(
        taskDescription,
        (agent: AgentType, phase: string, progress: number) => {
          setExecutionStatus((prev) => ({
            ...prev,
            currentAgent: agent,
            currentPhase: phase,
            progress,
            messages: pipeline.getMessages(),
          }));
        }
      );

      setExecutionStatus({
        status: 'completed',
        progress: 100,
        messages: result.messages,
        result: result.result,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      setExecutionStatus((prev) => ({
        ...prev,
        status: 'error',
        error: errorMessage,
        messages: pipeline.getMessages(),
      }));
    }
  };

  const handleReset = () => {
    setExecutionStatus({
      status: 'idle',
      progress: 0,
      messages: [],
    });
    setTaskDescription('');
  };

  const isExecuting = executionStatus.status === 'executing';
  const hasApiKey = !!settings.apiKey;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-gradient-primary py-6 px-6 shadow-elegant">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <FontAwesomeIcon icon={faRobot} className="text-4xl text-white" />
            <div>
              <h1 className="text-3xl font-bold text-white">Cybernetic VSM</h1>
              <p className="text-sm text-white/80">Viable System Model Pipeline</p>
            </div>
          </div>
          <button
            onClick={() => setIsSettingsOpen(true)}
            className="w-12 h-12 rounded-full bg-white/10 hover:bg-white/20
                     flex items-center justify-center transition-smooth"
            aria-label="Open settings"
          >
            <FontAwesomeIcon icon={faCog} className="text-white text-xl" />
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {!hasApiKey && (
          <div className="mb-6 bg-destructive/10 border border-destructive rounded-lg p-4 flex items-start gap-3">
            <FontAwesomeIcon icon={faExclamationTriangle} className="text-destructive text-xl mt-1" />
            <div>
              <h3 className="font-semibold text-destructive mb-1">API Key Required</h3>
              <p className="text-sm text-destructive/80">
                Please configure your OpenRouter API key in settings to use the VSM pipeline.
              </p>
              <button
                onClick={() => setIsSettingsOpen(true)}
                className="mt-2 text-sm font-medium text-destructive hover:text-destructive/80 underline"
              >
                Open Settings
              </button>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Input & VSM Diagram */}
          <div className="lg:col-span-1 space-y-6">
            {/* Task Input */}
            <div className="bg-card rounded-lg p-6 shadow-elegant">
              <h2 className="text-xl font-semibold mb-4">Task Input</h2>
              <div className="space-y-4">
                <textarea
                  value={taskDescription}
                  onChange={(e) => setTaskDescription(e.target.value)}
                  placeholder="Describe your task here... The VSM pipeline will analyze, plan, and execute it through the cybernetic hierarchy."
                  disabled={isExecuting}
                  rows={6}
                  className="w-full bg-background border border-input rounded-md px-3 py-2
                           focus:outline-none focus:ring-2 focus:ring-ring transition-smooth
                           resize-none disabled:opacity-50 disabled:cursor-not-allowed"
                />
                <div className="flex gap-3">
                  <button
                    onClick={handleExecuteTask}
                    disabled={!taskDescription.trim() || isExecuting || !hasApiKey}
                    className="flex-1 bg-primary text-primary-foreground rounded-md px-4 py-2
                             font-medium hover:bg-primary/90 shadow-glow transition-smooth
                             disabled:opacity-50 disabled:cursor-not-allowed flex items-center
                             justify-center gap-2"
                  >
                    {isExecuting ? (
                      <>
                        <FontAwesomeIcon icon={faSpinner} className="animate-spin" />
                        Executing...
                      </>
                    ) : (
                      <>
                        <FontAwesomeIcon icon={faPaperPlane} />
                        Execute Task
                      </>
                    )}
                  </button>
                  {executionStatus.status !== 'idle' && (
                    <button
                      onClick={handleReset}
                      disabled={isExecuting}
                      className="px-4 py-2 rounded-md font-medium bg-secondary
                               text-secondary-foreground hover:bg-secondary/90
                               transition-smooth disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Reset
                    </button>
                  )}
                </div>
              </div>

              {/* Progress Bar */}
              {isExecuting && (
                <div className="mt-4">
                  <div className="flex items-center justify-between text-xs text-muted-foreground mb-1">
                    <span>Progress</span>
                    <span>{executionStatus.progress}%</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
                    <div
                      className="bg-gradient-primary h-full transition-all duration-500"
                      style={{ width: `${executionStatus.progress}%` }}
                    />
                  </div>
                </div>
              )}
            </div>

            {/* VSM Diagram */}
            <VSMDiagram
              currentAgent={executionStatus.currentAgent}
              currentPhase={executionStatus.currentPhase}
            />
          </div>

          {/* Right Column - Messages */}
          <div className="lg:col-span-2">
            <div className="bg-card rounded-lg p-6 shadow-elegant">
              <h2 className="text-xl font-semibold mb-4">Agent Messages</h2>
              <div className="space-y-4 max-h-[calc(100vh-16rem)] overflow-y-auto pr-2">
                {executionStatus.messages.length === 0 ? (
                  <div className="text-center py-12 text-muted-foreground">
                    <FontAwesomeIcon icon={faRobot} className="text-5xl mb-4" />
                    <p>No messages yet. Execute a task to see the VSM pipeline in action.</p>
                  </div>
                ) : (
                  <>
                    {executionStatus.messages.map((message) => (
                      <AgentMessage key={message.id} message={message} />
                    ))}
                    <div ref={messagesEndRef} />
                  </>
                )}
              </div>

              {/* Status Footer */}
              {executionStatus.status !== 'idle' && (
                <div className="mt-4 pt-4 border-t border-border">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium">Status:</span>
                    <span
                      className={`text-sm px-2 py-1 rounded ${
                        executionStatus.status === 'completed'
                          ? 'bg-success/10 text-success'
                          : executionStatus.status === 'error'
                          ? 'bg-destructive/10 text-destructive'
                          : 'bg-primary/10 text-primary'
                      }`}
                    >
                      {executionStatus.status.charAt(0).toUpperCase() +
                        executionStatus.status.slice(1)}
                    </span>
                  </div>
                  {executionStatus.error && (
                    <div className="mt-2 text-sm text-destructive">
                      Error: {executionStatus.error}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onSave={handleSettingsSave}
        currentSettings={settings}
      />
    </div>
  );
}

export default App;
