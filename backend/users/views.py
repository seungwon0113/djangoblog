from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View

from categories.models import Category
from posts.services import get_category_post_count
from users.services import UserService


# user_profile View
class UserProfileView(LoginRequiredMixin, View):
    login_url = "/users/login/"  # 로그인이 필요할 때 리다이렉트할 URL
    redirect_field_name = "next"  # 로그인 후 원래 페이지로 돌아가기 위한 파라미터 이름

    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return render(
                    request,
                    "users/login.html",
                    {
                        "error": "로그인 후 이용해주세요.",
                        "next": request.path,  # 로그인 후 돌아올 페이지 저장
                    },
                )

            user = UserService.get_user_by_username(request.user.username)
            categories = Category.objects.all()
            # 카테고리별 게시글 수 계산
            category_post_count = get_category_post_count(user)
            return render(
                request,
                "users/profile.html",
                {
                    "user": user,
                    "user_image": user.user_image,
                    "categories": categories,
                    "category_post_count": category_post_count,
                },
            )
        except Exception as e:
            return render(request, "users/login.html", {"error": str(e)})


# user_signup View
class UserSignupView(View):
    def get(self, request):
        return render(request, "users/signup.html")

    def post(self, request):
        try:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            # 비밀번호 확인
            if password1 != password2:
                raise ValueError("비밀번호가 일치하지 않습니다.")

            # 사용자 생성
            user = UserService.create_user(
                username=username,
                password=password1,  # password1을 password로 전달
                email=email,
            )

            # 로그인 처리
            auth_login(request, user)
            return redirect("index")

        except Exception as e:
            return render(request, "users/signup.html", {"error": str(e)})


# user_update View
class UserUpdateView(View):
    def post(self, request):
        try:
            # 이미지 파일이 있는 경우에만 처리
            user_image = request.FILES.get("user_image")

            user = UserService.update_user(
                request.user,
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                user_image=user_image if user_image else request.user.user_image,
            )
            return redirect("users:user_profile")
        except Exception as e:
            messages.error(request, str(e))
            return redirect("users:user_profile")


# user_login View
class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("posts:post_list")
        return render(request, "users/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # next 파라미터가 있으면 해당 URL로 리다이렉트
                next_url = request.GET.get("next") or request.POST.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("posts:post_list")
            else:
                messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
        except Exception as e:
            messages.error(request, str(e))

        return render(request, "users/login.html")


class UserLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("index")
