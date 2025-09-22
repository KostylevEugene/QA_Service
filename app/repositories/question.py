from app.db.models import Question
from .general import GeneralRepository


class QuestionRepository(GeneralRepository):
    model = Question
