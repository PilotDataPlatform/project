# Project Service

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.9](https://img.shields.io/badge/python-3.9-brightgreen?style=for-the-badge)](https://www.python.org/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/PilotDataPlatform/project/ci?style=for-the-badge)](https://github.com/PilotDataPlatform/project/actions)
[![codecov](https://img.shields.io/codecov/c/github/PilotDataPlatform/project?style=for-the-badge)](https://codecov.io/gh/PilotDataPlatform/project)

## About

Service for managing projects and project related resources.

### Start

1. Install [Docker](https://www.docker.com/get-started/).
2. Start container with project application.

       docker compose up

3. Visit http://127.0.0.1:5064/v1/api-doc for API documentation.

### Development

1. Install [Poetry](https://python-poetry.org/docs/#installation).
2. Install dependencies.

       poetry install

    2.1. For Mac Users:

        brew install libmagic


3. Add environment variables into `.env`.
4. Run application.

       poetry run python -m project

5. Generate migration (based on comparison of database to defined models).

       docker compose run --rm alembic revision --autogenerate -m "Migration message" --rev-id 0002 --depends-on 0001
