from users.models import User

class UserService:
    @staticmethod
    def get_user_by_username(username):
        return User.objects.get(username=username)

    @staticmethod
    def create_user(username, password, email):
        return User.objects.create_user(username=username, password=password, email=email)
    
    @staticmethod
    def update_user(user, **kwargs):
        for key, value in kwargs.items():
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