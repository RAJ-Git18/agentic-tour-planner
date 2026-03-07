from utils.logger import logger
from pydantic import BaseModel
from typing import List


class Intent(BaseModel):
    reasoning: str
    intent: str


class ClassifyService:
    """
    Classifies the intent of the user query like policy, tour planning, booking or general inquiry
    """

    def __init__(self, llm):
        self.llm = llm

    async def classify(self, user_query, message_history: List[str] | None = None):
        prompt = self._get_classify_prompt(
            user_query=user_query, message_history=message_history
        )
        structured_llm = self.llm.with_structured_output(Intent)
        response = await structured_llm.ainvoke(prompt)
        intent_data = response.model_dump()
        logger.info(f"classify reasoning ----> {intent_data['reasoning']}")
        logger.info(f"classify result ----> {intent_data['intent']}")
        return intent_data["intent"]

    def _get_classify_prompt(self, user_query, message_history):
        system_context = """You are an expert intent classifier for a Nepal-based tour planning service.
Your task is to categorize the user's query and provide a brief reasoning.

Intents:
- policy: Questions about rules, terms, or 'how-to' procedures. (e.g., "What is the refund policy?", "How do I cancel?").
- planning: Trip creation, itineraries, attractions. (e.g., "Plan a day in KTM").
- ask_booking: Checking STATUS or DETAILS of an existing booking. (e.g., "Is my trip confirmed?", "What is the status?", "Verify my reservation").
- confirm_booking: DIRECT INSTRUCTION to finalize, pay, or execute a new booking. (e.g., "Book it now", "Finalize payment", "Go ahead with booking").
- cancel_booking: DIRECT INSTRUCTION to cancel an active booking. (e.g., "Cancel reservation NP-12345").
- general: Greetings, thanks, or random chat.

CRITICAL RULE for 'Confirm':
- If the user uses the word 'confirm' to ask about status (e.g., "I want to confirm my booking is safe"), use 'ask_booking'.
- If the user uses the word 'confirm' to give an order (e.g., "Confirm this booking now"), use 'confirm_booking'.

User Message History: {message_history}"""

        return [("system", system_context), ("user", f"User query: {user_query}")]
