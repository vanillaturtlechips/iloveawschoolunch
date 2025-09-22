# backend/Dockerfile

FROM python:3.10-alpine

# 빌드에 필요한 도구와 종속성 설치
RUN apk add --no-cache build-base postgresql-dev

# 작업 디렉토리 설정
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app

# Gunicorn을 실행하는 CMD 명령어
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]