from prompts.ai_prompts import AIPrompts
from utils.logger import logger


class GeneralService:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, user_query: str, message_history: list):
        prompt = AIPrompts.get_general_prompt(user_query, message_history)
        response = await self.llm.ainvoke(prompt)
        return response.content
