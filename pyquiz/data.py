from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question_id:int

class QuizRequest(BaseModel):
    question_num:int