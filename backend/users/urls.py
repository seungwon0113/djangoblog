from django.urls import path

from users.views import (
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserSignupView,
    UserUpdateView,
)

app_name = "users"

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("signup/", UserSignupView.as_view(), name="user_signup"),
    path("update/", UserUpdateView.as_view(), name="user_update"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
]
