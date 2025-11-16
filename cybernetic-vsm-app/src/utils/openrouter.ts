import type {
  OpenRouterMessage,
  OpenRouterRequest,
  OpenRouterResponse,
} from '../types';

const OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions';

export class OpenRouterAPI {
  private apiKey: string;
  private model: string;

  constructor(apiKey: string, model: string) {
    this.apiKey = apiKey;
    this.model = model;
  }

  async sendMessage(
    messages: OpenRouterMessage[],
    options?: {
      temperature?: number;
      max_tokens?: number;
    }
  ): Promise<string> {
    if (!this.apiKey) {
      throw new Error('OpenRouter API key is required');
    }

    const request: OpenRouterRequest = {
      model: this.model,
      messages,
      temperature: options?.temperature ?? 0.7,
      max_tokens: options?.max_tokens ?? 4000,
    };

    try {
      const response = await fetch(OPENROUTER_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
          'HTTP-Referer': window.location.origin,
          'X-Title': 'Cybernetic VSM',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          `OpenRouter API error: ${response.status} - ${
            errorData.error?.message || response.statusText
          }`
        );
      }

      const data: OpenRouterResponse = await response.json();

      if (!data.choices || data.choices.length === 0) {
        throw new Error('No response from OpenRouter API');
      }

      return data.choices[0].message.content;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Unknown error occurred while calling OpenRouter API');
    }
  }

  updateCredentials(apiKey: string, model: string): void {
    this.apiKey = apiKey;
    this.model = model;
  }
}
