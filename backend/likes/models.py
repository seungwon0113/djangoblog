from django.db import models

from core.basemodels import BaseModel
from posts.models import Post
from users.models import User


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}님이 {self.post.title}을(를) 좋아합니다."

    class Meta:
        db_table = "likes"
        verbose_name = "좋아요"
        verbose_name_plural = "좋아요"
