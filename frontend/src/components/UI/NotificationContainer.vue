<template>
  <div class="fixed top-4 right-4 z-50 space-y-2">
    <NotificationToast
      v-for="notification in notifications"
      :key="notification.id"
      :show="true"
      :type="notification.type"
      :message="notification.message"
      @close="removeNotification(notification.id)"
    />
  </div>
</template>

<script setup lang="ts">
import { useNotifications } from '../../composables/useNotifications'
import NotificationToast from './NotificationToast.vue'

const { notifications, removeNotification } = useNotifications()
</script>
