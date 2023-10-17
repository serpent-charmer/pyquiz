from fastapi import APIRouter
from sqlalchemy import select
from pyquiz.data import QuestionRequest
from pyquiz.db import SessionDependency
from pyquiz.model import Question


router = APIRouter(
            prefix="/question",
            tags=["question"]
        )


@router.post("/get")
async def _post(sess:SessionDependency, data: QuestionRequest):
    question = await sess.execute(
        select(Question).where(Question._id == data.question_id)
    )
    return question.scalar()