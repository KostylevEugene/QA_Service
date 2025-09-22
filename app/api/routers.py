from fastapi import APIRouter

from .endpoints import answers, questions


router = APIRouter()

router.include_router(questions.router)
router.include_router(answers.router)
