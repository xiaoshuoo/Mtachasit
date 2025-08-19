<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="glass-element w-full max-w-md rounded-2xl p-6 border-glass shadow-glass">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-300">
          <i class="fas fa-user-lock"></i>
        </div>
        <h1 class="text-xl font-semibold">Вход</h1>
      </div>
      <form @submit.prevent="login" class="space-y-4">
        <div>
          <label class="block text-sm text-gray-300 mb-1">Логин</label>
          <input v-model.trim="username" class="w-full px-4 py-3 bg-black/20 border border-purple-500/10 rounded-xl text-white" required />
        </div>
        <div>
          <label class="block text-sm text-gray-300 mb-1">Пароль</label>
          <input v-model="password" type="password" class="w-full px-4 py-3 bg-black/20 border border-purple-500/10 rounded-xl text-white" required />
        </div>
        <div class="flex justify-end">
          <NeonButton type="submit">Войти</NeonButton>
        </div>
      </form>
      <p v-if="error" class="text-red-400 text-sm mt-3">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import NeonButton from '@/components/UI/NeonButton.vue'
import { authApi } from '@/services/api'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

async function login(){
  try{
    error.value = ''
    await authApi.login(username.value, password.value)
    router.push({ name: 'lectures' })
  }catch(e:any){
    error.value = 'Неверный логин или пароль'
  }
}
</script>

<style scoped>
</style>


