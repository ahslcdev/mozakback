# syntax=docker/dockerfile:1
FROM python:3.11-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
	&& apt-get upgrade -y \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/static /app/media
# RUN python manage.py collectstatic --noinput