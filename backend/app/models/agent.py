from pydantic import BaseModel, Field

from app.models.portfolio import Portfolio
from app.models.profile import InvestorProfile


class AgentChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    profile: InvestorProfile | None = None
    portfolio: Portfolio | None = None
    conversation_id: int | None = Field(default=None, gt=0)


class AgentToolResult(BaseModel):
    name: str
    output: dict


class AgentChatResponse(BaseModel):
    message: str
    mode: str
    tools_used: list[AgentToolResult] = Field(default_factory=list)
    disclaimer: str
    conversation_id: int | None = None
    sources: list[dict] = Field(default_factory=list)
