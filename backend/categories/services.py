from typing import List

from categories.models import Category


class CategoryService:
    @staticmethod
    def get_all_categories() -> List[Category]:
        return Category.objects.all()

    @staticmethod
    def create_category(name: str) -> Category:
        if not name:
            raise ValueError("카테고리 이름은 필수입니다.")

        return Category.objects.create(name=name)

    @staticmethod
    def update_category(category: Category, name: str) -> Category:
        if not name:
            raise ValueError("카테고리 이름은 필수입니다.")

        category.name = name
        category.save()
        return category

    @staticmethod
    def delete_category(category: Category) -> None:
        category.delete()

    @staticmethod
    def is_staff_superuser(user) -> bool:
        if not user.is_authenticated:
            return False
        return user.is_staff or user.is_superuser

    @staticmethod
    def get_category_by_id(category_id: int) -> Category:
        return Category.objects.get(pk=category_id)
