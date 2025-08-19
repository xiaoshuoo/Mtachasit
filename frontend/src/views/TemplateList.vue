<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="header mb-6 pl-4 pr-4">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div class="flex items-center gap-3 min-w-0">
          <AnimatedIcon icon="fas fa-file-alt" title="Templates" />
          <div class="min-w-0">
            <h1 class="text-2xl lg:text-3xl font-semibold text-slate-100 truncate">Шаблоны текстов Gutierrez</h1>
            <p class="text-gray-400 mt-0.5">Управление текстовыми шаблонами</p>
          </div>
        </div>

        <div class="flex items-center gap-3 lg:gap-4">
          <div class="search-bar w-[240px] lg:w-[320px]">
            <SearchInput v-model="searchQuery" placeholder="Поиск шаблонов..." />
          </div>
          <NeonButton @click="goNew" class="ml-0">Добавить шаблон</NeonButton>
        </div>
      </div>
      <!-- quick links removed per request -->
    </div>

    <!-- Mobile categories select -->
    <div class="lg:hidden">
      <select v-model="activeCategory" class="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl text-white appearance-none">
        <option value="all">Все категории</option>
        <option v-for="cat in categories" :key="cat.slug" :value="cat.slug">{{ cat.name }} ({{ cat.count }})</option>
      </select>
    </div>

    <!-- Main grid -->
    <div class="grid grid-cols-1 lg:grid-cols-[168px_minmax(0,1fr)] gap-6 px-4">
      <div class="sticky top-0 self-start pr-2">
        <CategorySidebar :categories="categories" :active="activeCategory" :total-count="total" @select="(c) => (activeCategory = c)" />
      </div>
      <div class="space-y-6 main-content max-w-[1800px]">
        <div v-if="loading" class="text-slate-300">Загрузка...</div>
        <template v-else>
          <div v-if="filteredTemplates.length === 0" class="text-slate-300">Ничего не найдено</div>
          <div v-else class="space-y-6 max-w-none">
            <div v-for="slug in orderedGroupSlugs" :key="slug">
              <!-- Folder section only if there are 2+ templates in the category -->
              <div v-if="groupedTemplates[slug].items.length >= 2" class="category-section glass-element rounded-xl border-glass overflow-hidden">
                <!-- Group header -->
                <div class="category-header flex items-center justify-between px-4 sm:px-6 py-2.5 cursor-pointer select-none" @click="toggleGroup(slug)">
                  <div class="flex items-center gap-3 min-w-0">
                    <span class="w-7 h-7 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-slate-300 flex-shrink-0">
                      <i class="fas fa-folder"></i>
                    </span>
                    <h2 class="text-white font-semibold text-[16px] lg:text-[18px] truncate">{{ groupedTemplates[slug].name }}</h2>
                  </div>
                  <div class="flex items-center gap-3">
                    <span class="category-badge">{{ groupedTemplates[slug].items.length }}</span>
                    <i :class="['fas fa-chevron-down text-gray-300', { 'rotate-180': !isCollapsed(slug) }]" style="transition: none;"></i>
                  </div>
                </div>
                <!-- Group body -->
                <div v-show="!isCollapsed(slug)" class="px-4 sm:px-6 pb-4 space-y-3">
                  <TemplateCard v-for="(t, idx) in groupedTemplates[slug].items" :key="t.id" :template="t" :index="idx + 1" @edit="goEdit(t.id)" @delete="remove(t.id)" />
                </div>
              </div>
              <!-- If only one template in the category, show it directly without a folder header -->
              <div v-else class="space-y-3">
                <TemplateCard v-for="(t, idx) in groupedTemplates[slug].items" :key="t.id" :template="t" :index="idx + 1" @edit="goEdit(t.id)" @delete="remove(t.id)" />
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { templateApi, rossiTemplateApi } from '../services/api'
import CategorySidebar from '../components/CategorySidebar.vue'
import TemplateCard from '../components/TemplateCard.vue'
import { useRouter } from 'vue-router'
import NeonButton from '../components/UI/NeonButton.vue'
import AnimatedIcon from '../components/UI/AnimatedIcon.vue'
import SearchInput from '../components/UI/SearchInput.vue'

interface TemplateDto {
  id: number
  title: string
  category: string
  content: string
  created_at: string
  updated_at: string
}

interface TemplateView extends TemplateDto {
  titleLower: string
  categorySlug: string
}

const router = useRouter()
const route = useRoute()
const templates = ref<TemplateView[]>([])
const categories = ref<Array<{ name: string; slug: string; count: number }>>([])
const total = ref(0)
const loading = ref(false)

