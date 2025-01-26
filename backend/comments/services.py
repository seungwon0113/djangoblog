from django.shortcuts import get_object_or_404

from comments.models import Comment


class CommentService:
    # 게시글 댓글 조회
    @staticmethod
    def get_comments_by_post_id(post_id):
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")

    # 댓글 생성
    @staticmethod
    def create_comment(post_id, content, author):
        return Comment.objects.create(post_id=post_id, content=content, author=author)

    # 댓글 수정
    @staticmethod
    def update_comment(comment_id, content):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.content = content
        comment.save()
        return comment

    # 댓글 삭제
    @staticmethod
    def delete_comment(comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
