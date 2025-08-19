import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import './styles/cosmic-theme.css'
import './styles/glass-components.css'
import './styles/animations.css'
import './styles/utilities.css'
import App from './App.vue'
import TemplateList from './views/TemplateList.vue'
import EditTemplate from './views/EditTemplate.vue'
import Lectures from './views/Lectures.vue'
import Login from './views/Login.vue'
import HomePage from './views/HomePage.vue'
import NotFound from './views/NotFound.vue'

const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/Xuachoo', name: 'my-templates', component: TemplateList, props: { filter: 'all' } },
  { path: '/templates/rossi', name: 'templates-rossi', component: TemplateList, props: { filter: 'rossi' } },
  { path: '/templates/gutierrez', name: 'templates-gutierrez-public', component: TemplateList, props: { filter: 'gutierrez-public' } },
  { path: '/new/gutierrez', name: 'new-gutierrez', component: EditTemplate, props: { templateType: 'gutierrez' } },
  { path: '/new/rossi', name: 'new-rossi', component: EditTemplate, props: { templateType: 'rossi' } },
  { path: '/new', name: 'new', component: EditTemplate },
  { path: '/templates/:id', name: 'edit', component: EditTemplate, props: true },
  { path: '/lectures', name: 'lectures', component: Lectures },
  { path: '/login', name: 'login', component: Login },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Добавляем обработчик ошибок для отладки
router.onError((error) => {
  console.error('🚨 Router error:', error)
})

// Добавляем логирование навигации
router.beforeEach((to, from, next) => {
  console.log('🧭 Router navigation:')
  console.log('  📍 From:', from.path, from.name)
  console.log('  🎯 To:', to.path, to.name)
  console.log('  🔍 To params:', to.params)
  next()
})

router.afterEach((to, from) => {
  console.log('✅ Navigation completed:')
  console.log('  📍 Current path:', to.path)
  console.log('  📍 Current name:', to.name)
})

createApp(App)
  .use(createPinia())
  .use(router)
  .mount('#app')
