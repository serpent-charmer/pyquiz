from fastapi import FastAPI


from .route.quiz import router as quiz_r
from .route.question import router as question_r

app = FastAPI()

app.include_router(quiz_r)
app.include_router(question_r)
