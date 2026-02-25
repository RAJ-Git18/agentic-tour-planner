import json

from workflow.state import GraphState
from langchain_core.runnables import RunnableConfig
from utils.logger import logger


async def general_node(state: GraphState, config: RunnableConfig):
    """
    Get the general answer to the user query.
    """
    cfg = config.get("configurable")
    general_service = cfg.get("general_service")
    user_query = state.get("user_query")
    messages = state.get("messages") or []

    if general_service and user_query:
        response = await general_service.run(
            user_query=user_query, message_history=messages
        )
        messages.append({"role": "user", "content": user_query})
        messages.append({"role": "assistant", "content": response})
    else:
        response = "I am unable to answer your query at the moment."

    return {"response": response, "messages": messages}
