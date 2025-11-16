import { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faCog, faKey, faMicrochip } from '@fortawesome/free-solid-svg-icons';
import type { Settings } from '../types';
import { DEFAULT_MODEL } from '../types';
import { storage } from '../utils/storage';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (settings: Settings) => void;
  currentSettings: Settings;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({
  isOpen,
  onClose,
  onSave,
  currentSettings,
}) => {
  const [apiKey, setApiKey] = useState(currentSettings.apiKey);
  const [model, setModel] = useState(currentSettings.model);

  useEffect(() => {
    setApiKey(currentSettings.apiKey);
    setModel(currentSettings.model);
  }, [currentSettings]);

  const handleSave = () => {
    const newSettings: Settings = { apiKey, model };
    storage.saveSettings(newSettings);
    onSave(newSettings);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm animate-fade-in">
      <div className="bg-card rounded-lg shadow-elegant w-full max-w-md mx-4 animate-scale-in">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-border">
          <div className="flex items-center gap-3">
            <FontAwesomeIcon icon={faCog} className="text-primary text-xl" />
            <h2 className="text-2xl font-semibold">Settings</h2>
          </div>
          <button
            onClick={onClose}
            className="text-muted-foreground hover:text-foreground transition-smooth"
            aria-label="Close settings"
          >
            <FontAwesomeIcon icon={faTimes} className="text-xl" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* API Key */}
          <div className="space-y-2">
            <label htmlFor="apiKey" className="flex items-center gap-2 text-sm font-medium">
              <FontAwesomeIcon icon={faKey} className="text-accent" />
              OpenRouter API Key
            </label>
            <input
              id="apiKey"
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-or-v1-..."
              className="w-full bg-background border border-input rounded-md px-3 py-2 text-sm
                       focus:outline-none focus:ring-2 focus:ring-ring transition-smooth"
            />
            <p className="text-xs text-muted-foreground">
              Get your API key from{' '}
              <a
                href="https://openrouter.ai/keys"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:text-primary-glow underline"
              >
                openrouter.ai/keys
              </a>
            </p>
          </div>

          {/* Model Selection */}
          <div className="space-y-2">
            <label htmlFor="model" className="flex items-center gap-2 text-sm font-medium">
              <FontAwesomeIcon icon={faMicrochip} className="text-primary" />
              Model
            </label>
            <input
              id="model"
              type="text"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              placeholder={DEFAULT_MODEL}
              className="w-full bg-background border border-input rounded-md px-3 py-2 text-sm
                       focus:outline-none focus:ring-2 focus:ring-ring transition-smooth"
            />
            <p className="text-xs text-muted-foreground">
              Default: <code className="text-xs bg-muted px-1 py-0.5 rounded">{DEFAULT_MODEL}</code>
              <br />
              See available models at{' '}
              <a
                href="https://openrouter.ai/models"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:text-primary-glow underline"
              >
                openrouter.ai/models
              </a>
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 p-6 border-t border-border">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-md text-sm font-medium bg-secondary text-secondary-foreground
                     hover:bg-secondary/90 transition-smooth"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-4 py-2 rounded-md text-sm font-medium bg-primary text-primary-foreground
                     hover:bg-primary/90 shadow-glow transition-smooth"
          >
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
};
