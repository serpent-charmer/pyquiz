from datetime import datetime
from fastapi import APIRouter
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from pyquiz.db import SessionDependency
from pyquiz.data import QuizRequest
from pyquiz.model import Question
from pyquiz.request import get_questions


router = APIRouter(
            prefix="/quiz",
            tags=["quiz"]
        )


async def populate_db(sess, qnum):
    questions = await get_questions(qnum)
    while questions:
        qs = questions.pop()
        try :
            td = datetime.strptime(qs["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
            i = insert(Question).values(
                external_id = qs["id"],
                text= qs["question"],
                answer= qs["answer"],
                create_date= td
            )
            await sess.execute(i)
            await sess.commit()
        except IntegrityError as e:
            await sess.rollback()
            replace = await get_questions(1)
            questions.extend(replace)


@router.post("/random")
async def _post(sess: SessionDependency, data: QuizRequest):
    await populate_db(sess, data.question_num)