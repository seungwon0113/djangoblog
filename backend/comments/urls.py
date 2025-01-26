from django.urls import path

from .views import (
    CommentCreateView,
    CommentDeleteView,
    CommentListView,
    CommentUpdateView,
)

app_name = "comments"

urlpatterns = [
    path("<int:post_id>/", CommentListView.as_view(), name="comment_list"),
    path("<int:post_id>/create/", CommentCreateView.as_view(), name="comment_create"),
    path("<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),
    path("<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
]
