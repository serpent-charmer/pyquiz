from python:3.9-slim-bullseye

RUN python3 -m pip install poetry
RUN mkdir /app

WORKDIR /app 
COPY pyproject.toml /app
RUN poetry install

COPY pyquiz /app/pyquiz
COPY scripts /app/scripts
COPY alembic.ini /app

CMD poetry run alembic upgrade head && poetry run uvicorn pyquiz:app --host 0.0.0.0 --port 80