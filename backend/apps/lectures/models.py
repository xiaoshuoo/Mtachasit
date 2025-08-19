from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class LectureCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(max_length=50, default="fas fa-folder", verbose_name="Иконка")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категория лекций"
        verbose_name_plural = "Категории лекций"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or 'category'
            unique = base
            i = 2
            while LectureCategory.objects.filter(slug=unique).exclude(pk=self.pk).exists():
                unique = f"{base}-{i}"
                i += 1
            self.slug = unique
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название лекции")
    content = models.TextField(verbose_name="Содержание лекции")
    category = models.ForeignKey(
        LectureCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lectures',
        verbose_name="Категория",
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Лекция"
        verbose_name_plural = "Лекции"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:lecture_detail', kwargs={'pk': self.pk})

    def get_lines(self):
        return [line.strip() for line in self.content.split('\n') if line.strip()]


