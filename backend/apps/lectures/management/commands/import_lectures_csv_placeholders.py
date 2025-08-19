import csv
from pathlib import Path
from typing import Optional
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.lectures.models import Lecture, LectureCategory


class Command(BaseCommand):
    help = "Import lectures from CSV and auto-create placeholder categories by category_id."

    def add_arguments(self, parser):
        parser.add_argument('--lectures', type=str, required=True, help='Path to lectures CSV (title,content,category_id)')
        parser.add_argument('--delimiter', default=',')
        parser.add_argument('--truncate', action='store_true', help='Delete existing lectures before import')

    def handle(self, *args, **opts):
        p = Path(opts['lectures'])
        if not p.exists():
            raise CommandError(f'Lectures CSV not found: {p}')
        delim = opts['delimiter']

        if opts['truncate']:
            Lecture.objects.all().delete()

        created = 0
        with p.open('r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f, delimiter=delim)
            with transaction.atomic():
                for row in reader:
                    title = (row.get('title') or row.get('name') or 'Без названия').strip()
                    content = row.get('content') or row.get('text') or ''
                    raw_cat = row.get('category_id') or row.get('category') or ''
                    category_id: Optional[int] = None
                    if raw_cat:
                        slug = str(raw_cat).strip()
                        name = f'Категория {slug}'
                        cat, _ = LectureCategory.objects.get_or_create(slug=slug, defaults={'name': name})
                        category_id = cat.id
                    Lecture.objects.create(title=title, content=content, category_id=category_id)
                    created += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {created} lectures with placeholder categories'))


