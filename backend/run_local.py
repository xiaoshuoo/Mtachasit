#!/usr/bin/env python
"""
Local development script for Django backend
"""
import os
import sys
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Устанавливаем переменные окружения ДО загрузки Django
env_local = backend_dir / '.env.local'
if env_local.exists():
    print("🔧 Found .env.local - using custom database settings")
    # Переменные будут загружены из .env.local
else:
    print("🔧 No .env.local found - using Clever Cloud database")
    # Устанавливаем переменные окружения для Clever Cloud
    os.environ['DEBUG'] = 'True'
    os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1'
    os.environ['POSTGRESQL_ADDON_HOST'] = 'bx6whf2srgqgcuyzg5vx-postgresql.services.clever-cloud.com'
    os.environ['POSTGRESQL_ADDON_DB'] = 'bx6whf2srgqgcuyzg5vx'
    os.environ['POSTGRESQL_ADDON_USER'] = 'uo9kug9cfbvudhutwjwo'
    os.environ['POSTGRESQL_ADDON_PORT'] = '50013'
    os.environ['POSTGRESQL_ADDON_PASSWORD'] = 'QtQkPVkK7lUhUrwCDuEYN3y4R1iTcn'

# Теперь загружаем Django
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    
    print("🚀 Starting Django in LOCAL DEVELOPMENT mode...")
    print("🔧 DEBUG = True")
    print("🔧 ALLOWED_HOSTS = localhost,127.0.0.1")
    print("🌐 Server will be available at: http://localhost:8000")
    print("🔑 Admin panel: http://localhost:8000/admin")
    print("📚 API: http://localhost:8000/api/")
    print()
    
    # Run Django management command
    execute_from_command_line(sys.argv)
