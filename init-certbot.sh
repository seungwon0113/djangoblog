#!/bin/bash

# certbot 디렉토리 초기화
sudo rm -rf certbot/
sudo mkdir -p certbot/conf
sudo mkdir -p certbot/www
sudo mkdir -p certbot/logs
sudo mkdir -p certbot/work

# 권한 설정
sudo chown -R root:root certbot/
sudo chmod -R 755 certbot/

# nginx 재시작
docker compose down
docker compose up -d nginx

# 잠시 대기
sleep 5

# certbot 실행
docker compose run --rm --entrypoint certbot certbot \
    certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --config-dir=/etc/letsencrypt \
    --work-dir=/var/lib/letsencrypt \
    --logs-dir=/var/log/letsencrypt \
    --email jungseungwon0113@gmail.com \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    --staging \
    --non-interactive \
    -v \
    -d slog.my -d www.slog.my

# 인증서 발급 확인
sudo ls -la certbot/conf/live/ 