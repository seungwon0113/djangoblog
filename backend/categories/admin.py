from django.contrib import admin

from categories.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


admin.site.register(Category, CategoryAdmin)
