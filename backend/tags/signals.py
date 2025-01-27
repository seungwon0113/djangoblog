from django.db.models.signals import post_delete
from django.dispatch import receiver

from posts.models import Post
from tags.models import Tag


@receiver(post_delete, sender=Post)
def cleanup_unused_tags(sender, instance, **kwargs):
    # 사용되지 않는 태그 삭제
    Tag.objects.filter(post__isnull=True).delete()
