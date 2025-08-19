<template>
  <div class="min-h-screen text-white relative">
    <CosmicBackground />
    <div class="px-4 md:px-8 py-4 md:py-8">
      <router-view />
    </div>
    <NotificationContainer />
  </div>
</template>

<script setup lang="ts">
import '@fortawesome/fontawesome-free/css/all.min.css'
import CosmicBackground from './components/Layout/CosmicBackground.vue'
import NotificationContainer from './components/UI/NotificationContainer.vue'
</script>


