<template>
  <div class="template-card glass-element rounded-2xl overflow-hidden border-glass shadow-glass w-full bg-[rgba(26,22,37,0.60)]" role="group">
    <!-- Collapsed row header -->
    <div class="template-row flex items-center justify-between h-[64px] px-5 cursor-pointer hover:bg-white/5" @click="expanded = !expanded">
      <!-- Left: number -->
      <div class="flex items-center w-[52px] flex-shrink-0">
        <div class="w-8 h-8 rounded-full bg-white/5 ring-1 ring-white/10 flex items-center justify-center text-gray-300 font-semibold text-[12px]">#{{ index }}</div>
      </div>

      <!-- Center: title + preview + meta -->
      <div class="flex-1 min-w-0 px-6 flex flex-col justify-center">
        <div class="flex items-center justify-between">
          <h3 class="text-[15px] font-medium text-white/95 truncate">{{ template.title }}</h3>
          <button class="w-8 h-8 flex items-center justify-center rounded-md hover:bg-white/5 text-gray-300 hover:text-white ml-3" @click.stop="expanded = !expanded" aria-label="Развернуть">
            <i :class="['fas fa-chevron-down text-[13px] leading-none', { 'rotate-180': expanded }]" style="transition: none;"></i>
          </button>
        </div>
        <!-- previewText удалён -->
        <div class="text-[11px] text-gray-500/90">
          {{ linesCount }} строк
        </div>
      </div>

      <!-- Right: actions -->
      <div class="flex items-center gap-2 w-[160px] justify-end flex-shrink-0 pr-1">
        <button @click.stop="copyAll" class="w-8 h-8 flex items-center justify-center rounded-md btn-glass text-gray-300 hover:text-white" aria-label="Копировать всё">
          <i class="fas fa-copy"></i>
        </button>
        <button @click.stop="emit('edit')" class="w-8 h-8 flex items-center justify-center rounded-md btn-glass text-gray-300 hover:text-white" aria-label="Редактировать">
          <i class="fas fa-edit"></i>
        </button>
        <button @click.stop="emit('delete')" class="w-8 h-8 flex items-center justify-center rounded-md btn-glass text-red-300 hover:text-white" aria-label="Удалить">
          <i class="fas fa-trash-alt"></i>
        </button>
      </div>
    </div>

    <Transition name="expand-fade">
      <div v-show="expanded" class="expanded-content mx-5 mb-5 mt-0 p-4 rounded-xl bg-white/5 border border-white/10">
        <div class="content-area space-y-1.5 max-h-[750px] overflow-y-auto">
          <template v-for="(line, lineIndex) in contentLines" :key="lineIndex">
            <!-- НЕКОПИРУЕМАЯ ПОДСКАЗКА: строки, начинающиеся с #p -->
            <div v-if="line.isAnnotation" class="select-none pointer-events-none">
              <div class="relative p-2.5 rounded-lg text-[12px] leading-5 bg-white/5 border border-white/10 text-amber-300/90">
                {{ line.display }}
              </div>
            </div>
            <!-- КОПИРУЕМАЯ СТРОКА -->
            <div v-else
                 @click="toggleCopy(lineIndex, line.copy)"
                 :class="['relative group p-2.5 rounded-lg cursor-pointer select-none', 'hover:bg-white/10', copied.has(lineIndex) ? 'copied-highlight' : '']"
                 title="Нажмите, чтобы скопировать строку">
              <div class="flex items-center">
                <span class="w-6 h-6 flex-shrink-0 flex items-center justify-center rounded-md bg-white/10 text-gray-300 text-xs font-mono border border-white/10 mr-2.5">{{ lineIndex + 1 }}</span>
                <span class="text-gray-300/90 font-mono text-[13px] break-words flex-1">{{ line.display }}</span>
                <span class="hidden group-hover:flex ml-2 text-[11px] text-gray-300 bg-white/10 px-2 py-1 rounded-md">
                  <i class="fas fa-copy mr-1"></i> Копировать
                </span>
              </div>
              <div v-show="copied.has(lineIndex)" class="absolute right-2 top-1/2 -translate-y-1/2 text-green-400/90 bg-green-500/20 px-3 py-1 rounded-lg backdrop-blur-sm border border-green-500/20 text-xs font-semibold shadow-lg">
                <i class="fas fa-check mr-1"></i> Скопировано!
              </div>
            </div>
          </template>
        </div>
      </div>
    </Transition>
  </div>
 </template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { copyText } from '../utils/clipboard'

interface TemplateDto {
  id: number
  title: string
  category: string
  content: string
  created_at: string
  updated_at: string
  lines_count?: number
}

const props = defineProps<{ template: TemplateDto; index: number }>()
const emit = defineEmits<{ (e: 'edit'): void; (e: 'delete'): void }>()

const expanded = ref(false)
const copied = ref<Set<number>>(new Set())

// Вычисляем строки только при раскрытии, чтобы не тратить CPU на большие списки
const contentLines = computed(() => {
  if (!expanded.value) return [] as Array<{ isAnnotation: boolean; display: string; copy: string }>
  // Преобразуем строки: '#p ...' — это подсказка (не копируется)
  return props.template.content
    .split('\n')
    .map(raw => raw.replace(/[\u00A0\s]+/g, ' ').replace(/^[\s\t]+|[\s\t]+$/g, ''))
    .filter(l => /\S/.test(l))
    .map(line => {
      if (line.startsWith('#p ')) {
        return { isAnnotation: true, display: line.slice(3), copy: '' }
      }
      return { isAnnotation: false, display: line, copy: line }
    })
})
const linesCount = computed(() => {
  const provided = props.template.lines_count
  if (typeof provided === 'number') return provided
  return contentLines.value.filter(l => !l.isAnnotation).length
})
const previewText = computed(() => {
  const text = props.template.content || ''
  const n = text.indexOf('\n')
  const first = n === -1 ? text : text.slice(0, n)
  return first.length > 80 ? first.slice(0, 80) + '…' : first
})

const formattedUpdated = computed(() => {
  const dt = new Date(props.template.updated_at)
  const diffMs = Date.now() - dt.getTime()
  const mins = Math.floor(diffMs / 60000)
  if (mins < 60) return `${mins} мин назад`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs} ч назад`
  const days = Math.floor(hrs / 24)
  return `${days} дн назад`
})

async function toggleCopy(idx: number, line: string) {
  const ok = await copyText(line)
  if (ok) {
    if (copied.value.has(idx)) {
      copied.value.delete(idx)
    } else {
      copied.value.add(idx)
    }
  }
}

async function copyAll() {
  const ok = await copyText(props.template.content)
  if (ok) {
    // Tiny pulse feedback could be added via class toggle if needed
  }
}
</script>


