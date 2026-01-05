FROM python:3.12-slim 

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.2.1
RUN curl -sSL https://install.python-poetry.org | python3 - --yes
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-root \
    && poetry cache clear --all pypi

COPY . /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
