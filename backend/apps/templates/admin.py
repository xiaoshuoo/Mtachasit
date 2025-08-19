from django.contrib import admin
from .models import GutierrezTemplate


@admin.register(GutierrezTemplate)
class GutierrezTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "updated_at")
    list_filter = ("category",)
    search_fields = ("title", "category", "content")
    ordering = ("-updated_at",)


# Register your models here.
