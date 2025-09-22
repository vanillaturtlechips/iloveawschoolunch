# backend/Dockerfile

FROM python:3.10-alpine
RUN apk add --no-cache build-base postgresql-dev
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# backend 폴더 전체를 /app/backend/로 복사
COPY . /app/backend/
# Django 프로젝트의 루트 디렉터리를 Pythonpath에 추가
ENV PYTHONPATH=/app:$PYTHONPATH
# gunicorn은 backend 폴더 내 wsgi를 참조
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]