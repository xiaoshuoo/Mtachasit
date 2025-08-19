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

# Создаем суперпользователя (если не существует)
python manage.py create_superuser
