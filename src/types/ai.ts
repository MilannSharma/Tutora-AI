/**
 * Tutora AI Public Supported Providers and Model Identifiers
 */

export type AIProvider = "gemini" | "groq" | "openrouter" | "openai" | "claude";

export interface AIProviderMetadata {
  id: AIProvider;
  name: string;
  defaultModel: string;
  freeTierAvailable: boolean;
  rateLimitTokensPerMin?: number;
}

export const SUPPORTED_AI_PROVIDERS: Record<AIProvider, AIProviderMetadata> = {
  gemini: {
    id: "gemini",
    name: "Google Gemini",
    defaultModel: "gemini-2.5-flash",
    freeTierAvailable: true,
    rateLimitTokensPerMin: 1_000_000,
  },
  groq: {
    id: "groq",
    name: "Groq Cloud",
    defaultModel: "llama-3.3-70b-versatile",
    freeTierAvailable: true,
  },
  openrouter: {
    id: "openrouter",
    name: "OpenRouter Hub",
    defaultModel: "auto",
    freeTierAvailable: true,
  },
  openai: {
    id: "openai",
    name: "OpenAI Platform",
    defaultModel: "gpt-4o-mini",
    freeTierAvailable: false,
  },
  claude: {
    id: "claude",
    name: "Anthropic Claude",
    defaultModel: "claude-3-5-sonnet-20241022",
    freeTierAvailable: false,
  },
};
