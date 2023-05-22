# Entropy task api using FastAPI, PostgresSQL and Docker

Very simple api template for demo purposes

## Description

This project template is designed to be used as starting point for api docker images.

## Getting Started

### Major dependencies

Fast.api, Uvicorn, ormar and pytest. More in requirements.txt

### Installing

* ```$ docker-compose up -d --build``` <- Build  🏠 

### Maintaining:
* ```$ docker-compose exec web pytest .``` <- Run tests 🧪
* ```$ docker-compose down --volumes``` <-Clean DB 🧹

### Running

Server should be up on http://127.0.0.1:8008/

By default, Swagger documentation is used. Alternatively ReDoc available on http://127.0.0.1:8008/redoc

Some internal errors will be printed in docker console only.

Good luck.

## Authors

🔥Ilia Rodikov - freeze.eli@gmail.com🔥
