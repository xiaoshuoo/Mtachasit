# Инструкция по деплою проекта на Render

## Обзор проекта
Ваш проект состоит из:
- **Backend**: Django REST API
- **Frontend**: Vue.js 3 + Vite + Tailwind CSS

## Шаг 1: Деплой Django Backend

### 1.1 Подготовка
1. Убедитесь, что все файлы закоммичены в Git
2. Создайте репозиторий на GitHub/GitLab

### 1.2 Настройка на Render
1. Зайдите на [dashboard.render.com](https://dashboard.render.com/)
2. Нажмите "New +" → "Web Service"
3. Подключите ваш Git репозиторий
4. Выберите ветку (обычно `main` или `master`)

### 1.3 Конфигурация Backend
- **Name**: `django-backend` (или любое другое)
- **Environment**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn config.wsgi:application`
- **Plan**: Free

### 1.4 Переменные окружения
Render автоматически создаст PostgreSQL базу данных и настроит переменные:
- `SECRET_KEY` - генерируется автоматически
- `DEBUG` - `false`
- `DB_*` - настраиваются автоматически из базы данных

### 1.5 Создание базы данных
1. В Render Dashboard нажмите "New +" → "PostgreSQL"
2. Выберите Free план
3. Скопируйте имя базы данных
4. В настройках web service добавьте ссылку на базу данных

## Шаг 2: Деплой Vue.js Frontend

### 2.1 Настройка на Render
1. "New +" → "Static Site"
2. Подключите тот же Git репозиторий
3. Выберите ветку

### 2.2 Конфигурация Frontend
- **Name**: `vue-frontend`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`
- **Plan**: Free

### 2.3 Переменные окружения
- `VITE_API_URL`: URL вашего Django backend (например: `https://django-backend.onrender.com`)

## Шаг 3: Обновление конфигурации

### 3.1 Backend
После деплоя backend, обновите `frontend/render.yaml`:
```yaml
envVars:
  - key: VITE_API_URL
    value: "https://ВАШ_BACKEND_URL.onrender.com"
```

### 3.2 Frontend
Обновите `backend/config/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "https://ВАШ_FRONTEND_URL.onrender.com",
]
```

## Шаг 4: Проверка деплоя

### 4.1 Backend
1. Проверьте логи на Render Dashboard
2. Откройте URL backend + `/admin/`
3. Создайте суперпользователя: `python manage.py createsuperuser`

### 4.2 Frontend
1. Откройте URL frontend
2. Проверьте, что API запросы работают
3. Проверьте консоль браузера на ошибки

## Возможные проблемы

### Backend не запускается
- Проверьте логи на Render
- Убедитесь, что `build.sh` исполняемый
- Проверьте переменные окружения

### Frontend не собирается
- Проверьте версии Node.js
- Убедитесь, что все зависимости в `package.json`

### CORS ошибки
- Проверьте настройки CORS в Django
- Убедитесь, что frontend URL добавлен в `CORS_ALLOWED_ORIGINS`

## Полезные команды

### Локальная проверка
```bash
# Backend
cd backend
python manage.py runserver

# Frontend
cd frontend
npm run dev
```

### Проверка production build
```bash
# Frontend
cd frontend
npm run build
npm run preview
```

## Ссылки
- [Render Documentation](https://render.com/docs)
- [Django Deployment](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Vue.js Deployment](https://vuejs.org/guide/best-practices/production-deployment.html)
