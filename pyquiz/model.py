import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, DeclarativeBase


class QuizBase(DeclarativeBase):
    pass

class Question(QuizBase):
    __tablename__ = 'question'
    _id = mapped_column(sa.Integer, primary_key=True)
    external_id = mapped_column(sa.Integer, unique=True)
    text = mapped_column(sa.Text)
    answer = mapped_column(sa.Text)
    create_date = mapped_column(type_=sa.TIMESTAMP(timezone=True))
