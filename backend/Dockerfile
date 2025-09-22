# backend/Dockerfile

FROM python:3.10-alpine

RUN apk add --no-cache build-base postgresql-dev

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]