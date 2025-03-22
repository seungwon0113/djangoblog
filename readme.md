# Slog (개인블로그)

<div align="center">

  <h3>📋 Slog Link</h3>
  <p>
  </p>
   <a href="https://slog.my" target="_blank">
    <img src="https://img.shields.io/badge/배포 링크-8867DF?style=for-the-badge">
  </a>
</div>

---
<div align="center">
<h3>👩🏻‍💻 Stack 👩🏻‍💻</h3>
<a href="https://www.djangoproject.com/">
  <img src="https://img.shields.io/badge/django-009688?style=for-the-badge&logo=django&logoColor=white">
</a>
<a href="https://www.postgresql.org/">
  <img src="https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white">
</a>
<a href="https://www.docker.com/">
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
</a>
<a href="https://www.python.org/">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
</a>
<a href="https://uvicorn.org/">
  <img src="https://img.shields.io/badge/uvicorn-009688?style=for-the-badge&logo=uvicorn&logoColor=white">
</a>
<a href="https://www.nginx.com/">
  <img src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white">
</a>
<a href="https://www.ncloud.com/">
  <img src="https://img.shields.io/badge/NAVER%20CLOUD-%03C75A.svg?style=for-the-badge&logo=NAVER&logoColor=white">
</a>
</div>


## 프로젝트 구성

```
slog/
 ├── backend/ # Django 백엔드
 │       ├── users/ # 사용자 관리
 │       ├── posts/ # 게시글 관리
 │       ├── comments/ # 댓글 관리
 │       ├── likes/ # 좋아요 관리
 │       ├── tags/ # 태그 관리
 │       ├── categories/ # 카테고리 관리
 │       └── contact/ # 이메일 발송
 │       
 ├── nginx/ # Nginx 설정
 ├── certbot/ # SSL 인증서
 ├── docker-compose.yml # 운영 환경 설정
 └── docker-compose.dev.yml # 개발 환경 설정
```

## docker compose
```bash
# 운영 환경 실행
docker compose -f docker-compose.yml up -d
# 개발 환경 실행
docker compose -f docker-compose.dev.yml up -d

# 운영 환경 로그 확인
docker compose logs -f
# 개발 환경 로그 확인
docker compose -f docker-compose.dev.yml logs -f
``` 

## 기능
- 유저 회원가입, 로그인, 로그아웃

- 게시글 작성, 수정, 삭제

- 태그 추가 기능

- 댓글 작성, 수정, 삭제

- 좋아요 기능

- 토스 테스트 결제 기능

- 문의 하기 >> 관리자 이메일

- 카테고리 관리 기능 (관리자)
