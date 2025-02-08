from django.db.models import Count

from categories.models import Category
from posts.services import PostService


def categories(request):
    # 현재 선택된 카테고리 정보
    category_name = request.GET.get("category", "")
    current_category = None
    if category_name:
        current_category = Category.objects.filter(name=category_name).first()

    # 카테고리 목록과 각 카테고리별 게시글 수
    categories = Category.objects.all()
    for category in categories:
        category.post_count = PostService.get_total_posts_by_category(category)

    # 전체 공개 게시글 수
    total_posts = PostService.get_total_posts()

    return {
        "categories": categories,
        "total_posts": total_posts,
        "current_category": current_category,
    }
