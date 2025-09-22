from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.repositories.exceptions import EntityAlreadyExistError
from app.repositories.question import QuestionRepository
# from app.services.answer import AnswerService
from app.services.exceptions import QuestionAlreadyExists, QuestionNotExists
from app.schemas.question import CreateQuestion, EditQuestion, Question


class QuestionService:
    def __init__(self, session: async_sessionmaker):
        self.repo = QuestionRepository(session)

    async def add_question(self, data: CreateQuestion) -> Question:
        try:
            question = data.model_dump()
            return await self.repo.add(**question)
        except EntityAlreadyExistError:
            raise QuestionAlreadyExists(
                f"Подобный вопрос уже существует - {question}"
            )

    async def get_question(self, question_id: int) -> Question:
        if question := await self.repo.get_by_id(model_id=question_id):
            return question
        else:
            msg = f"Вопроса с id = {question_id} не существует"
            logger.error(msg)
            raise QuestionNotExists(msg=msg)

    
    async def get_questions(self) -> list[Question]:
        if result := await self.repo.get_all():
            return result
        else:
            msg = "Вопросов не найдено"
            logger.error(msg)
            raise QuestionNotExists(msg=msg)


    async def edit_question(
        self, question_id: int, data: EditQuestion
    ) -> Question:
        edited_question = data.model_dump()
        if result := await self.repo.update_by_id(
            model_id=question_id, **edited_question
        ):
            return result
        else:
            msg = f"Вопроса с id = {question_id} не существует"
            logger.error(msg)
            raise QuestionNotExists(msg=msg)



    async def delete_question(self, question_id):
        if await self.repo.get_by_id(model_id=question_id):
            await self.repo.delete(model_id=question_id)
        else:
            msg = f"Вопроса с id = {question_id} не существует"
            logger.error(msg)
            raise QuestionNotExists(msg=msg)