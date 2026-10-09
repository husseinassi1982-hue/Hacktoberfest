from typing import Any

from app.agent.prompts import DISCLAIMER
from app.agent.tools import analyze_portfolio_tool, stress_test_tool
from app.models.agent import AgentChatRequest, AgentChatResponse, AgentToolResult


def answer(request: AgentChatRequest) -> AgentChatResponse:
    tools_used: list[AgentToolResult] = []
    message = (
        "Je peux analyser votre portefeuille, comparer son risque et simuler des "
        "scénarios. Fournissez vos positions ou connectez votre compte pour commencer."
    )

    if request.portfolio is not None:
        analysis = analyze_portfolio_tool(request.portfolio)
        tools_used.append(AgentToolResult(name="analyze_portfolio", output=analysis))
        stress = stress_test_tool(request.portfolio)
        tools_used.append(AgentToolResult(name="stress_test", output=stress))
        message = (
            f"Votre portefeuille vaut {analysis['total_value']:.2f}. "
            f"Le scénario « risk-off » produit un impact estimé de "
            f"{stress['total_pnl']:.2f}. "
            "Ce résultat est une hypothèse de stress, pas une prévision."
        )

    return AgentChatResponse(
        message=message,
        mode="deterministic-tools",
        tools_used=tools_used,
        disclaimer=DISCLAIMER,
    )
