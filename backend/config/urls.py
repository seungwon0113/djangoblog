from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from .views import IndexView  # 수정

app_name = "config"


def index(request):
    return render(request, "index.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("example/", include("example.urls")),
    path("", IndexView.as_view(), name="index"),  # 수정
    path("", RedirectView.as_view(url="/example/")),
    path("users/", include("users.urls", namespace="users")),
    path("posts/", include("posts.urls", namespace="posts")),
    path("comments/", include("comments.urls", namespace="comments")),
    path("contacts/", include("contacts.urls", namespace="contacts")),
    path("category/", include("categories.urls", namespace="category")),
    path("carousel/", include("carousel.urls", namespace="carousel")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 개발 환경에서 media 파일 서빙을 위한 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
