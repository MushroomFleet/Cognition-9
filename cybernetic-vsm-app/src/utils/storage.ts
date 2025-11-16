import type { Settings } from '../types';
import { DEFAULT_MODEL } from '../types';

const STORAGE_KEYS = {
  SETTINGS: 'cybernetic-vsm-settings',
} as const;

export const storage = {
  getSettings(): Settings {
    try {
      const stored = localStorage.getItem(STORAGE_KEYS.SETTINGS);
      if (stored) {
        return JSON.parse(stored);
      }
    } catch (error) {
      console.error('Error reading settings from storage:', error);
    }
    return {
      apiKey: '',
      model: DEFAULT_MODEL,
    };
  },

  saveSettings(settings: Settings): void {
    try {
      localStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(settings));
    } catch (error) {
      console.error('Error saving settings to storage:', error);
    }
  },

  clearSettings(): void {
    try {
      localStorage.removeItem(STORAGE_KEYS.SETTINGS);
    } catch (error) {
      console.error('Error clearing settings from storage:', error);
    }
  },
};
