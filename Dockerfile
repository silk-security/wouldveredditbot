FROM python:3.11

WORKDIR /app

COPY src/* poetry.lock pyproject.toml ./

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

RUN poetry install --no-root

EXPOSE 8080

CMD ["python", "main.py"]
