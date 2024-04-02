FROM python:3.11

WORKDIR /app

COPY src/* poetry.lock pyproject.toml ./

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

RUN poetry install --no-root

# For health check
RUN apt-get update && apt-get install -y netcat-traditional
EXPOSE 8080

RUN chmod 700 run.sh

CMD ./run.sh
