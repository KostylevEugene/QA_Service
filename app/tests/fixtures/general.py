import random

import pytest_asyncio

from app.repositories.answer import AnswerRepository
from app.repositories.question import QuestionRepository


@pytest_asyncio.fixture()
async def question_repo(db_session):
    return QuestionRepository(db_session)


@pytest_asyncio.fixture()
async def question(question_repo):
    return await question_repo.add(text="Is it easy question?")


@pytest_asyncio.fixture()
async def another_question(question_repo):
    return await question_repo.add(text="Is it another easy question?")


@pytest_asyncio.fixture()
async def answer_repo(db_session):
    return AnswerRepository(db_session)


@pytest_asyncio.fixture()
async def answer(answer_repo, question):
    return await answer_repo.add(
        text="This is a Test Answer.",
        user_id=str(random.randint(1, 100)),
        question_id=question.id,
    )
