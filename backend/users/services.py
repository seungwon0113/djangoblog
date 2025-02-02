from users.models import User


class UserService:
    @staticmethod
    def get_user_by_username(username):
        return User.objects.get(username=username)

    @staticmethod
    def check_email_exists(email):
        return User.objects.filter(email=email).exists()

    @staticmethod
    def check_username_exists(username):
        return User.objects.filter(username=username).exists()

    @staticmethod
    def create_user(username, password, email, phone=None, user_image=None):
        # 소셜로그인 예외 처리

        if UserService.check_username_exists(username):
            raise ValueError("이미 사용 중인 아이디입니다.")
        if UserService.check_email_exists(email):
            raise ValueError("이미 사용 중인 이메일입니다.")

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

    @staticmethod
    def get_or_create_google_user(email, user_data):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            username = f"google_{user_data.get('id')}"
            user = User.objects.create_user(
                username=username,
                email=email,
                password=None,  # 소셜 로그인은 비밀번호 불필요
            )
        return user

    @staticmethod
    def create_google_user(email, username):
        """구글 로그인 사용자 생성"""
        user = User.objects.create_user(
            email=email,
            username=username,
        )
        return user
