<template>
  <div class="relative">
    <input
      v-model="query"
      type="text"
      placeholder="Поиск по названию..."
      class="w-full rounded-xl px-4 py-2 bg-white/5 border border-white/10 focus:outline-none focus:ring-2 focus:ring-accentBlue"
    />
    <i class="fa-solid fa-magnifying-glass absolute right-3 top-2.5 text-slate-400"></i>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: string): void }>()
const query = ref(props.modelValue || '')

watch(() => props.modelValue, v => query.value = v)
watch(query, v => emit('update:modelValue', v))
</script>


