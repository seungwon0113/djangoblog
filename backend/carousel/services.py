from .models import Carousel


class CarouselService:
    @staticmethod
    def get_carousel_images():
        # 활성화된 모든 캐러셀 이미지 조회
        return Carousel.objects.all()

    @staticmethod
    def get_carousel_image(carousel_id):
        # 단일 캐러셀 이미지 조회
        return Carousel.objects.get(id=carousel_id)

    @staticmethod
    def create_carousel_image(title, image, link=None, is_active=True):
        # 새로운 캐러셀 이미지 생성
        return Carousel.objects.create(
            title=title, image=image, link=link, is_active=is_active
        )

    @staticmethod
    def delete_carousel_image(carousel_id):
        # 캐러셀 이미지 삭제
        carousel = Carousel.objects.get(id=carousel_id)
        carousel.delete()

    @staticmethod
    def toggle_status(carousel_id):
        # 캐러셀 이미지 활성화 상태 토글
        carousel = Carousel.objects.get(id=carousel_id)
        carousel.is_active = not carousel.is_active
        carousel.save()
        return carousel
