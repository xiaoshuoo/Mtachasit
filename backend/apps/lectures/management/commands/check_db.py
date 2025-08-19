from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Checks database connectivity by executing SELECT 1'

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1;')
                row = cursor.fetchone()
            self.stdout.write(self.style.SUCCESS(f'Database OK. Result: {row}'))
        except OperationalError as exc:
            self.stderr.write(self.style.ERROR(f'Database ERROR: {exc}'))
            raise SystemExit(1)


