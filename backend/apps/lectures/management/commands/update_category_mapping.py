from django.core.management.base import BaseCommand
from apps.lectures.models import LectureCategory


class Command(BaseCommand):
    help = 'Apply hard-coded mapping for placeholder categories to real names/slugs.'

    def handle(self, *args, **kwargs):
        mapping = {
            '304': ('Для МВД', 'dlya-mvd'),
            '306': ('Первая помощь', 'pervaja-pomosch'),
            '302': ('Заболевания', 'zabolevanija'),
            '305': ('Другое', 'drugoe'),
        }
        updated = 0
        for slug, (name, new_slug) in mapping.items():
            try:
                cat = LectureCategory.objects.get(slug=slug)
            except LectureCategory.DoesNotExist:
                continue
            cat.name = name
            cat.slug = new_slug
            cat.save(update_fields=['name', 'slug'])
            updated += 1
        self.stdout.write(self.style.SUCCESS(f'Updated {updated} categories'))


