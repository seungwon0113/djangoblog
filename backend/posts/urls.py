from django.urls import path
from posts.views import (
    PostListView,
    PostDetailView,
    PostCreateView
    )

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
]
