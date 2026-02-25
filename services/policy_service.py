from services.base_rag import BaseRagService
from utils.logger import logger


class PolicyService(BaseRagService):
    async def run(self, user_query: str) -> str:
        """
        Handles policy-related queries using RAG and re-ranking.
        """
        retriever_results = await self.hybrid_search(
            query=user_query, k=6, filter={"filename": "company.txt"}
        )

        logger.info(f"Retriever results ----> {retriever_results}")

        # Extract documents from Pinecone matches
        retrieved_doc_list = [
            match["metadata"].get("content") or match["metadata"].get("text", "")
            for match in retriever_results["matches"]
        ]

        top_3_docs = await self.ranking_service.rank_documents(
            user_query, retrieved_doc_list
        )

        logger.info(f"Top 3 docs ----> {top_3_docs}")

        prompt = self._get_policy_prompt(user_query, top_3_docs)
        response = await self.llm.ainvoke(prompt)
        return response.content

    def _get_policy_prompt(self, user_query: str, docs: list) -> list:
        system_content = """You are an assistant specialized in addressing user query about company policies, cancellations, and refunds.

RULES:
1. Use ONLY the information provided in the Documents section.
2. Do NOT use prior knowledge or assumptions.
3. Keep the answer short, precise, and factual. Provide the answer within a single paragraph without styling.
4. Always provide the answer in the same language as the user query also consider the user intent.
5. If there is no proper answer in the documents, tell user that there is no answer to this question and ask them to contact the support team.
"""

        user_content = f"""User query: {user_query}

Documents:
{"".join(docs)}"""

        return [
            ("system", system_content),
            ("user", user_content),
        ]
