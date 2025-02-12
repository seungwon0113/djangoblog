import os

from django.db import models
from django.utils import timezone

from core.basemodels import BaseModel


def carousel_image_path(instance, filename):
    # 파일명에서 확장자 추출
    ext = filename.split(".")[-1]
    # 새로운 파일명 생성 (현재 시간 기준)
    new_filename = f'carousel_{timezone.now().strftime("%Y%m%d_%H%M%S")}.{ext}'
    return os.path.join("carousel", new_filename)


# Create your models here.
class Carousel(BaseModel):
    title = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to=carousel_image_path, null=False, blank=False, verbose_name="이미지"
    )
    link = models.URLField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "carousel"
        verbose_name = "캐러셀"
        verbose_name_plural = "캐러셀"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = os.path.splitext(os.path.basename(self.image.name))[0]
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # 이미지 파일 삭제
        if self.image:
            storage = self.image.storage
            if storage.exists(self.image.name):
                storage.delete(self.image.name)
        super().delete(*args, **kwargs)
