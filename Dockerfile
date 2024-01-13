FROM python:3.12.1

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY pyproject.toml /code/
COPY /src /code

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction
