import sys
import logging
import os
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller to get correct stack depth
        frame, depth = logging.currentframe(), 2
        while frame.f_back and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    logger.remove()
    logger.add(
        sink=sys.stdout,
        format=(
            "<level>{time:YYYY-MM-DD HH:mm:ss}</level> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level> | "
            "<level>{exception}</level> | "
        ),
        level="INFO",
        colorize=True,
        diagnose=False,
    )

    logger.add(
        sink="logs/app.log",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            " {level: <8} | {name}:{function}:{line} | {message}"
        ),
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        enqueue=True,
        diagnose=False,
    )

    """Подключает логирование"""
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    os.makedirs("logs", exist_ok=True)

    # Перенаправляются логи от uvicorn и fastapi
    loggers = (
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
    )
    for name in loggers:
        logging.getLogger(name).handlers = [InterceptHandler()]
        logging.getLogger(name).propagate = False
