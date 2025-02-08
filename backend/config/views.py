from django.shortcuts import render
from django.views import View

from categories.models import Category
from posts.services import PostService


class IndexView(View):
    def get(self, request):
        # 현재 선택된 카테고리 가져오기
        category_name = request.GET.get("category", "")
        current_category = None
        if category_name:
            current_category = Category.objects.filter(name=category_name).first()

        # 인기 게시글 (조회수 TOP 10)
        hot_posts = PostService.get_top_posts()

        # 카테고리별 최신글
        category_posts = {}
        for category in Category.objects.all():
            posts = PostService.get_posts_by_category(category)
            if posts.exists():  # 게시글이 있는 카테고리만 표시
                category_posts[category] = posts

        context = {
            "hot_posts": hot_posts,
            "category_posts": category_posts,
            "current_category": current_category,
        }

        return render(request, "index.html", context)
