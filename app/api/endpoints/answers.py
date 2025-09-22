from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import answer_service
from app.schemas.answer import Answer
from app.services.answer import AnswerService
from app.services.exceptions import AnswerNotExists

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/{answer_id}", response_model=Answer)
async def get_answer(
    answer_id: int,
    answer_service: Annotated[AnswerService, Depends(answer_service)],
):
    try:
        return await answer_service.get_answer(answer_id=answer_id)
    except AnswerNotExists as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(
    answer_id: int,
    answer_service: Annotated[AnswerService, Depends(answer_service)],
):
    try:
        await answer_service.delete_answer(answer_id=answer_id)
    except AnswerNotExists as e:
        raise HTTPException(status_code=409, detail=e.msg)
