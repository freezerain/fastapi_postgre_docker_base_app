# API App using FastAPI, PostgresSQL, and Docker 🚀

A simple and dynamic FastAPI application seamlessly integrated with a PostgresSQL database within a Docker image.

## Description

This project template serves as a versatile starting point for various future projects, fostering easy development and scalability.

## Getting Started

### Major Dependencies

- FastAPI
- Uvicorn
- Ormar
- Pytest
- More details in `requirements.txt`

### Installing

```bash
$ docker-compose up -d --build  # Build 🏠
```

### Maintenance

* Run tests 🧪
  ```bash
  $ docker-compose exec web pytest .
  ```

* Clean DB 🧹
  ```bash
  $ docker-compose down --volumes
  ```

### Running

The server is accessible at http://127.0.0.1:8008/

By default, Swagger documentation is available. Alternatively, you can use ReDoc at http://127.0.0.1:8008/redoc

Certain internal errors will be displayed in the Docker console only.

Wishing you the best of luck! 🌟

## Authors

🔥 Ilia Rodikov - freeze.eli@gmail.com 🔥