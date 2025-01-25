from django.shortcuts import render, redirect
from django.views import View
from posts.models import Post
from categories.models import Category
from tags.models import Tag


# 게시글 전체조회
class PostListView(View):
    def get(self, request):
        posts = Post.objects.all()
        categories = Category.objects.all()
        tags = Tag.objects.all()
        return render(
            request,
            "posts/postlist.html",
            {"posts": posts, "categories": categories, "tags": tags},
        )


# 게시글 상세조회
class PostDetailView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        return render(request, "posts/postdetail.html", {"post": post})


# 게시글 작성
class PostCreateView(View):
    def get(self, request):
        categories = Category.objects.all()
        tags = Tag.objects.all()
        return render(
            request, "posts/postcreate.html", {"categories": categories, "tags": tags}
        )

    def post(self, request):
        post = Post.objects.create(
            title=request.POST["title"],
            content=request.POST["content"],
            author=request.user,
            category=Category.objects.get(name=request.POST["category"]),
        )
        return redirect("post_list")
