import json

from workflow.state import GraphState
from langchain_core.runnables import RunnableConfig
from utils.logger import logger


async def planner_node(
    state: GraphState,
    config: RunnableConfig,
):
    """
    Gets the answer to the user query from the policy document
    """
    cfg = config.get("configurable")
    rag_service = cfg.get("rag_service")
    user_query = state.get("user_query")
    messages = state.get("messages") or []
    if rag_service and user_query:
        response = await rag_service.tour_planning_service(
            user_query=user_query, message_history=messages
        )

        # Determine what to save to history.
        # If it's a full plan (dict), just save the title so we don't clog history with JSON.
        history_content = (
            response.get("title") if isinstance(response, dict) else response
        )

        messages.append({"role": "user", "content": user_query})
        messages.append({"role": "assistant", "content": history_content})
    else:
        raise ValueError("RAG service returned none.")
    title = response.get("title") if isinstance(response, dict) else None

    return {"response": response, "messages": messages, "title": title}
