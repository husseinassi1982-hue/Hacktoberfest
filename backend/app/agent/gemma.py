import json
import logging
import os
from typing import Any

from app.agent.prompts import DISCLAIMER, SYSTEM_PROMPT
from app.agent.tools import analyze_portfolio_tool, stress_test_tool
from app.models.agent import AgentChatRequest, AgentChatResponse, AgentToolResult
from app.rag.retrieval import search as search_sources

logger = logging.getLogger(__name__)


def _deterministic_answer(request: AgentChatRequest) -> AgentChatResponse:
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


def _context_for_model(request: AgentChatRequest) -> tuple[str, list[AgentToolResult], list[dict]]:
    tools_used: list[AgentToolResult] = []
    context: dict[str, Any] = {"question": request.message}
    sources = search_sources(request.message, limit=4)
    context["sources"] = sources
    if request.profile is not None:
        context["profile"] = request.profile.model_dump(mode="json")
    if request.portfolio is not None:
        analysis = analyze_portfolio_tool(request.portfolio)
        stress = stress_test_tool(request.portfolio)
        tools_used.extend([
            AgentToolResult(name="analyze_portfolio", output=analysis),
            AgentToolResult(name="stress_test", output=stress),
        ])
        context["analysis"] = analysis
        context["stress_test"] = stress
    return json.dumps(context, ensure_ascii=False, default=str), tools_used, sources


def _gemma_answer(request: AgentChatRequest) -> AgentChatResponse | None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        context, tools_used, sources = _context_for_model(request)
        response = client.models.generate_content(
            model=os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it"),
            contents=(
                "Réponds en français à la question du client. Utilise uniquement le contexte JSON fourni. "
                "Explique les hypothèses et l’incertitude. Ne prétends jamais exécuter une transaction, "
                "ne garantis aucun rendement et distingue les faits des scénarios.\n\n"
                f"Contexte JSON :\n{context}"
            ),
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
                thinking_config=types.ThinkingConfig(thinking_level="minimal"),
            ),
        )
        return AgentChatResponse(
            message=(response.text or "Je n’ai pas pu produire une réponse.").strip(),
            mode="gemma-4",
            tools_used=tools_used,
            disclaimer=DISCLAIMER,
            sources=sources,
        )
    except Exception as error:
        logger.exception("Gemma provider call failed: %s", error)
        return None


def answer(request: AgentChatRequest) -> AgentChatResponse:
    return _gemma_answer(request) or _deterministic_answer(request)
