from django.db.models import Q

from posts.models import Category, Post, Tag


class PostService:
    @staticmethod
    def get_post_by_id(post_id):
        return Post.objects.get(id=post_id)

    @staticmethod
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

    @staticmethod
    def get_posts_by_author(search_query):
        return Post.objects.filter(author__username__icontains=search_query).order_by(
            "-created_at"
        )

    @staticmethod
    def get_category_post_count(user):
        category_counts = {}
        for category in Category.objects.all():
            count = Post.objects.filter(author=user, category=category).count()
            category_counts[category.id] = count
        return category_counts

    @staticmethod
    def increase_view_count(post):
        post.view_count += 1
        post.save()

    @staticmethod
    def get_public_posts():
        return Post.objects.filter(is_public=True)

    @staticmethod
    def search_posts(search_query, user=None):
        if user and user.is_authenticated:
            posts = Post.objects.filter(Q(is_public=True) | Q(author=user)).order_by(
                "-created_at"
            )
        else:
            posts = Post.objects.filter(is_public=True).order_by("-created_at")

        # 검색어가 있는 경우 필터링
        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query)  # 제목 검색
                | Q(content__icontains=search_query)  # 내용 검색
                | Q(category__name__icontains=search_query)  # 카테고리 검색
                | Q(tags__name__icontains=search_query)  # 태그 검색
                | Q(author__nickname__icontains=search_query)  # 작성자 검색
            ).distinct()

        return posts

    @staticmethod
    def filter_posts_by_category(posts, category_name):
        if category_name:
            return posts.filter(category__name__exact=category_name)
        return posts