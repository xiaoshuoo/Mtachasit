from django.contrib import admin
from .models import Lecture, LectureCategory


@admin.register(LectureCategory)
class LectureCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "is_active", "created_at")
    list_filter = ("is_active", "category")
    search_fields = ("title", "content")


