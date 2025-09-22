from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.services import AnswerService, QuestionService
from app.repositories import AnswerRepository, QuestionRepository
from app.db.connection import AsyncSessionLocal


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


def question_service(session: async_sessionmaker = Depends(get_db)):
    return QuestionService(session)


def answer_service(session: async_sessionmaker = Depends(get_db)):
    return AnswerService(session)
