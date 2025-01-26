from django.db import models

from categories.models import Category
from core.basemodels import BaseModel
from tags.models import Tag
from users.models import User

# Create your models here.


class Post(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "posts"
        verbose_name = "게시글"
        verbose_name_plural = "게시글"
