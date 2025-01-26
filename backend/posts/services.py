import markdown
from django.db.models import Q

from posts.models import Post, Tag


def get_post_by_id(post_id):
    return Post.objects.get(id=post_id)


# 게시글 생성 로직
def create_post(title, content, author, category, image=None, tags=None):
    # 마크다운을 그대로 저장 (HTML 변환하지 않음)
    post = Post.objects.create(
        title=title,
        content=content,  # 원본 마크다운 텍스트 저장
        author=author,
        category=category,
        image=image,
    )

    # 태그 처리
    tag_objects = []
    if tags:
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)

    if tag_objects:
        post.tags.set(tag_objects)

    return post


# 게시글 조회 로직
def get_posts_by_title(search_query):
    return Post.objects.filter(
        Q(title__icontains=search_query) | Q(content__icontains=search_query)
    ).order_by("-created_at")


# 사용자 조회 로직
def get_posts_by_author(search_query):
    return Post.objects.filter(author__username__icontains=search_query).order_by(
        "-created_at"
    )


# 카테고리 조회 로직
def get_posts_by_category(search_query):
    return Post.objects.filter(category__name__icontains=search_query).order_by(
        "-created_at"
    )


# 태그 조회 로직
def get_posts_by_tag(search_query):
    return (
        Post.objects.filter(tags__name__icontains=search_query)
        .order_by("-created_at")
        .distinct()
    )


# 작성자 조회 로직
def get_posts_by_author(search_query):
    return Post.objects.filter(author__username__icontains=search_query).order_by(
        "-created_at"
    )
