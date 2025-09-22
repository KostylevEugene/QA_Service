from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from app.schemas.answer import Answer


class CreateQuestion(BaseModel):
    text: str = Field(description="Текст вопроса")

    @field_validator("text", mode="after")
    @classmethod
    def is_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("Поле 'text' не должно быть пустым")

        return value


class Question(CreateQuestion):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class EditQuestion(CreateQuestion):
    pass


class QuestionWithAnswers(Question):
    answers: list[Answer]

    class Config:
        from_attributes = True