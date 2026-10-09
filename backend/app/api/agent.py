from fastapi import APIRouter

from app.agent.gemma import answer
from app.models.agent import AgentChatRequest, AgentChatResponse


router = APIRouter(prefix="/agent", tags=["Advisor Agent"])


@router.post("/chat", response_model=AgentChatResponse)
def chat(request: AgentChatRequest) -> AgentChatResponse:
    return answer(request)
