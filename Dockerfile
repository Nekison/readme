FROM python:3

WORKDIR /app

RUN pip install pipenv

COPY Pipfile /app/
COPY Pipfile.lock /app/

RUN pipenv install --system
