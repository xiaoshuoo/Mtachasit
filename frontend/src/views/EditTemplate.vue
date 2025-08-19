<template>
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <div class="md:col-span-3">
      <div class="glass-card rounded-xl p-4 md:p-6">
        <TemplateEditor v-model="form" @submit="save" @cancel="goBack" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { templateApi, rossiTemplateApi } from '../services/api'
import TemplateEditor from '../components/TemplateEditor.vue'
import { useNotifications } from '../composables/useNotifications'

const route = useRoute()
const router = useRouter()
const { success, error, warning } = useNotifications()

// Получаем тип шаблона из URL и роута
const templateType = computed(() => {
  console.log('🔍 Computing templateType:')
  console.log('  - route.path:', route.path)
  console.log('  - route.name:', route.name)
  
  if (route.path.includes('rossi')) {
    console.log('  ✅ Found "rossi" in path')
    return 'rossi'
  }
  if (route.path.includes('gutierrez')) {
    console.log('  ✅ Found "gutierrez" in path')
    return 'gutierrez'
  }
  if (route.name === 'new-rossi') {
    console.log('  ✅ Route name is "new-rossi"')
    return 'rossi'
  }
  if (route.name === 'new-gutierrez') {
    console.log('  ✅ Route name is "new-gutierrez"')
    return 'gutierrez'
  }
  if (route.name === 'templates-rossi') {
    console.log('  ✅ Route name is "templates-rossi"')
    return 'rossi'
  }
  if (route.name === 'templates-gutierrez-public') {
    console.log('  ✅ Route name is "templates-gutierrez-public"')
    return 'gutierrez'
  }
  if (route.name === 'new') {
    console.log('  ✅ Route name is "new" - returning "general"')
    return 'general'
  }
  console.log('  ⚠️ No match found, returning "gutierrez" as fallback')
  return 'gutierrez'
})

// Выбираем правильный API в зависимости от типа
const api = computed(() => {
  if (templateType.value === 'rossi') return rossiTemplateApi
  if (templateType.value === 'gutierrez') return templateApi
  if (templateType.value === 'general') {
    // Для general типа (my-templates) нужно использовать API с created_by_id=1
    console.log('🔍 Using templateApi with created_by_id=1 for general type')
    return templateApi
  }
  return templateApi // fallback
})

console.log('🔍 Route path:', route.path)
console.log('🔍 Route name:', route.name)
console.log('🔍 Template type:', templateType.value)
console.log('🔍 Using API:', templateType.value === 'rossi' ? 'rossiTemplateApi' : 'templateApi')

const form = reactive<{ id?: number; title: string; category: string; content: string }>({
  title: '',
  category: '',
  content: '',
})

onMounted(async () => {
  const id = route.params.id as string | undefined
  if (id && id !== 'Xuachoo') { // Проверяем что это не Xuachoo
    try {
      console.log('🔍 Loading template with ID:', id)
      const { data } = await api.value.getById(Number(id))
      Object.assign(form, data)
      console.log('✅ Template loaded successfully')
    } catch (error) {
      console.error('❌ Error loading template:', error)
      if (error.response?.status === 404) {
        console.log('⚠️ Template not found, creating new one')
        warning('Шаблон не найден. Создаем новый.')
        // Если шаблон не найден, очищаем форму для создания нового
        Object.assign(form, { title: '', category: '', content: '' })
      } else {
        error('Ошибка при загрузке шаблона. Попробуйте еще раз.')
      }
    }
  } else {
    console.log('🆕 Creating new template (no ID or Xuachoo route)')
  }
  
  console.log('🔍 Template type:', templateType.value)
  console.log('🔍 Route path:', route.path)
})

async function save(payload: typeof form) {
  try {
    console.log('🚀 Starting save process...')
    console.log('📋 Payload:', payload)
    console.log('🔍 Form ID:', form.id)
    console.log('📍 Current route:', route)
    console.log('📍 Route name:', route.name)
    console.log('📍 Route path:', route.path)
    
    if (form.id) {
      // Обновление существующего шаблона
      console.log('📝 Updating existing template...')
      await api.value.update(form.id, payload)
      console.log('✅ Template updated successfully')
      router.push({ name: 'home' })
    } else {
      // Создание нового шаблона
      console.log('🆕 Creating new template...')
      
      let response
      if (templateType.value === 'general') {
        // Для general типа добавляем created_by_id=1
        console.log('🔍 Adding created_by_id=1 for general type')
        const payloadWithUserId = { ...payload, created_by_id: 1 }
        console.log('📤 Creating template with payload:', payloadWithUserId)
        response = await api.value.create(payloadWithUserId)
      } else {
        response = await api.value.create(payload)
      }
      
      console.log('✅ Template created successfully:', response.data)
      
      // Показываем уведомление об успехе
      success('Шаблон успешно создан!')
      
      // После создания редиректим на список шаблонов
      console.log('🔄 Redirecting after template creation...')
      console.log('🔍 Template type:', templateType.value)
      console.log('🔍 Template type comparison:')
      console.log('  - templateType.value === "rossi":', templateType.value === 'rossi')
      console.log('  - templateType.value === "general":', templateType.value === 'general')
      console.log('  - templateType.value === "gutierrez":', templateType.value === 'gutierrez')
      
      if (templateType.value === 'rossi') {
        console.log('🔄 Redirecting to Rossi templates')
        console.log('📍 Target route name: templates-rossi')
        console.log('📍 Target path: /templates/rossi')
        router.push({ name: 'templates-rossi' })
      } else if (templateType.value === 'general') {
        console.log('🔄 Redirecting to my templates (general)')
        console.log('📍 Target route name: my-templates-alt')
        console.log('📍 Target path: /templates/Xuachoo')
        router.push({ name: 'my-templates-alt' })
      } else {
        console.log('�� Redirecting to Gutierrez templates (fallback)')
        console.log('📍 Target route name: templates-gutierrez-public')
        console.log('📍 Target path: /templates/gutierrez')
        router.push({ name: 'templates-gutierrez-public' })
      }
    }
  } catch (error) {
    console.error('❌ Error saving template:', error)
    
    // Определяем тип ошибки и показываем соответствующее уведомление
    if (error.response?.status === 400) {
      error('Неверные данные. Проверьте заполнение полей.')
    } else if (error.response?.status === 401) {
      error('Необходима авторизация.')
    } else if (error.response?.status === 403) {
      error('Доступ запрещен.')
    } else if (error.response?.status === 404) {
      error('Шаблон не найден.')
    } else if (error.response?.status === 500) {
      error('Ошибка сервера. Попробуйте позже.')
    } else if (error.code === 'NETWORK_ERROR') {
      error('Ошибка сети. Проверьте подключение к интернету.')
    } else {
      error('Ошибка при сохранении шаблона. Попробуйте еще раз.')
    }
  }
}

function goBack() { router.back() }
</script>


