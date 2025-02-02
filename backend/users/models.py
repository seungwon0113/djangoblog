from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from core.basemodels import BaseModel


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("이름은 필수 입력 항목입니다.")
        if not email:
            raise ValueError("이메일은 필수 입력 항목입니다.")

        user = self.model(
            username=username, email=self.normalize_email(email), **extra_fields
        )

        # 소셜 로그인의 경우 password가 None일 수 있음
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("email", f"{username}@example.com")
        return self.create_user(
            username, extra_fields.pop("email"), password, **extra_fields
        )


class User(BaseModel, AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # 기존 필드들
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    user_image = models.ImageField(upload_to="user_images/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @classmethod
    def create_user(cls, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("사용자 이름은 필수 입력 항목입니다.")
        if not email:
            raise ValueError("이메일은 필수 입력 항목입니다.")

        user = cls(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user
