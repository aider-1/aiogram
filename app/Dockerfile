FROM python:3.13

WORKDIR /aiogram/app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
