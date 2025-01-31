#!/bin/bash
# 인증서 갱신
docker compose run --rm certbot renew
# nginx 재시작
docker compose exec nginx nginx -s reload 
