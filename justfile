set unstable
set shell := ["bash", "-cu"]


PROJECT_NAME := "santa_ana"
COMPOSE_FILES := "docker-compose.yml"

compose *args:
    docker compose -p {{PROJECT_NAME}} -f {{COMPOSE_FILES}} {{args}}

build:
    just compose build

start:
    just compose up -d

stop:
    just compose down

reload:
    just stop
    just start

exec service *cmd:
    just compose exec -it {{service}} {{cmd}}

shell:
    just exec fast-api /bin/bash

test *args:
    just exec fast-api poetry run pytest {{args}}

rebuild:
    just stop
    just compose build
    just start

makemigrations *args:
    docker compose -p {{PROJECT_NAME}} -f {{COMPOSE_FILES}} exec fast-api poetry run alembic revision --autogenerate -m "{{args}}"

migrate:
    just exec fast-api poetry run alembic upgrade head

db-reset:
    docker compose -p {{PROJECT_NAME}} -f {{COMPOSE_FILES}} exec db psql -U postgres -d santa_ana_db -c "TRUNCATE TABLE formas_pagamento, itens_venda, vendas, produtos, categorias RESTART IDENTITY CASCADE;"