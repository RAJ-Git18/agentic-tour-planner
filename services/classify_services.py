from utils.logger import logger
from pydantic import BaseModel


class Intent(BaseModel):
    intent: str


class ClassifyService:
    """
    Classifies the intent of the user query like policy, tour planning, booking or general inquiry
    """

    def __init__(self, llm):
        self.llm = llm

    async def classify(self, user_query, message_history):
        prompt = self._get_classify_prompt(
            user_query=user_query, message_history=message_history
        )
        structured_llm = self.llm.with_structured_output(Intent)
        response = await structured_llm.ainvoke(prompt)
        intent = response.model_dump()
        logger.info(f"classify service ----> {intent}")
        return intent["intent"]

    def _get_classify_prompt(self, user_query, message_history):
        system_context = f"""You are an assistant that classifies user intent.
        
User Message History: {message_history}

Intents:
- policy: Company information, name, policies, cancellations, refunds, or terms of service.
- planning: Tour planning, itineraries, finding attractions, or destination queries.
- booking: Booking trips, hotels, or flights.
- general: Simple greetings (hi, hello), thanks, or irrelevant/out‑of‑scope chat.

Note: Consider the message history to see if the user is continuing a previous topic."""

        return [("system", system_context), ("user", f"User query: {user_query}")]
