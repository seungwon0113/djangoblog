#!/bin/bash

# 데이터베이스 연결 대기
echo "Waiting for database..."
while ! poetry run python manage.py check > /dev/null 2>&1; do
    sleep 1
done

# 마이그레이션 실행
echo "Running migrations..."
poetry run python manage.py migrate

# 서버 시작
echo "Starting server..."
poetry run python manage.py runserver 0.0.0.0:8000