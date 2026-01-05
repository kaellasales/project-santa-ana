set unstable

set shell := ["bash", "-cu"]

COMPOSE_FILES := "docker-compose.yml"

compose *args:
    docker compose -p santa_ana -f {{COMPOSE_FILES}} {{args}}

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


django command:
    just exec fast-api python manage.py {{command}}


test *args:
    just exec fast-api poetry run pytest {{args}}

