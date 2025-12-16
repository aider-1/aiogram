FROM python:3.13-slim

WORKDIR /aiogram2/app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
