# syntax=docker/dockerfile:1
FROM python:3.13-slim

WORKDIR /usr/local/app

COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .
COPY src ./src
COPY models ./models

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --with ui --no-root

EXPOSE 8000
EXPOSE 8501

CMD ["bash"]
