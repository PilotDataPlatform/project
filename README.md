# Project Service

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)

## About

Service for managing projects and project related resources.

### Start

1. Install [Docker](https://www.docker.com/get-started/).
2. Export environment variables with credentials to internal package registry (PyPI).

       export PIP_USERNAME=... PIP_PASSWORD=...

3. Start container with project application

       docker compose up

4. Visit http://127.0.0.1:5064/v1/api-doc for API documentation.

### Development

1. Install [Poetry](https://python-poetry.org/docs/#installation).
2. Configure access to internal package registry (PyPI).

       poetry config http-basic.pilot ${PIP_USERNAME} ${PIP_PASSWORD}

3. Install dependencies.

       poetry install

4. Add environment variables into `.env`.
5. Run application.

       poetry run python -m project

6. Generate migration (based on comparison of database to defined models).

       docker compose run --rm alembic revision --autogenerate -m "Migration message" --rev-id 0002 --depends-on 0001
