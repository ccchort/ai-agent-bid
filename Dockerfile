FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install \
        aiogram==3.17.0 \
        sqlalchemy \
        asyncpg \
        apscheduler \
        pydantic-settings \
        google-api-python-client \
        gspread \
        python-dotenv \
        maxapi

CMD ["python", "-m", "ai.main"]
