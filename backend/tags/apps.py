from django.apps import AppConfig


class TagsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tags"

    def ready(self):
        import tags.signals  # 시그널 등록
