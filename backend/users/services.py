from users.models import User


class UserService:
    @staticmethod
    def get_user_by_username(username):
        return User.objects.get(username=username)

    @staticmethod
    def create_user(username, password, email, phone, user_image=None):
        return User.objects.create_user(
            username=username,
            password=password,
            email=email,
            phone=phone,
            user_image=user_image,
        )

    @staticmethod
    def update_user(user, **kwargs):
        # 이미지 파일이 있는 경우 기존 이미지 삭제
        if "user_image" in kwargs and kwargs["user_image"] and user.user_image:
            user.user_image.delete()

        for key, value in kwargs.items():
            if value is not None:  # None이 아닌 값만 업데이트
                setattr(user, key, value)
        user.save()
        return user

    @staticmethod
    def delete_user(user):
        user.delete()

    @staticmethod
    def validate_user(user):
        if not user.is_authenticated:
            raise ValueError("사용자가 인증되지 않았습니다.")
        return user
