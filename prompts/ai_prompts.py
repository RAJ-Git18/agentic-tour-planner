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

Your task is to politely ask the user for the following missing details: {missing_constraints}.

LOGIC FOR YOUR RESPONSE:
1. If 'to_city' is in the missing details, you MUST mention the cities we currently support: {', '.join(allowed_cities)}.
2. If the user is asking about what tours you provide, list the supported destinations.
3. If 'to_city' is already known, do NOT list all cities; just ask for the other missing fields (like starting city or days).
4. Be direct but friendly."""

        user_content = (
            f"Ask me for the missing details: {', '.join(missing_constraints)}."
        )

        return [
            ("system", system_content),
            ("user", user_content),
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

    @staticmethod
    def get_general_prompt(user_query: str, message_history: list) -> list:
        system_content = """You are a friendly and helpful travel assistant.
Respond to the user's general queries, greetings, or expressions of gratitude politely.
If the query is completely unrelated to travel or the services provided, politely guide them back to tour planning or policy questions."""

        user_content = f"""Message History: {message_history}
User Query: {user_query}"""

        return [
            ("system", system_content),
            ("user", user_content),
        ]
