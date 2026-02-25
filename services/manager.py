from config import settings
from utils.logger import logger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder
from redis.asyncio import Redis
from services.pinecone_service import pc_service


class Manager:
    _instance = None

    def __init__(self):
        pinecone_api_key = settings.PINECONE_API_KEY
        gemini_api_key = settings.GEMINI_API_KEY

        if not pinecone_api_key or not gemini_api_key:
            raise RuntimeError("Missing API keys in environment.")

        self.pc_index = pc_service.get_index()

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", google_api_key=gemini_api_key, temperature=0
        )

        self.emb_model = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
        self.cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

        self.redis_client = Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
        )

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Manager()
        return cls._instance

    def load_all_instances(self):
        instances = {
            "pc_index": self.pc_index,
            "llm": self.llm,
            "emb_model": self.emb_model,
            "cross_encoder": self.cross_encoder,
            "redis_client": self.redis_client,
        }
        return instances
