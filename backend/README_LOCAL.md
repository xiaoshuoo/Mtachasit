# 🚀 Локальная разработка Django Backend

## 🎯 Варианты запуска

### Вариант 1: С Clever Cloud базой данных (по умолчанию)
Использует ту же базу данных, что и на хостинге.

#### 1. Убедитесь что установлен PostgreSQL драйвер:
```bash
pip install psycopg[binary]
```

#### 2. Запустите:
```bash
python run_local.py runserver
```

**Автоматически используются настройки Clever Cloud:**
- Host: `bx6whf2srgqgcuyzg5vx-postgresql.services.clever-cloud.com`
- Database: `bx6whf2srgqgcuyzg5vx`
- User: `uo9kug9cfbvudhutwjwo`
- Port: `50013`

### Вариант 2: С кастомными настройками базы
Создайте файл `.env.local` для переопределения настроек.

#### 1. Создайте файл `.env.local` в папке `backend/`:
```bash
# Custom Database Settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=5432
```

#### 2. Запустите:
```bash
python run_local.py runserver
```

## 🔑 Доступ

- **Frontend**: http://localhost:5173 (Vue.js dev server)
- **Backend**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/

## 👤 Суперпользователь

- **Username**: `odinochka`
- **Password**: `1`

## 📁 Структура проекта

```
backend/
├── apps/                    # Django приложения
│   ├── templates/          # Управление шаблонами
│   └── lectures/          # Управление лекциями
├── config/                 # Настройки Django
├── run_local.py           # Скрипт локального запуска
├── .env.local             # Опционально: кастомные настройки БД
└── requirements.txt       # Python зависимости
```

## 🔧 Переменные окружения

### С Clever Cloud базой (по умолчанию):
- `DEBUG = True`
- `DATABASE = PostgreSQL (Clever Cloud)`
- `ALLOWED_HOSTS = localhost,127.0.0.1`
- `POSTGRESQL_ADDON_*` переменные автоматически установлены

### С кастомными настройками (.env.local):
- `DEBUG = True`
- `DATABASE = PostgreSQL (custom)`
- `ALLOWED_HOSTS = localhost,127.0.0.1`

## 🚨 Проблемы

### Если не работает с Clever Cloud базой:
1. Убедитесь что установлен `psycopg[binary]`
2. Проверьте доступность базы данных
3. Проверьте правильность порта (50013)

### Если не работает create_superuser:
```bash
python run_local.py shell
```
```python
from django.contrib.auth.models import User
User.objects.create_superuser('odinochka', 'odinochka@example.com', '1')
exit()
```

## 🌐 CORS для локальной разработки

Frontend на `localhost:5173` автоматически разрешен для API запросов.

## 💡 Преимущества Clever Cloud базы:

✅ **Одинаковые данные** везде  
✅ **Не нужно мигрировать** локально  
✅ **Актуальная структура** базы  
✅ **Реальные данные** для разработки  
✅ **Автоматическая настройка** без .env файлов
