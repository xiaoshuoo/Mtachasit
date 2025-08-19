<template>
  <div class="glass-element" :class="customClass">
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{ customClass?: string }>()
</script>


