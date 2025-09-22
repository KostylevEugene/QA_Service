from sqlalchemy import select

from app.db.models import Answer
from .general import GeneralRepository


class AnswerRepository(GeneralRepository):
    model = Answer

    async def get_by_question_id(self, question_id: int):
        result = await self.session.execute(
            select(self.model).where(self.model.question_id == question_id)
        )
        return result.scalars().all()