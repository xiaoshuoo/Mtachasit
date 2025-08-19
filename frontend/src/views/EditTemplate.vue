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
})

async function save(payload: typeof form) {
  if (form.id) {
    await templateApi.update(form.id, payload)
  } else {
    await templateApi.create(payload)
  }
  router.push({ name: 'home' })
}

function goBack() { router.back() }
</script>


