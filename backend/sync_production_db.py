#!/usr/bin/env python
"""
Скрипт для синхронизации локальной разработки с production базой
"""
import os
import sys
import django
from pathlib import Path

# Добавляем backend в Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Устанавливаем переменные окружения для production базы
os.environ['DEBUG'] = 'True'
os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1'
os.environ['DB_ENGINE'] = 'django.db.backends.postgresql'

# Получаем данные из production (замените на ваши реальные данные)
os.environ['DB_NAME'] = 'djangodb'  # Имя базы из Render
os.environ['DB_USER'] = 'djangouser'  # Пользователь из Render
os.environ['DB_PASSWORD'] = 'your_password_here'  # Пароль из Render
os.environ['DB_HOST'] = 'your_host_here'  # Хост из Render
os.environ['DB_PORT'] = '5432'

# Устанавливаем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    
    print("🔄 Синхронизация с production базой данных...")
    print("🔧 DEBUG = True")
    print("🔧 Database = PostgreSQL (production)")
    print("🔧 ALLOWED_HOSTS = localhost,127.0.0.1")
    print()
    
    # Запускаем Django команду
    execute_from_command_line(sys.argv)
