const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

export type AuthUser = { id: string; email: string };
export type InvestorProfileResponse = { profile: Record<string, unknown> | null; risk_profile: Record<string, unknown> | null; updated_at?: string };

export function getToken(): string | null { return sessionStorage.getItem('finpilot_token'); }
export function getStoredUser(): AuthUser | null {
  const value = sessionStorage.getItem('finpilot_user');
  return value ? JSON.parse(value) as AuthUser : null;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set('Content-Type', 'application/json');
  const token = getToken();
  if (token) headers.set('Authorization', `Bearer ${token}`);
  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  if (!response.ok) throw new Error((await response.text()) || `API returned ${response.status}`);
  return response.json() as Promise<T>;
}

export async function authenticate(path: '/auth/login' | '/auth/register', email: string, password: string): Promise<AuthUser> {
  const response = await request<{ token: string; user: AuthUser }>(path, { method: 'POST', body: JSON.stringify({ email, password }) });
  sessionStorage.setItem('finpilot_token', response.token);
  sessionStorage.setItem('finpilot_user', JSON.stringify(response.user));
  return response.user;
}

export function logout(): Promise<{ message: string }> {
  return request<{ message: string }>('/auth/logout', { method: 'POST' }).finally(() => {
    sessionStorage.removeItem('finpilot_token');
    sessionStorage.removeItem('finpilot_user');
  });
}

export function getInvestorProfile(): Promise<InvestorProfileResponse> { return request<InvestorProfileResponse>('/profile/'); }
export function saveInvestorProfile(profile: Record<string, unknown>): Promise<InvestorProfileResponse> {
  return request<InvestorProfileResponse>('/profile/', { method: 'POST', body: JSON.stringify(profile) });
}

export type SavedPosition = { symbol: string; quantity: number; price: number; sector: string; asset_type: string };
export type SavedPortfolio = { id: number; name: string; portfolio: { cash: number; positions: SavedPosition[] }; created_at: string; updated_at: string };
export function getSavedPortfolios(): Promise<{ portfolios: SavedPortfolio[] }> { return request<{ portfolios: SavedPortfolio[] }>('/portfolio/saved'); }

export type AgentToolResult = {
  name: string;
  output: Record<string, unknown>;
};

export type AgentResponse = {
  message: string;
  mode: string;
  tools_used: AgentToolResult[];
  disclaimer: string;
  conversation_id?: number;
  sources?: Array<{ title: string; url?: string; publisher?: string; published_at?: string; content: string }>;
};

export async function askAdvisor(message: string, conversationId?: number): Promise<AgentResponse> {
  return request<AgentResponse>('/agent/chat', { method: 'POST', body: JSON.stringify({ message, conversation_id: conversationId }) });
}
