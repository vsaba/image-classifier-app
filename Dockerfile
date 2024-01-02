# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

ENV GMAIL_PASSKEY="ahafdezfpkvdkgeo"

ENV CONFIGURATION_OBJECT="config.Production"

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD flask --app flaskr run --host=0.0.0.0
