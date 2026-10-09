const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

export type AgentToolResult = {
  name: string;
  output: Record<string, unknown>;
};

export type AgentResponse = {
  message: string;
  mode: string;
  tools_used: AgentToolResult[];
  disclaimer: string;
};

export async function askAdvisor(message: string): Promise<AgentResponse> {
  const response = await fetch(`${API_BASE_URL}/agent/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Advisor API returned ${response.status}`);
  }

  return response.json() as Promise<AgentResponse>;
}
