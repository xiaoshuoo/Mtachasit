from django.core.management.base import BaseCommand
from django.db.models import Count
from apps.lectures.models import LectureCategory


class Command(BaseCommand):
    help = 'Delete lecture categories that have zero lectures (cleanup duplicates created accidentally).'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without deleting')

    def handle(self, *args, **options):
        dry = options['dry_run']

        qs = (
            LectureCategory.objects
            .annotate(num_lectures=Count('lectures'))
            .filter(num_lectures=0)
        )

        targets = list(qs)
        if not targets:
            self.stdout.write(self.style.SUCCESS('No empty categories to delete.'))
            return

        for cat in targets:
            self.stdout.write(f"- {cat.id}: {cat.name} (slug={cat.slug})")

        if dry:
            self.stdout.write(self.style.WARNING(f"Would delete {len(targets)} categories (dry-run)."))
            return

        count = len(targets)
        for cat in targets:
            cat.delete()

        self.stdout.write(self.style.SUCCESS(f'Deleted {count} empty categories.'))


