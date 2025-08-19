import csv
from pathlib import Path
from typing import Optional
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.lectures.models import Lecture, LectureCategory


class Command(BaseCommand):
    help = "Import categories and lectures from CSV files (UTF-8, with headers)."

    def add_arguments(self, parser):
        parser.add_argument('--categories', type=str, help='Path to categories CSV (id,name,slug)')
        parser.add_argument('--lectures', type=str, required=True, help='Path to lectures CSV (title,content,category_id)')
        parser.add_argument('--delimiter', default=',')

    def handle(self, *args, **opts):
        delim = opts['delimiter']
        cat_path = opts.get('categories')
        lec_path = opts['lectures']

        id_map: dict[str, int] = {}

        if cat_path:
            p = Path(cat_path)
            if not p.exists():
                raise CommandError(f'Categories CSV not found: {p}')
            with p.open('r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f, delimiter=delim)
                with transaction.atomic():
                    for row in reader:
                        src_id = (row.get('id') or row.get('pk') or '').strip()
                        name = (row.get('name') or '').strip()
                        slug = (row.get('slug') or name.lower().replace(' ', '-')).strip()
                        if not name:
                            name = slug or src_id or 'Категория'
                        cat, _ = LectureCategory.objects.get_or_create(slug=slug or src_id, defaults={'name': name})
                        if src_id:
                            id_map[src_id] = cat.id

        p = Path(lec_path)
        if not p.exists():
            raise CommandError(f'Lectures CSV not found: {p}')

        created = 0
        with p.open('r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f, delimiter=delim)
            with transaction.atomic():
                for row in reader:
                    title = (row.get('title') or row.get('name') or 'Без названия').strip()
                    content = row.get('content') or row.get('text') or ''
                    cat_fk = row.get('category_id') or row.get('category') or ''
                    category_id: Optional[int] = None
                    if cat_fk:
                        category_id = id_map.get(cat_fk)
                    Lecture.objects.create(title=title, content=content, category_id=category_id)
                    created += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {created} lectures'))


