#!/bin/bash

# 데이터베이스 연결 대기
echo "Waiting for database..."
while ! poetry run python manage.py check > /dev/null 2>&1; do
    sleep 1
done

# 마이그레이션 실행
echo "Running migrations..."
poetry run python manage.py migrate

# 정적 파일 수집
echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

# Gunicorn으로 서버 시작
echo "Starting Gunicorn server..."
poetry run gunicorn --bind 0.0.0.0:8000 config.wsgi:application