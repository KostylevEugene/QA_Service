from sqlalchemy.ext.asyncio import async_sessionmaker

from app.repositories.answer import AnswerRepository
from app.schemas.answer import Answer, CreateAnswer
from app.services.exceptions import AnswerNotExists, QuestionNotExists
from app.services.question import QuestionService

from loguru import logger


class AnswerService:
    def __init__(self, session: async_sessionmaker):
        self.repo = AnswerRepository(session)
        self.question_service = QuestionService(session)

    async def add_answer(
        self, question_id: int, answer_data: CreateAnswer
    ) -> Answer:
        if await self.question_service.get_question(question_id=question_id):
            return await self.repo.add(
                question_id=question_id, **answer_data.model_dump()
            )
        else:
            msg = f"Вопроса с id = {question_id} не существует"
            logger.error(msg)
            raise QuestionNotExists(msg=msg)

    async def get_answer(self, answer_id: int) -> Answer:
        if result := await self.repo.get_by_id(model_id=answer_id):
            return result
        else:
            msg = f"Ответа с id = {answer_id} не существует"
            logger.error(msg)
            raise AnswerNotExists(msg=msg)

    async def get_answers_by_question(self, question_id: int) -> list[Answer]:
        if result := await self.repo.get_by_question_id(
            question_id=question_id
        ):
            return result
        else:
            msg = f"Ответов на вопрос с id = {question_id} не найдено"
            logger.error(msg)
            raise AnswerNotExists(msg=msg)

    async def delete_answer(self, answer_id: int) -> None:
        if await self.repo.get_by_id(model_id=answer_id):
            await self.repo.delete(model_id=answer_id)
        else:
            msg = f"Ответа с id = {answer_id} не существует"
            logger.error(msg)
            raise AnswerNotExists(msg=msg)