const searchQuery = ref('')
const debouncedQuery = ref('')
let debounceTimer: number | undefined
watch(searchQuery, (v) => {
  clearTimeout(debounceTimer)
  debounceTimer = window.setTimeout(() => (debouncedQuery.value = v), 200)
})
const activeCategory = ref('all')
const pageType = ref<'all' | 'rossi' | 'gutierrez-public'>('all')

const filteredTemplates = computed(() => {
  let list = templates.value
  if (activeCategory.value !== 'all') {
    list = list.filter(t => t.categorySlug === activeCategory.value)
  }
  // Фильтрация по типу страницы
  // Для Rossi мы уже получаем данные с отдельного эндпоинта, дополнительная фильтрация не нужна
  if (pageType.value === 'gutierrez-public') {
    list = list.filter((t:any) => (t as any).created_by_id == null)
  }
  if (debouncedQuery.value) {
    list = list.filter(t => t.titleLower.includes(debouncedQuery.value.toLowerCase()))
  }
  return list
})

function toSlug(value: string): string {
  return String(value || '').toLowerCase().trim().replace(/\s+/g, '-')
}

const groupedTemplates = computed(() => {
  const groups: Record<string, { name: string; items: TemplateView[] }> = {}
  for (const t of filteredTemplates.value) {
    const name = t.category || 'Без категории'
    const slug = t.categorySlug || toSlug(name)
    if (!groups[slug]) groups[slug] = { name, items: [] }
    groups[slug].items.push(t)
  }
  return groups
})

const collapsedGroups = ref<Set<string>>(new Set())
function isCollapsed(slug: string): boolean { return collapsedGroups.value.has(slug) }
function toggleGroup(slug: string) {
  if (collapsedGroups.value.has(slug)) collapsedGroups.value.delete(slug)
  else collapsedGroups.value.add(slug)
}

const orderedGroupSlugs = computed(() => {
  const available = groupedTemplates.value
  const slugs = Object.keys(available)
  if (activeCategory.value !== 'all') return slugs.filter(s => s === activeCategory.value)
  const ordered: string[] = []
  for (const c of categories.value) {
    if (available[c.slug]) ordered.push(c.slug)
  }
  for (const s of slugs) if (!ordered.includes(s)) ordered.push(s)
  return ordered
})

async function fetchTemplates() {
  loading.value = true
  try {
    const apiSet = pageType.value === 'rossi' ? rossiTemplateApi : templateApi
    const params: any = {}
    if (pageType.value === 'gutierrez-public') {
      params.created_by_id = 'null'
    } else if (pageType.value === 'all') {
      params.created_by_id = 1
    }
    const [tplAll, catRes] = await Promise.all([
      fetchAllTemplates(apiSet),
      apiSet.getCategories(params)
    ])
    templates.value = tplAll.map((t: any) => ({
      ...t,
      titleLower: (t.title || '').toLowerCase(),
      categorySlug: toSlug(t.category || 'Без категории'),
    }))
    total.value = tplAll.length
    categories.value = (catRes.data || []).map((c: any) => ({
      name: c.category || 'Без категории',
      slug: toSlug(c.category || ''),
      count: c.count ?? 0,
    }))
  } finally {
    loading.value = false
  }
}

async function fetchAllTemplates(apiSet = templateApi): Promise<TemplateDto[]> {
  const pageSize = 100
  const items: TemplateDto[] = []
  let page = 1
  let params: any = { page, page_size: pageSize }
  // Добавляем фильтрацию по created_by_id для нужных страниц
  if (pageType.value === 'gutierrez-public') {
    params.created_by_id = 'null'
  } else if (pageType.value === 'all') {
    params.created_by_id = 1
  }
  while (true) {
    params.page = page
    const res = await apiSet.getAll(params)
    const data = res.data
    const batch: TemplateDto[] = data.results ?? data
    items.push(...batch)
    const hasNext = Boolean(data.next) && batch.length > 0
    if (!hasNext) break
    page += 1
  }
  return items
}

async function remove(id: number) {
  await templateApi.delete(id)
  await fetchTemplates()
}

function goEdit(id: number) {
  router.push({ name: 'edit', params: { id } })
}

function goNew() {
  router.push({ name: 'new' })
}

onMounted(() => {
  const name = (route as any)?.name as string | undefined
  if (name === 'templates-rossi') pageType.value = 'rossi'
  else if (name === 'templates-gutierrez-public') pageType.value = 'gutierrez-public'
  fetchTemplates()
})
</script>


