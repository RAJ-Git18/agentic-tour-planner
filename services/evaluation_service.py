from fastapi import APIRouter
import pandas as pd
from services.classify_services import ClassifyService
from utils.logger import logger
from typing import List
from sklearn.metrics import classification_report
import json


class EvaluationService:
    def __init__(self, classify_service: ClassifyService):
        self.classify_service = classify_service
        self.df = pd.read_csv("data/router_test_case.csv")

    async def get_predicted_intent(self):
        predicted_intent_list = []
        for idx, user_query in enumerate(self.df["query"].tolist()):
            intent = await self.classify_service.classify(
                user_query, message_history=[]
            )
            predicted_intent_list.append(intent)
            logger.info(f"Completed Query {idx + 1}")
        self.df["predicted_intent"] = predicted_intent_list

    async def get_classification_report(self):
        await self.get_predicted_intent()
        report = classification_report(
            self.df["class"], self.df["predicted_intent"], output_dict=True
        )
        try:
            with open("../data/evaluation_report.json", "w") as f:
                json.dump(report, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing evaluation report: {e}")
        logger.info(report)
        return report
