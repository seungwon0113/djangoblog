#!/bin/bash

domains=(slog.my www.slog.my)
rsa_key_size=4096
data_path="./certbot"
email="jungseungwon0113@gmail.com"
staging=1 # 테스트를 위해 1로 설정

# 필요한 디렉토리 생성
mkdir -p "$data_path/www"
chmod -R 755 "$data_path"

# nginx 컨테이너 재시작
docker compose down
docker compose up -d nginx
sleep 10  # nginx가 완전히 시작될 때까지 대기

# 인증서 발급 시도
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $email \
    --domains ${domains[*]} \
    --staging=$staging \
    --agree-tos \
    --force-renewal \
    --debug-challenges \
    -v

# nginx 재시작
docker compose exec nginx nginx -s reload 