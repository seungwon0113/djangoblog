import logging
import os

from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View

from categories.models import Category
from comments.services import CommentService
from posts.models import Post
from posts.services import create_post, get_post_by_id, get_public_posts
from tags.models import Tag

logger = logging.getLogger(__name__)


# 게시글 전체조회
class PostListView(View):
    def get(self, request):
        categories = Category.objects.all()
        search_query = request.GET.get("search", "")
        category = request.GET.get("category", "")

        # 로그인한 사용자의 경우 자신의 비공개 게시글도 표시
        if request.user.is_authenticated:
            posts = Post.objects.filter(
                Q(is_public=True) | Q(author=request.user)
            ).order_by("-created_at")
        else:
            # 비로그인 사용자는 공개 게시글만 표시
            posts = Post.objects.filter(is_public=True).order_by("-created_at")

        # 카테고리로 필터링
        if category:
            posts = posts.filter(category__name__exact=category)
        # 검색어가 있는 경우 모든 필드에서 검색
        elif search_query:
            posts = posts.filter(
                Q(title__icontains=search_query)  # 제목 검색
                | Q(content__icontains=search_query)  # 내용 검색
                | Q(category__name__icontains=search_query)  # 카테고리 검색
                | Q(tags__name__icontains=search_query)  # 태그 검색
                | Q(author__username__icontains=search_query)  # 작성자 검색
            ).distinct()

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

        # 비공개 게시글인 경우 작성자만 접근 가능
        if not post.is_public and (
            not request.user.is_authenticated or request.user != post.author
        ):
            return render(request, "posts/post_forbidden.html", status=403)

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
        # 사용자 검증
        if not request.user.is_authenticated:
            return redirect("users:user_login")

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
            logger.info(f"POST Data: {request.POST}")  # 전체 POST 데이터 로깅

            tags = [
                tag.strip().lstrip("#")
                for tag in request.POST.get("tags", "").split(",")
                if tag.strip()
            ]

            # is_public 값 처리
            is_public = request.POST.get("is_public") == "true"
            logger.info(f"Create - is_public value: {is_public}")

            post = create_post(
                title=request.POST["title"],
                content=request.POST["content"],
                author=request.user,
                category=Category.objects.get(name=request.POST["category"]),
                image=request.FILES.get("image"),
                tags=tags,
                is_public=is_public,
            )
            return redirect("posts:post_detail", pk=post.pk)
        except Exception as e:
            categories = Category.objects.all()
            return render(
                request,
                "posts/postcreate.html",
                {"categories": categories, "error": str(e)},
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
            logger.info(f"UPDATE - POST Data: {request.POST}")  # 전체 POST 데이터 로깅

            post = Post.objects.get(pk=pk)
            post.title = request.POST["title"]
            post.content = request.POST["content"]
            post.category = Category.objects.get(name=request.POST["category"])

            # is_public 값 처리
            post.is_public = request.POST.get("is_public") == "true"
            logger.info(f"Update - is_public value: {post.is_public}")

            if "image" in request.FILES:
                post.image = request.FILES["image"]

            # 태그 처리
            if "tags" in request.POST:
                post.tags.clear()
                tag_names = [
                    tag.strip().replace("#", "")
                    for tag in request.POST["tags"].split(",")
                    if tag.strip().replace("#", "")
                ]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            post.save()
            return redirect("posts:post_detail", pk=post.pk)

        except Exception as e:
            categories = Category.objects.all()
            return render(
                request,
                "posts/postupdate.html",
                {
                    "post": post,
                    "categories": categories,
                    "error": str(e),
                },
            )


class PostDeleteView(View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("posts:post_list")
