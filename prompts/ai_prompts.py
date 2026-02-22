class AIPrompts:
    @staticmethod
    def get_tour_constraint_prompt(
        user_query: str, message_history: list, allowed_cities: list
    ) -> list:
        system_content = f"""You are an AI assistant specialized in entity extraction for tour planning.
        
Your task is to retrieve the necessary entities (from_city, to_city, days) from the user query and history.
Database Cities: {allowed_cities}.
Important: Use full city names. Check message history for previously mentioned entities."""

        user_content = f"""Message History: {message_history}
User Query: {user_query}"""

        return [
            ("system", system_content),
            ("user", user_content),
        ]

    @staticmethod
    def get_missing_constraints_prompt(
        missing_constraints: list, allowed_cities: list
    ) -> list:
        system_content = f"""You are a polite AI travel assistant.
        
Your goal is to ask the user to provide the missing information ({missing_constraints}) needed to plan their tour.
Promote our tour packages for: {', '.join(allowed_cities)}."""

        return [
            ("system", system_content),
        ]

    @staticmethod
    def get_planning_prompt(
        user_query: str,
        metadata: dict,
        attractions: list,
        travel: list,
        hotels: list,
    ) -> list:
        system_content = f"""You are an expert tour planner. Create a {metadata['days']}-day tour plan from {metadata['from_city']} to {metadata['to_city']}.

DATA:
- Attractions: {attractions}
- Travel Info: {travel}
- Hotels: {hotels}

INSTRUCTIONS:
1. Provide a {metadata['days']}-day detailed itinerary with specific timings.
2. Select the best hotel from the provided data.
3. Mention travel mode and estimated time.
4. Use ONLY the provided data. No outside knowledge.
5. Title: "Tour Plan for {metadata['from_city']} to {metadata['to_city']}\""""

        return [
            ("system", system_content),
            ("user", f"User Query: {user_query}"),
        ]
