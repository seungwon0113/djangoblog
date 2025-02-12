from django.conf import settings
from django.db import models
from django.db.models import Count
from django.shortcuts import render
from django.views import View

from carousel.models import Carousel
from categories.models import Category
from posts.models import Post


class IndexView(View):
    def get(self, request):
        # 활성화된 캐러셀 이미지
        carousel_images = Carousel.objects.filter(is_active=True).order_by(
            "-created_at"
        )

        # 인기 게시글 (조회수 기준 상위 5개)
        hot_posts = Post.objects.filter(is_public=True).order_by(
            "-view_count", "-created_at"
        )[:5]

        # 카테고리별 최신글
        category_posts = {}
        categories = Category.objects.annotate(
            post_count=Count("post", filter=models.Q(post__is_public=True))
        ).filter(post_count__gt=0)

        for category in categories:
            posts = Post.objects.filter(category=category, is_public=True).order_by(
                "-created_at"
            )[:5]
            if posts.exists():
                category_posts[category] = posts

        context = {
            "carousel_images": carousel_images,
            "debug_info": {
                "media_root": settings.MEDIA_ROOT,
                "media_url": settings.MEDIA_URL,
            },
            "hot_posts": hot_posts,
            "category_posts": category_posts,
        }

        # 디버깅을 위한 출력
        print("Hot Posts Count:", hot_posts.count())
        for post in hot_posts:
            print(
                f"Post: {post.title}, Image: {post.image if post.image else 'No Image'}"
            )

        return render(request, "index.html", context)
