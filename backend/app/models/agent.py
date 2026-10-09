from pydantic import BaseModel, Field

from app.models.portfolio import Portfolio
from app.models.profile import InvestorProfile


class AgentChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    profile: InvestorProfile | None = None
    portfolio: Portfolio | None = None


class AgentToolResult(BaseModel):
    name: str
    output: dict


class AgentChatResponse(BaseModel):
    message: str
    mode: str
    tools_used: list[AgentToolResult] = Field(default_factory=list)
    disclaimer: str
