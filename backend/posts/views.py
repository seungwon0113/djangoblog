import os

from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View

from categories.models import Category
from comments.services import CommentService
from posts.models import Post
from posts.services import (
    create_post,
    get_post_by_id,
    get_posts_by_author,
    get_posts_by_category,
    get_posts_by_tag,
    get_posts_by_title,
)
from tags.models import Tag


# 게시글 전체조회
class PostListView(View):
    def get(self, request):
        categories = Category.objects.all()
        search_query = request.GET.get("search", "")
        category = request.GET.get("category", "")  # 카테고리 파라미터 추가

        # 기본적으로 최신순 정렬
        posts = Post.objects.all().order_by("-created_at")

        # 카테고리로 필터링
        if category:
            posts = posts.filter(category__name__exact=category)  # 정확한 일치 검색
        # 검색어가 있는 경우 모든 필드에서 검색
        elif search_query:
            posts = (
                Post.objects.filter(
                    Q(title__icontains=search_query)  # 제목 검색
                    | Q(content__icontains=search_query)  # 내용 검색
                    | Q(category__name__icontains=search_query)  # 카테고리 검색
                    | Q(tags__name__icontains=search_query)  # 태그 검색
                    | Q(author__username__icontains=search_query)  # 작성자 검색
                )
                .distinct()
                .order_by("-created_at")
            )

        context = {
            "posts": posts,
            "categories": categories,
            "search_query": search_query,
        }

        return render(request, "posts/postlist.html", context)


# 게시글 상세조회
class PostDetailView(View):
    def get(self, request, pk):
        post = get_post_by_id(pk)
        categories = Category.objects.all()
        comments = CommentService.get_comments_by_post_id(pk)
        return render(
            request,
            "posts/postdetail.html",
            {"post": post, "categories": categories, "comments": comments},
        )


# 게시글 작성
class PostCreateView(View):
    def get(self, request):
        categories = Category.objects.all()
        tags = Tag.objects.all()
        # image 파일 업로드 경로 설정
        image_upload_path = os.path.join(settings.MEDIA_ROOT, "images")
        if not os.path.exists(image_upload_path):
            os.makedirs(image_upload_path)

        return render(
            request,
            "posts/postcreate.html",
            {
                "categories": categories,
                "tags": tags,
                "image_upload_path": image_upload_path,
            },
        )

    def post(self, request):
        try:
            # create_post 서비스 함수 사용
            post = create_post(
                title=request.POST["title"],
                content=request.POST["content"],
                author=request.user,
                category=Category.objects.get(name=request.POST["category"]),
                image=request.FILES.get("image"),
                tags=[
                    tag.strip()
                    for tag in request.POST.get("tags", "").split(",")
                    if tag.strip()
                ],
            )
            return redirect("posts:post_detail", pk=post.pk)
        except Exception as e:
            categories = Category.objects.all()
            tags = Tag.objects.all()
            return render(
                request,
                "posts/postcreate.html",
                {"categories": categories, "tags": tags, "error": str(e)},
            )


class PostUpdateView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        categories = Category.objects.all()
        tags = Tag.objects.all()
        return render(
            request,
            "posts/postupdate.html",
            {
                "post": post,
                "categories": categories,
                "tags": tags,
                "categories": categories,
            },
        )

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.title = request.POST["title"]
            post.content = request.POST["content"]  # 마크다운 원본 저장
            post.category = Category.objects.get(name=request.POST["category"])

            if "image" in request.FILES:
                post.image = request.FILES["image"]

            # 태그 처리
            if "tags" in request.POST:
                post.tags.clear()
                tag_names = [
                    tag.strip()
                    for tag in request.POST["tags"].split(",")
                    if tag.strip()
                ]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            post.save()
            return redirect("posts:post_detail", pk=post.pk)

        except Exception as e:
            categories = Category.objects.all()
            tags = Tag.objects.all()
            return render(
                request,
                "posts/postupdate.html",
                {
                    "post": post,
                    "categories": categories,
                    "tags": tags,
                    "error": str(e),
                },
            )


class PostDeleteView(View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("posts:post_list")
