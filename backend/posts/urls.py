from django.urls import path

from .views import (
    ImageUploadView,
    PaymentFailView,
    PaymentSuccessView,
    PaymentView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
)

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("upload_image/", ImageUploadView.as_view(), name="upload_image"),
    path("payment/", PaymentView.as_view(), name="payment"),
    path("payment/success/", PaymentSuccessView.as_view(), name="payment_success"),
    path("payment/fail/", PaymentFailView.as_view(), name="payment_fail"),
]
