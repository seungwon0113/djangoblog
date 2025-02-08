from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from categories.models import Category
from categories.services import CategoryService


class CategoryView(View):
    def get(self, request):
        # staff나 superuser가 아니면 메인으로 리다이렉트
        if not CategoryService.is_staff_superuser(request.user):
            messages.error(request, "접근 권한이 없습니다.")
            return redirect("index")
        return render(request, "category/category.html")

    def post(self, request):
        # staff나 superuser가 아니면 메인으로 리다이렉트
        if not CategoryService.is_staff_superuser(request.user):
            messages.error(request, "접근 권한이 없습니다.")
            return redirect("index")

        action = request.POST.get("action")

        try:
            # 생성
            if action == "create":
                name = request.POST.get("name")
                CategoryService.create_category(name)
                messages.success(request, "카테고리가 생성되었습니다.")

            # 수정
            elif action == "update":
                category_id = request.POST.get("category_id")
                name = request.POST.get("name")
                category = Category.objects.get(pk=category_id)
                CategoryService.update_category(category, name)
                messages.success(request, "카테고리가 수정되었습니다.")

            # 삭제
            elif action == "delete":
                category_id = request.POST.get("category_id")
                category = Category.objects.get(pk=category_id)
                category.delete()
                messages.success(request, "카테고리가 삭제되었습니다.")

            else:
                messages.error(request, "잘못된 요청입니다.")

        except Exception as e:
            messages.error(request, f"오류가 발생했습니다: {str(e)}")

        return redirect("category:category")
