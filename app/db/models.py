from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, comment="ID вопроса"
    )
    text: Mapped[str] = mapped_column(
        nullable=False, unique=True, comment="Текст вопроса"
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), comment="Дата создания"
    )

    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, comment="ID ответа"
    )
    text: Mapped[str] = mapped_column(comment="Текст ответа")
    user_id: Mapped[str] = mapped_column(comment="ID пользователя")
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), comment="ID вопроса"
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), comment="Дата создания"
    )

    question: Mapped["Question"] = relationship(back_populates="answers")
