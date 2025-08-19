from django.db import models
from django.utils.text import slugify


class GutierrezTemplate(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    category = models.CharField(max_length=100, verbose_name="Категория")
    content = models.TextField(verbose_name="Содержание")
    # Доп. поле для импорта из старой БД (нужно для страницы Gutierrez public)
    created_by_id = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Шаблон Gutierrez"
        verbose_name_plural = "Шаблоны Gutierrez"

    def __str__(self) -> str:
        return f"{self.title} ({self.category})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'template'
            unique_slug = base_slug
            suffix = 2
            # Ensure uniqueness by appending -2, -3, ... if needed
            while GutierrezTemplate.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = unique_slug
        else:
            # If slug provided manually, still ensure it's unique when updating title or slug
            base_slug = self.slug
            unique_slug = base_slug
            suffix = 2
            while GutierrezTemplate.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class RossiTemplate(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    category = models.CharField(max_length=100, verbose_name="Категория")
    content = models.TextField(verbose_name="Содержание")
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Шаблон Rossi"
        verbose_name_plural = "Шаблоны Rossi"

    def __str__(self) -> str:
        return f"{self.title} ({self.category})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'template'
            unique_slug = base_slug
            suffix = 2
            while RossiTemplate.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = unique_slug
        else:
            base_slug = self.slug
            unique_slug = base_slug
            suffix = 2
            while RossiTemplate.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

