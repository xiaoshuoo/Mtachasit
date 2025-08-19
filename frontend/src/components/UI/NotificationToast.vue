<template>
  <Transition name="toast">
    <div v-if="show" :class="toastClasses" class="fixed top-4 right-4 z-50 max-w-sm">
      <div class="flex items-center p-4 rounded-lg shadow-lg">
        <div class="flex-shrink-0">
          <i :class="iconClasses"></i>
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium" :class="textClasses">
            {{ message }}
          </p>
        </div>
        <div class="ml-auto pl-3">
          <button
            @click="close"
            class="inline-flex text-gray-400 hover:text-gray-600 focus:outline-none"
          >
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  show: boolean
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  close: []
}>()

const toastClasses = computed(() => {
  const base = 'border-l-4'
  switch (props.type) {
    case 'success':
      return `${base} bg-green-50 border-green-400 text-green-800`
    case 'error':
      return `${base} bg-red-50 border-red-400 text-red-800`
    case 'warning':
      return `${base} bg-yellow-50 border-yellow-400 text-yellow-800`
    case 'info':
      return `${base} bg-blue-50 border-blue-400 text-blue-800`
    default:
      return `${base} bg-gray-50 border-gray-400 text-gray-800`
  }
})

const iconClasses = computed(() => {
  const base = 'fas text-lg'
  switch (props.type) {
    case 'success':
      return `${base} fa-check-circle text-green-400`
    case 'error':
      return `${base} fa-exclamation-circle text-red-400`
    case 'warning':
      return `${base} fa-exclamation-triangle text-yellow-400`
    case 'info':
      return `${base} fa-info-circle text-blue-400`
    default:
      return `${base} fa-info-circle text-gray-400`
  }
})

const textClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'text-green-800'
    case 'error':
      return 'text-red-800'
    case 'warning':
      return 'text-yellow-800'
    case 'info':
      return 'text-blue-800'
    default:
      return 'text-gray-800'
  }
})

function close() {
  emit('close')
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
