from django.core.management.base import BaseCommand
from django.db import connection, transaction
from apps.lectures.models import Lecture, LectureCategory


class Command(BaseCommand):
    help = (
        "Copy data from existing tables in the same database (e.g., blog_lecture/blog_category) "
        "into our models (Lecture/LectureCategory)."
    )

    def add_arguments(self, parser):
        parser.add_argument('--lectures-table', default='blog_lecture')
        parser.add_argument('--categories-table', default='blog_category')
        parser.add_argument('--title-field', default='title')
        parser.add_argument('--content-field', default='content')
        parser.add_argument('--category-id-field', default='category_id')
        parser.add_argument('--cat-id', default='id')
        parser.add_argument('--cat-name', default='name')
        parser.add_argument('--cat-slug', default='slug')

    def handle(self, *args, **opts):
        lt = opts['lectures_table']
        ct = opts['categories_table']
        title_f = opts['title_field']
        content_f = opts['content_field']
        cat_fk = opts['category_id_field']
        cat_id = opts['cat_id']
        cat_name = opts['cat_name']
        cat_slug = opts['cat_slug']

        with connection.cursor() as cur:
            cur.execute(f'SELECT {cat_id}, {cat_name}, {cat_slug} FROM {ct}')
            rows = cur.fetchall()

        srcid_to_catid: dict[str, int] = {}
        with transaction.atomic():
            for r in rows:
                src_pk, name, slug = r
                if not slug and name:
                    slug = str(name).lower().replace(' ', '-')
                cat, _ = LectureCategory.objects.get_or_create(slug=slug or str(src_pk), defaults={'name': name or slug or str(src_pk)})
                srcid_to_catid[str(src_pk)] = cat.id

        with connection.cursor() as cur:
            cur.execute(f'SELECT {title_f}, {content_f}, {cat_fk} FROM {lt}')
            lrows = cur.fetchall()

        created = 0
        with transaction.atomic():
            for title, content, src_cat in lrows:
                category_id = srcid_to_catid.get(str(src_cat)) if src_cat is not None else None
                Lecture.objects.create(title=title or 'Без названия', content=content or '', category_id=category_id)
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {created} lectures from {lt}'))


