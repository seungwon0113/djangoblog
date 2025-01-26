from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from comments.models import Comment
from comments.services import CommentService
from posts.services import get_post_by_id


class CommentListView(View):
    def get(self, request, post_id):
        comments = CommentService.get_comments_by_post_id(post_id)
        return render(request, "posts/postdetail.html", {"comments": comments})


class CommentCreateView(View):
    def post(self, request, post_id):
        try:
            content = request.POST.get("content")
            if not content:
                raise ValueError("댓글 내용을 입력해주세요.")

            if not request.user.is_authenticated:
                raise ValueError("로그인이 필요한 서비스입니다.")

            CommentService.create_comment(
                post_id=post_id, content=content, author=request.user
            )
            return redirect("posts:post_detail", pk=post_id)
        except Exception as e:
            return render(
                request,
                "posts/postdetail.html",
                {"post": get_post_by_id(post_id), "error": str(e)},
            )


class CommentUpdateView(View):
    def post(self, request, pk):
        try:
            content = request.POST.get("content")
            if not content:
                raise ValueError("댓글 내용을 입력해주세요.")

            comment = CommentService.update_comment(comment_id=pk, content=content)
            return redirect("posts:post_detail", pk=comment.post.id)
        except Exception as e:
            return render(request, "posts/postdetail.html", {"error": str(e)})


class CommentDeleteView(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        post_id = comment.post.id
        CommentService.delete_comment(pk)
        return redirect("posts:post_detail", pk=post_id)


# 대댓글 작성
