# backend/Dockerfile

FROM python:3.10-alpine

RUN apk add --no-cache build-base postgresql-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Gunicorn 실행 명령어를 'backend.wsgi:application'에서 'wsgi:application'으로 변경

CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8000"]