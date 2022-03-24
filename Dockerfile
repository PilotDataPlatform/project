FROM python:3.9.11-buster

ARG REGISTRY_USERNAME
ARG REGISTRY_PASSWORD

ENV PYTHONUNBUFFERED=true \
    PYTHONDONTWRITEBYTECODE=true \
    PYTHONIOENCODING=UTF-8 \
    POETRY_VERSION=1.1.12 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry config http-basic.pilot ${REGISTRY_USERNAME} ${REGISTRY_PASSWORD}

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev --no-root --no-interaction

COPY project ./project
