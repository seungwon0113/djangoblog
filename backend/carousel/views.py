import json

from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View

from .models import Carousel
from .services import CarouselService


class CarouselView(View):
    def handle_json_response(self, success=True, message=None, status=200):
        response = {"status": "success" if success else "error"}
        if message:
            response["message"] = message
        return JsonResponse(response, status=status)

    def post(self, request):
        try:
            if request.path == "/carousel/create/":
                return self.handle_create(request)
            elif request.path == "/carousel/update_status/":
                return self.handle_status_update(request)
            elif request.path == "/carousel/delete/":
                return self.handle_delete(request)
        except Exception as e:
            print(f"Error in carousel view: {str(e)}")
            if request.path in ["/carousel/delete/", "/carousel/update_status/"]:
                return self.handle_json_response(False, str(e), 400)
            messages.error(request, f"오류가 발생했습니다: {str(e)}")

        return redirect("category:category")

    def handle_create(self, request):
        image = request.FILES.get("image")
        if not image:
            raise ValueError("이미지 파일이 필요합니다.")

        print(f"Received image: {image.name} ({image.content_type})")

        # 이미지 저장
        carousel = CarouselService.create_carousel_image(
            title=request.POST.get("title"),
            image=image,
            link=request.POST.get("link"),
            is_active=True,
        )

        print(f"Saved image at: {carousel.image.path}")
        print(f"Image URL: {carousel.image.url}")

        messages.success(request, "캐러셀 이미지가 추가되었습니다.")
        return redirect("category:category")

    def handle_status_update(self, request):
        data = json.loads(request.body)
        carousel_id = data.get("id")
        CarouselService.toggle_status(carousel_id)
        return self.handle_json_response()

    def handle_delete(self, request):
        data = json.loads(request.body)
        carousel_id = data.get("id")
        if not carousel_id:
            raise ValueError("캐러셀 ID가 필요합니다.")

        carousel = Carousel.objects.get(id=carousel_id)
        # 이미지 파일 삭제
        if carousel.image:
            default_storage.delete(carousel.image.name)
        carousel.delete()
        return self.handle_json_response()
