FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev

COPY . .

EXPOSE 8000

ENV AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED=true

CMD ["poetry", "run", "uvicorn", "startup:app", "--host", "0.0.0.0", "--port", "8000"]