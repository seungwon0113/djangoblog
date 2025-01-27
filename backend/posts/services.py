from django.db.models import Q

from posts.models import Category, Post, Tag


def get_post_by_id(post_id):
    return Post.objects.get(id=post_id)


# 게시글 생성 로직
def create_post(
    title, content, author, category, image=None, tags=None, is_public=True
):
    # 마크다운을 그대로 저장 (HTML 변환하지 않음)
    post = Post.objects.create(
        title=title,
        content=content,  # 원본 마크다운 텍스트 저장
        author=author,
        category=category,
        image=image,
        is_public=is_public,
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


# 작성자 조회 로직
def get_posts_by_author(search_query):
    return Post.objects.filter(author__username__icontains=search_query).order_by(
        "-created_at"
    )


# 카테고리별 게시글 수 계산
def get_category_post_count(user):
    category_counts = {}
    for category in Category.objects.all():
        count = Post.objects.filter(author=user, category=category).count()
        category_counts[category.id] = count
    return category_counts


# 조회수 증가
def increase_view_count(post):
    post.view_count += 1
    post.save()


# 공개 여부 조회
def get_public_posts():
    return Post.objects.filter(is_public=True)
