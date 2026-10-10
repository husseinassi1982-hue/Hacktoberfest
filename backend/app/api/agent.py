from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.database.persistence import add_message, create_conversation, get_conversation, get_profile, list_portfolios
from app.models.portfolio import Portfolio
from app.models.profile import InvestorProfile
from app.agent.gemma import answer
from app.models.agent import AgentChatRequest, AgentChatResponse


router = APIRouter(prefix="/agent", tags=["Advisor Agent"])


@router.get("/conversations/{conversation_id}")
def conversation(conversation_id: int, user: dict[str, str] = Depends(get_current_user)):
    result = get_conversation(int(user["id"]), conversation_id)
    if result is None:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")
    return result


@router.post("/chat", response_model=AgentChatResponse)
def chat(request: AgentChatRequest, user: dict[str, str] = Depends(get_current_user)) -> AgentChatResponse:
    user_id = int(user["id"])
    conversation_id = request.conversation_id or create_conversation(user_id, request.message[:80])
    add_message(user_id, conversation_id, "user", request.message)
    if request.profile is None:
        saved_profile = get_profile(user_id)
        if saved_profile and saved_profile.get("profile"):
            request.profile = InvestorProfile.model_validate(saved_profile["profile"])
    if request.portfolio is None:
        saved_portfolios = list_portfolios(user_id)
        if saved_portfolios:
            request.portfolio = Portfolio.model_validate(saved_portfolios[0]["portfolio"])
    response = answer(request)
    add_message(user_id, conversation_id, "assistant", response.message)
    response.conversation_id = conversation_id
    return response
