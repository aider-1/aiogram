FROM python:3.13-slim

WORKDIR /aiogram2/app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
