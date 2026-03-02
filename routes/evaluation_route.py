from fastapi import APIRouter, Depends
from dependencies.dependency import get_evaluation_service
from pydantic import BaseModel

router = APIRouter(tags=["Evaluation Report"])


class ClassificationReportResponse(BaseModel):
    report: dict


@router.get("/evaluate", response_model=ClassificationReportResponse)
async def evaluate(evaluation_service=Depends(get_evaluation_service)):
    report = await evaluation_service.get_classification_report()
    return ClassificationReportResponse(report=report)
