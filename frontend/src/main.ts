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
  { path: '/templates/:id', name: 'edit', component: EditTemplate, props: true },
  { path: '/new', name: 'new', component: EditTemplate },
  { path: '/lectures', name: 'lectures', component: Lectures },
  { path: '/login', name: 'login', component: Login },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App)
  .use(createPinia())
  .use(router)
  .mount('#app')
