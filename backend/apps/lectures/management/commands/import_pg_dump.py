import json
import re
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from apps.lectures.models import Lecture, LectureCategory


class Command(BaseCommand):
    help = "Import lectures from a PostgreSQL plain SQL dump by querying source tables via psql-like COPY-parsing (best-effort)."

    def add_arguments(self, parser):
        parser.add_argument('dump_path', type=str, help='Path to PostgreSQL dump (.sql)')
        parser.add_argument('--table-lectures', type=str, default='lectures', help='Source table for lectures')
        parser.add_argument('--table-categories', type=str, default='categories', help='Source table for categories')

    def handle(self, *args, **options):
        dump_path = options['dump_path']
        table_lectures = options['table_lectures']
        table_categories = options['table_categories']

        try:
            with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
                dump_text = f.read()
        except Exception as e:
            raise CommandError(f'Cannot read dump: {e}')

        # Extremely simplified COPY reader (expects sections like: COPY table (cols...) FROM stdin; ... \.')
        def parse_copy(table_name):
            pattern = re.compile(rf"COPY\s+{re.escape(table_name)}\s*\((.*?)\)\s*FROM\s+stdin;([\s\S]*?)\\\.", re.IGNORECASE)
            m = pattern.search(dump_text)
            if not m:
                return []
            cols = [c.strip().strip('"') for c in m.group(1).split(',')]
            rows_block = m.group(2)
            rows = []
            for line in rows_block.splitlines():
                if not line or line.startswith('--'):
                    continue
                if line.strip() == '\\.':
                    break
                # fields are tab-separated; \N is NULL
                parts = [None if p == '\\N' else p for p in line.split('\t')]
                rows.append(dict(zip(cols, parts)))
            return rows

        category_rows = parse_copy(table_categories)
        lecture_rows = parse_copy(table_lectures)

        if not lecture_rows:
            self.stdout.write(self.style.WARNING('No lecture rows parsed. Check table names or dump format.'))

        # Map categories
        slug_to_id = {}
        id_to_catid = {}
        with transaction.atomic():
            for row in category_rows:
                name = row.get('name') or row.get('title') or 'Без категории'
                slug = (row.get('slug') or str(name)).lower().replace(' ', '-').strip()
                cat, _ = LectureCategory.objects.get_or_create(slug=slug, defaults={'name': name})
                slug_to_id[slug] = cat.id
                src_id = row.get('id') or row.get('pk')
                if src_id is not None:
                    id_to_catid[str(src_id)] = cat.id

            created = 0
            for r in lecture_rows:
                title = r.get('title') or r.get('name') or 'Без названия'
                content = r.get('content') or r.get('text') or ''
                category_id = None
                cat_slug = (r.get('category_slug') or '').lower()
                if cat_slug:
                    category_id = slug_to_id.get(cat_slug)
                if category_id is None:
                    cat_fk = r.get('category_id') or r.get('category') or r.get('cat_id')
                    if cat_fk is not None:
                        category_id = id_to_catid.get(str(cat_fk))
                Lecture.objects.create(title=title, content=content, category_id=category_id)
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Imported {created} lectures'))


