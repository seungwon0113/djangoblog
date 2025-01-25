from django.db import models
from core.basemodels import BaseModel
from users.models import User
from categories.models import Category
from tags.models import Tag

# Create your models here.


class Post(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "posts"
        verbose_name = "게시글"
        verbose_name_plural = "게시글"
