import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.lectures.models import Lecture, LectureCategory


class Command(BaseCommand):
    help = 'Import lectures from JSON file (array of objects) with fields: title, content, (optional) category|category_id|category_slug.'

    def add_arguments(self, parser):
        parser.add_argument('json_path', type=str)
        parser.add_argument('--title', default='title')
        parser.add_argument('--content', default='content')
        parser.add_argument('--cat', default='category')
        parser.add_argument('--cat_id', default='category_id')
        parser.add_argument('--cat_slug', default='category_slug')

    def handle(self, *args, **opts):
        p = Path(opts['json_path'])
        if not p.exists():
            raise CommandError(f'File not found: {p}')
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:
            raise CommandError(f'Invalid JSON: {e}')
        if not isinstance(data, list):
            raise CommandError('JSON root must be an array')

        title_f = opts['title']
        content_f = opts['content']
        cat_name_f = opts['cat']
        cat_id_f = opts['cat_id']
        cat_slug_f = opts['cat_slug']

        created = 0
        with transaction.atomic():
            for obj in data:
                title = (obj.get(title_f) or '').strip() or 'Без названия'
                content = obj.get(content_f) or ''
                category_id = None

                # Try id
                src_id = obj.get(cat_id_f)
                if isinstance(src_id, int):
                    # We don't have mapping, so import/ensure by slug derived from id
                    cat, _ = LectureCategory.objects.get_or_create(slug=str(src_id), defaults={'name': str(src_id)})
                    category_id = cat.id

                # Try slug
                if category_id is None and obj.get(cat_slug_f):
                    slug = str(obj.get(cat_slug_f)).lower()
                    cat, _ = LectureCategory.objects.get_or_create(slug=slug, defaults={'name': slug})
                    category_id = cat.id

                # Try name
                if category_id is None and obj.get(cat_name_f):
                    name = str(obj.get(cat_name_f))
                    slug = name.lower().replace(' ', '-')
                    cat, _ = LectureCategory.objects.get_or_create(slug=slug, defaults={'name': name})
                    category_id = cat.id

                Lecture.objects.create(title=title, content=content, category_id=category_id)
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {created} lectures from JSON'))


