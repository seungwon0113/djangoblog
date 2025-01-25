from django.shortcuts import render, redirect
from django.views import View
from posts.models import Post
from categories.models import Category
from tags.models import Tag
import os
from django.conf import settings


# 게시글 전체조회
class PostListView(View):
    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")  # 최신글 순으로 정렬
        categories = Category.objects.all()  # 네비게이션 바의 카테고리 목록을 위해 추가
        return render(
            request, "posts/postlist.html", {"posts": posts, "categories": categories}
        )


# 게시글 상세조회
class PostDetailView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        categories = Category.objects.all()  # 네비게이션 바의 카테고리 목록을 위해 추가
        return render(
            request, "posts/postdetail.html", {"post": post, "categories": categories}
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
            post = Post.objects.create(
                title=request.POST["title"],
                content=request.POST["content"],
                author=request.user,
                category=Category.objects.get(name=request.POST["category"]),
            )

            # 이미지가 제공된 경우에만 처리
            if "image" in request.FILES:
                post.image = request.FILES["image"]
                post.save()

            # 태그 처리 (쉼표로 구분된 태그 처리)
            if "tags" in request.POST and request.POST["tags"]:
                tag_names = [tag.strip() for tag in request.POST["tags"].split(",")]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            return redirect("posts:post_list")  # namespace 포함
        except Exception as e:
            # 에러 처리
            categories = Category.objects.all()
            tags = Tag.objects.all()
            return render(
                request,
                "posts/postcreate.html",
                {"categories": categories, "tags": tags, "error": str(e)},
            )
