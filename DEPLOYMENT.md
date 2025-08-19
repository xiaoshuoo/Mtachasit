# Инструкция по деплою проекта

## Обзор проекта
Ваш проект состоит из:
- **Backend**: Django REST API (развернут на Render)
- **Frontend**: Vue.js 3 + Vite + Tailwind CSS (развернут на Vercel)

## Шаг 1: Деплой Django Backend на Render

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
- **Start Command**: `gunicorn --chdir backend config.wsgi:application`
- **Plan**: Free

### 1.4 Переменные окружения
В Render Dashboard добавьте:
- `DEBUG`: `false`
- `ALLOWED_HOSTS`: `mtachasit.onrender.com`
- `SECRET_KEY`: (оставьте пустым для автогенерации)

### 1.5 Создание базы данных
1. "New +" → "PostgreSQL" (Free план)
2. Свяжите с backend service

## Шаг 2: Деплой Vue.js Frontend на Vercel

### 2.1 Регистрация на Vercel
1. Зайдите на [vercel.com](https://vercel.com)
2. Войдите через GitHub
3. Нажмите "New Project"

### 2.2 Настройка Frontend
1. **Import Git Repository**: выберите ваш репозиторий
2. **Root Directory**: `frontend`
3. **Framework Preset**: Vite (автоматически)
4. **Build Command**: `npm run build` (автоматически)
5. **Output Directory**: `dist` (автоматически)

### 2.3 Переменные окружения
В Vercel добавьте:
- `VITE_API_URL`: `https://ВАШ_BACKEND_URL.onrender.com`

## Шаг 3: Проверка деплоя

### 3.1 Backend
1. Проверьте логи на Render Dashboard
2. Откройте URL backend + `/admin/`
3. Создайте суперпользователя

### 3.2 Frontend
1. Откройте URL frontend на Vercel
2. Проверьте, что API запросы работают
3. Проверьте маршруты: `/rossi`, `/templates` и т.д.

## Преимущества такого подхода

### Render (Backend):
- ✅ Поддержка Python/Django
- ✅ PostgreSQL база данных
- ✅ WebSocket поддержка
- ✅ Бесплатный план

### Vercel (Frontend):
- ✅ Автоматическая поддержка SPA routing
- ✅ Быстрый деплой
- ✅ CDN по всему миру
- ✅ Бесплатный план

## Ссылки
- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Django Deployment](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Vue.js on Vercel](https://vercel.com/guides/deploying-vuejs-to-vercel)
