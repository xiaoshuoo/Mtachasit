<template>
  <button class="neon-button" :class="customClass" @click="$emit('click')">
    <slot />
  </button>
  
</template>

<script setup lang="ts">
defineProps<{ customClass?: string }>()
</script>


