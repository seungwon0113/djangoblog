from django.shortcuts import render
from django.views import View

from carousel.models import Carousel


class IndexView(View):
    def get(self, request):
        # 활성화된 캐러셀 이미지만 가져오기
        carousel_images = Carousel.objects.filter(is_active=True).order_by(
            "-created_at"
        )

        context = {
            "carousel_images": carousel_images,
        }

        return render(request, "index.html", context)
