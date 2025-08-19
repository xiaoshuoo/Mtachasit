from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS('Superuser already exists')
            )
            return

        username = 'odinochka'
        email = 'odinochka@example.com'
        password = '1'

        # Проверяем переменные окружения
        if hasattr(settings, 'SUPERUSER_USERNAME'):
            username = settings.SUPERUSER_USERNAME
        if hasattr(settings, 'SUPERUSER_EMAIL'):
            email = settings.SUPERUSER_EMAIL
        if hasattr(settings, 'SUPERUSER_PASSWORD'):
            password = settings.SUPERUSER_PASSWORD

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(f'Superuser "{username}" created successfully')
        )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write('Please change the password after first login!')
