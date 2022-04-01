# Project Service

Service for managing projects and project related resources.

### Prerequisites

- [Poetry](https://python-poetry.org/) dependency manager.

### Installation

1. Install [Poetry](https://python-poetry.org/docs/#installation).
2. Configure access to internal package registry (PyPI).

       poetry config http-basic.pilot ${REGISTRY_USERNAME} ${REGISTRY_PASSWORD}

3. Install dependencies.

       poetry install

4. Add environment variables into `.env`.
5. Run application.

       poetry run python project/start.py
