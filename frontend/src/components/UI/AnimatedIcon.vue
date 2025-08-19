<template>
  <div class="animated-icon" :title="title">
    <i :class="['icon', icon]"></i>
  </div>
</template>

<script setup lang="ts">
defineProps<{ icon: string; title?: string }>()
</script>


