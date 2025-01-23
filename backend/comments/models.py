from django.db import models
from core.basemodels import BaseModel
from users.models import User
from posts.models import Post

class Comment(BaseModel):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20] + '...'
    
    class Meta:
        db_table = 'comments'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
