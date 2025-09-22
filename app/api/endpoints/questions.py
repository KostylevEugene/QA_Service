from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import answer_service, question_service
from app.schemas.answer import Answer, CreateAnswer
from app.schemas.question import (
    CreateQuestion,
    EditQuestion,
    Question,
    QuestionWithAnswers,
)
from app.services.answer import AnswerService
from app.services.exceptions import QuestionAlreadyExists, QuestionNotExists
from app.services.question import QuestionService

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/", response_model=Question, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: CreateQuestion,
    question_service: Annotated[QuestionService, Depends(question_service)],
):
    try:
        return await question_service.add_question(question_data)
    except QuestionAlreadyExists as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.get("/{question_id}", response_model=QuestionWithAnswers)
async def get_question(
    question_id: int,
    question_service: Annotated[QuestionService, Depends(question_service)],
):
    try:
        return await question_service.get_question(question_id=question_id)
    except QuestionNotExists as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.get("/", response_model=list[Question])
async def get_questions(
    question_service: Annotated[QuestionService, Depends(question_service)],
):
    try:
        return await question_service.get_questions()
    except QuestionNotExists as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.patch("/{question_id}", response_model=Question)
async def edit_question(
    question_id: int,
    question_data: EditQuestion,
    question_service: Annotated[QuestionService, Depends(question_service)],
):
    try:
        return await question_service.edit_question(
            question_id=question_id, data=question_data
        )
    except QuestionNotExists as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: int,
    question_service: Annotated[QuestionService, Depends(question_service)],
):
    try:
        await question_service.delete_question(question_id=question_id)
    except QuestionNotExists as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.post(
    "/{question_id}/answers",
    response_model=Answer,
    status_code=status.HTTP_201_CREATED,
)
async def create_answer(
    question_id: int,
    answer_data: CreateAnswer,
    answer_service: Annotated[AnswerService, Depends(answer_service)],
):
    try:
        return await answer_service.add_answer(
            question_id=question_id, answer_data=answer_data
        )
    except QuestionNotExists as e:
        raise HTTPException(status_code=404, detail=e.msg)
