FROM python:3.13

WORKDIR /aiogram

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY app ./app

CMD ["sh", "-c", "alembic revision --autogenerate && alembic upgrade head && python -m app"]
