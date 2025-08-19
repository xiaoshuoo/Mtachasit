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
import { onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { templateApi } from '../services/api'
import TemplateEditor from '../components/TemplateEditor.vue'

const route = useRoute()
const router = useRouter()

// Получаем тип шаблона из URL
const templateType = route.path.includes('rossi') ? 'rossi' : 'gutierrez'

console.log('🔍 Route path:', route.path)
console.log('🔍 Template type:', templateType)

const form = reactive<{ id?: number; title: string; category: string; content: string }>({
  title: '',
  category: '',
  content: '',
})

onMounted(async () => {
  const id = route.params.id as string | undefined
  if (id) {
    const { data } = await templateApi.getById(Number(id))
    Object.assign(form, data)
  }
  
  console.log('🔍 Template type:', templateType)
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
      await templateApi.update(form.id, payload)
      console.log('✅ Template updated successfully')
      router.push({ name: 'home' })
    } else {
      // Создание нового шаблона
      console.log('🆕 Creating new template...')
      const response = await templateApi.create(payload)
      console.log('✅ Template created successfully:', response.data)
      
      // После создания редиректим на список шаблонов
      console.log('🔄 Redirecting after template creation...')
      console.log('🔍 Template type:', templateType)
      
      if (templateType === 'rossi') {
        console.log('🔄 Redirecting to Rossi templates')
        console.log('📍 Target route name: templates-rossi')
        console.log('📍 Target path: /templates/rossi')
        router.push({ name: 'templates-rossi' })
      } else {
        console.log('🔄 Redirecting to Gutierrez templates')
        console.log('📍 Target route name: templates-gutierrez-public')
        console.log('📍 Target path: /templates/gutierrez')
        router.push({ name: 'templates-gutierrez-public' })
      }
    }
  } catch (error) {
    console.error('❌ Error saving template:', error)
    // Здесь можно добавить уведомление об ошибке
    alert('Ошибка при сохранении шаблона. Попробуйте еще раз.')
  }
}

function goBack() { router.back() }
</script>


