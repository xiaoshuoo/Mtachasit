<template>
  <aside class="hidden lg:flex w-[168px]">
    <div class="glass-element w-full rounded-2xl p-2.5 border-glass shadow-glass flex flex-col sticky top-0">
      <div class="flex items-center mb-2">
        <div class="animated-icon animated-icon--xs mr-1.5" title="Gutierrez">
          <i class="icon fas fa-rocket"></i>
        </div>
        <h3 class="text-sm font-bold text-white">Категории</h3>
      </div>

      <div class="space-y-0.5 overflow-auto pr-0.5" style="scrollbar-gutter: stable;">
        <button @click="select('all')"
                :class="['category-item category-item--sm', active === 'all' ? 'active' : '']">
          <div class="flex items-center flex-1 min-w-0">
            <i class="fas fa-border-all mr-1.5 text-purple-400 text-[12px]"></i>
            <span class="category-name truncate text-[11px] leading-tight">Все категории</span>
          </div>
          <span class="category-count ml-auto">{{ totalCount }}</span>
        </button>

        <button v-for="cat in categories" :key="cat.slug" @click="select(cat.slug)"
                :class="['category-item category-item--sm', active === cat.slug ? 'active' : '']">
          <div class="flex items-center flex-1 min-w-0">
            <i class="fas fa-folder mr-1.5 text-purple-400/80 text-[12px]"></i>
            <span class="category-name truncate text-[11px] leading-tight">{{ cat.name }}</span>
          </div>
          <span class="category-count ml-auto">{{ cat.count }}</span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
const props = defineProps<{ categories: Array<{ name: string; slug: string; count: number }>; active: string; totalCount: number }>()
const emit = defineEmits<{ (e: 'select', value: string): void }>()

function select(value: string) {
  emit('select', value)
}
</script>


