<template>
  <div class="search-input">
    <input class="input" :placeholder="placeholder" :value="modelValue" @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)" />
    <i class="fas fa-search search-icon"></i>
  </div>
</template>

<script setup lang="ts">
defineProps<{ modelValue: string; placeholder?: string }>()
defineEmits<{ (e: 'update:modelValue', v: string): void }>()
</script>


