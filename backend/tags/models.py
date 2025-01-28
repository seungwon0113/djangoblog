from django.db import models

from core.basemodels import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tags"
        verbose_name = "태그"
        verbose_name_plural = "태그"
