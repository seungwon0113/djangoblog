from django.urls import path

from .views import CarouselView

app_name = "carousel"

urlpatterns = [
    path("create/", CarouselView.as_view(), name="create"),
    path("update_status/", CarouselView.as_view(), name="update_status"),
    path("delete/", CarouselView.as_view(), name="delete"),
]
