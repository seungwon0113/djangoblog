from django.urls import path

from categories.views import CategoryView

app_name = "category"

urlpatterns = [
    path("", CategoryView.as_view(), name="category"),
]
