FROM python:3.12-alpine

RUN apk add curl

ENV POETRY_VERSION=2.1.3 \
    POETRY_NO_INTERACTION=true \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME="/opt/poetry" 

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /qa_app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --sync

COPY . .

ENV PYTHONPATH=/qa_app

CMD ["python", "app/main.py"]
