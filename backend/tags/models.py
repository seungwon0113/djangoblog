from django.db import models
from core.basemodels import BaseModel
from categories.models import Category

class Tag(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'tags'
        verbose_name = '태그'
        verbose_name_plural = '태그'
