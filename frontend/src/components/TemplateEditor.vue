<template>
  <form class="space-y-6" @submit.prevent="onSubmit">
    <div>
      <label class="block text-sm font-medium text-gray-400 mb-2">
        <i class="fas fa-heading text-purple-400 mr-2"></i>
        Название
      </label>
      <input v-model="form.title" required placeholder="Введите название шаблона..." class="w-full px-4 py-3 bg-black/20 border border-purple-500/10 rounded-xl text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 placeholder-gray-500" />
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-400 mb-2">
        <i class="fas fa-layer-group text-purple-400 mr-2"></i>
        Категория
      </label>
      <input v-model="form.category" required placeholder="Введите категорию..." class="w-full px-4 py-3 bg-black/20 border border-purple-500/10 rounded-xl text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 placeholder-gray-500" />
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-400 mb-2">
        <i class="fas fa-align-left text-purple-400 mr-2"></i>
        Содержание
      </label>
      <textarea v-model="form.content" required rows="10" placeholder="Каждая строка — отдельная фраза..." class="w-full px-4 py-3 bg-black/20 border border-purple-500/10 rounded-xl text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 placeholder-gray-500"></textarea>
    </div>
    <div class="flex gap-2">
      <button type="submit" class="group px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:shadow-lg hover:shadow-purple-500/25 relative overflow-hidden">
        <i class="fa-solid fa-floppy-disk mr-2"></i>
        Сохранить
        <div class="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 opacity-0 group-hover:opacity-100"></div>
      </button>
      <button type="button" @click="emit('cancel')" class="px-4 py-3 rounded-xl bg-white/5 hover:bg-white/10 text-white border border-white/10">
        Отмена
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, watch, toRaw } from 'vue'

interface TemplatePayload {
  id?: number
  title: string
  category: string
  content: string
}

const props = defineProps<{ modelValue: TemplatePayload }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: TemplatePayload): void; (e: 'submit', v: TemplatePayload): void; (e: 'cancel'): void }>()

const form = reactive<TemplatePayload>({ title: '', category: '', content: '', ...props.modelValue })

watch(() => props.modelValue, (v) => Object.assign(form, v || {}), { deep: true })
watch(form, (v) => emit('update:modelValue', toRaw(v) as TemplatePayload), { deep: true })

function onSubmit() {
  emit('submit', { ...form })
}
</script>


