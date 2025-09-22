import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator


class CreateAnswer(BaseModel):
    user_id: str
    text: str

    @field_validator("text", mode="after")
    @classmethod
    def is_text_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("Поле 'text' не должно быть пустым")

        return value
    
    @field_validator("user_id", mode="after")
    @classmethod
    def is_user_empty(cls, value: str) -> str:
        if not value:
            value = str(uuid.uuid4())

        return value


class Answer(CreateAnswer):
    id: int
    question_id: int
    created_at: datetime
