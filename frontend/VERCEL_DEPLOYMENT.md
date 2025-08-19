# Деплой Frontend на Vercel

## Обзор
Frontend (Vue.js) развернут на Vercel для лучшей поддержки SPA routing.

## Шаг 1: Подготовка
1. Убедитесь, что все файлы закоммичены в Git
2. Убедитесь, что backend работает на Render

## Шаг 2: Регистрация на Vercel
1. Зайдите на [vercel.com](https://vercel.com)
2. Войдите через GitHub
3. Нажмите "New Project"

## Шаг 3: Настройка проекта
1. **Import Git Repository**: выберите ваш репозиторий
2. **Framework Preset**: Vite (автоматически определится)
3. **Root Directory**: `frontend`
4. **Build Command**: `npm run build` (автоматически)
5. **Output Directory**: `dist` (автоматически)

## Шаг 4: Переменные окружения
В настройках проекта добавьте:
- **Key**: `VITE_API_URL`
- **Value**: `https://mtachasit.onrender.com`

## Шаг 5: Деплой
1. Нажмите "Deploy"
2. Vercel автоматически соберет и развернет проект
3. Получите URL вида: `https://your-project.vercel.app`

## Проверка
1. **Главная страница**: должна открываться
2. **Маршруты**: `/rossi`, `/templates` и т.д. должны работать
3. **API запросы**: должны идти на backend

## Преимущества Vercel
- ✅ Автоматическая поддержка SPA routing
- ✅ Быстрый деплой
- ✅ CDN по всему миру
- ✅ Бесплатный план
- ✅ Автоматические preview deployments

## Ссылки
- [Vercel Documentation](https://vercel.com/docs)
- [Vue.js on Vercel](https://vercel.com/guides/deploying-vuejs-to-vercel)
