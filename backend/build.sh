#!/usr/bin/env bash
# exit on error
set -o errexit

cd backend

# Устанавливаем зависимости
pip install -r requirements.txt

# Создаем папку для статических файлов
mkdir -p staticfiles

# Собираем статические файлы
python manage.py collectstatic --no-input

# Применяем миграции
python manage.py migrate

# Создаем суперпользователя odinochka с паролем 1
echo "🔑 Creating superuser odinochka..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='odinochka').exists():
    User.objects.create_superuser('odinochka', 'odinochka@example.com', '1')
    print("✅ Superuser 'odinochka' created successfully!")
else:
    print("ℹ️ Superuser 'odinochka' already exists!")
EOF
