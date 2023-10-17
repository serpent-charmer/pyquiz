from fastapi import APIRouter
from sqlalchemy import select
from pyquiz.data import QuestionRequest
from pyquiz.db import SessionDependency
from pyquiz.model import Question


router = APIRouter(
            prefix="/question",
            tags=["question"]
        )


@router.get("/get")
async def _get(sess:SessionDependency, question_id: int):
    question = await sess.scalars(
        select(Question).where(Question._id == question_id)
    )
    return question.first() or {}