import logging
import os
from uuid import uuid4

from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from categories.models import Category
from comments.services import CommentService
from posts.models import Post
from posts.services import PostService
from tags.models import Tag

logger = logging.getLogger(__name__)


# 게시글 전체조회
class PostListView(View):
    def get(self, request):
        search_query = request.GET.get("search", "")
        category_name = request.GET.get("category", "")

        # 검색 서비스 호출
        posts = PostService.search_posts(search_query, request.user)

        # 카테고리 필터링
        if category_name:
            posts = PostService.filter_posts_by_category(posts, category_name)

        context = {
            "posts": posts,
            "search_query": search_query,
        }

        return render(request, "posts/postlist.html", context)


# 게시글 상세조회
class PostDetailView(View):
    def get(self, request, pk):
        post = PostService.get_post_by_id(pk)

        # 비공개 게시글인 경우 작성자만 접근 가능
        if not post.is_public and (
            not request.user.is_authenticated or request.user != post.author
        ):
            return render(request, "posts/post_forbidden.html", status=403)

        comments = CommentService.get_comments_by_post_id(pk)
        context = {
            "post": post,
            "comments": comments,
        }
        return render(
            request,
            "posts/postdetail.html",
            context,
        )


# 게시글 작성
class PostCreateView(View):
    def get(self, request):
        # 사용자 검증
        if not request.user.is_authenticated:
            return redirect("users:user_login")

        tags = Tag.objects.all()
        # image 파일 업로드 경로 설정
        image_upload_path = os.path.join(settings.MEDIA_ROOT, "images")

        if not os.path.exists(image_upload_path):
            os.makedirs(image_upload_path)

        return render(
            request,
            "posts/postcreate.html",
            {
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

            post = PostService.create_post(
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
            context = {
                "error": str(e),
            }
            return render(
                request,
                "posts/postcreate.html",
                context,
            )


class PostUpdateView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        tags = Tag.objects.all()
        # 사용자 검증
        if not request.user.is_authenticated or request.user != post.author:
            return render(request, "posts/postauthor.html", status=403)

        context = {
            "post": post,
            "tags": tags,
        }
        return render(
            request,
            "posts/postupdate.html",
            context,
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
            context = {
                "post": post,
                "error": str(e),
            }
            return render(
                request,
                "posts/postupdate.html",
                context,
            )


class PostDeleteView(View):
    # 사용자 검증
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("users:user_login")
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("posts:post_list")


class ImageUploadView(View):
    def post(self, request):
        if "image" in request.FILES:
            image = request.FILES["image"]
            # 파일명 중복 방지를 위한 UUID 생성
            ext = os.path.splitext(image.name)[1]
            filename = f"{uuid4().hex}{ext}"

            # 이미지 저장
            image_path = os.path.join(settings.MEDIA_ROOT, "uploads", filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            with open(image_path, "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # 이미지 URL 반환
            image_url = f"/media/uploads/{filename}"
            return JsonResponse({"url": image_url})

        return JsonResponse({"error": "이미지를 찾을 수 없습니다."}, status=400)
