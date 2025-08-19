<template>
  <div class="space-y-6 px-4 sm:px-6 lg:px-8">
    <div class="header mb-6 flex items-center justify-between lg:ml-[168px] pr-4">
      <div class="flex items-center space-x-6">
        <AnimatedIcon icon="fas fa-chalkboard-teacher" title="Lectures" />
        <div>
          <h1 class="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 animate-gradient">Лекции</h1>
          <p class="text-gray-400 mt-1">Управление лекциями</p>
        </div>
      </div>
      <div class="flex flex-col items-end gap-2">
        <div class="flex items-center space-x-4">
          <div class="search-bar">
            <SearchInput v-model="searchQuery" placeholder="Поиск лекций..." />
          </div>
          <NeonButton @click="showCreateModal = true">Создать лекцию</NeonButton>
          <NeonButton as="label" class="relative overflow-hidden cursor-pointer">
            <input type="file" class="absolute inset-0 opacity-0 cursor-pointer" accept=".txt" @change="onImportFile" />
            Импорт .txt
          </NeonButton>
        </div>
        <div class="flex items-center gap-2 mt-1">
          <label class="text-gray-400 text-xs">Строк от</label>
          <div class="relative flex items-center">
            <input type="number" v-model.number="minLines" min="0" class="w-14 px-2 py-1 rounded-l bg-black/20 border border-white/10 text-white text-xs focus:z-10" />
            <button @click="toggleSortOrder" class="sort-btn px-2 py-1 rounded-r border border-l-0 border-white/10 bg-black/20 text-gray-300 hover:text-white focus:z-10 transition-colors duration-150 flex items-center justify-center"
              :aria-label="sortOrder === 'asc' ? 'Сортировать по возрастанию' : 'Сортировать по убыванию'"
              :title="sortOrder === 'asc' ? 'Сортировать по возрастанию' : 'Сортировать по убыванию'">
              <i :class="['fas', sortOrder === 'asc' ? 'fa-sort-numeric-up' : 'fa-sort-numeric-down', 'transition-transform duration-200']"
                :style="{ transform: sortOrder === 'asc' ? 'rotate(0deg)' : 'rotate(180deg)' }"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-[220px_minmax(0,1fr)] gap-6 px-4">
      <aside class="glass-element rounded-2xl p-4 border-glass shadow-glass h-max sticky top-6">
        <div class="text-white/90 font-semibold mb-2 flex items-center gap-2"><i class="fas fa-book"></i> Лекции</div>
        <div v-for="c in uiCategories" :key="c.slug" @click="activeCategory = c.slug"
             class="flex items-center gap-3 px-3 py-2 rounded-xl hover:bg-white/5 transition cursor-pointer"
             :class="{ 'bg-white/5 font-semibold': activeCategory === c.slug || (c.slug==='all' && activeCategory==='all') }">
          <i :class="[c.icon, 'text-gray-300']"></i>
          <span class="truncate">{{ c.name }}</span>
        </div>
      </aside>
      <div class="space-y-6 max-w-[1800px]">
        <div v-if="loading" class="text-slate-300">Загрузка...</div>
        <template v-else>
          <div v-if="grouped.length === 0" class="text-slate-300">Ничего не найдено</div>
          <div v-else class="space-y-6">
            <div v-for="group in grouped" :key="group.slug" class="glass-element rounded-xl border-glass overflow-hidden bg-[rgba(26,22,37,0.60)]">
              <div class="category-header flex items-center justify-between px-4 sm:px-6 py-3">
                <div class="flex items-center gap-3 min-w-0">
                  <span class="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-gray-300 flex-shrink-0">
                    <i class="fas fa-folder"></i>
                  </span>
                  <h2 class="text-white font-semibold text-[18px] truncate">{{ group.name }}</h2>
                </div>
          <span class="category-badge">{{ group.items.length }}</span>
              </div>
              <div class="px-4 sm:px-6 pb-2 space-y-2 will-change-transform">
                <TemplateCard v-for="(t, idx) in group.items" :key="t.id" :template="mapTemplate(t)" :index="idx + 1"
                  class="smaller-card" @edit="openEdit(t)" @delete="confirmDelete(t)" />
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="glass-element w-full max-w-2xl rounded-2xl p-6 border-glass shadow-glass">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-semibold">{{ editId ? 'Редактировать лекцию' : 'Создать лекцию' }}</h3>
        <button class="text-gray-400 hover:text-white" @click="closeModal"><i class="fas fa-times"></i></button>
      </div>
      <form @submit.prevent="submitLecture" class="space-y-4">
        <div>
          <label class="block text-sm text-gray-300 mb-1">Название</label>
          <input v-model.trim="form.title" required class="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl text-white focus:border-white/30" />
        </div>
        <div>
          <label class="block text-sm text-gray-300 mb-1">Категория (необязательно)</label>
            <div class="relative">
              <input v-model.trim="categoryQuery" placeholder="Поиск категории..." class="w-full mb-2 px-4 py-2 bg-black/20 border border-white/10 rounded-lg text-white" />
              <button type="button" class="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl text-white flex items-center justify-between hover:border-white/30"
                      @click="categoryMenuOpen = !categoryMenuOpen">
                <span class="truncate">{{ selectedCategoryLabel }}</span>
                <i :class="['fas fa-chevron-down transition-transform', { 'rotate-180': categoryMenuOpen }]" />
              </button>
              <div v-if="categoryMenuOpen" class="absolute z-50 mt-2 w-full glass-element rounded-xl border-glass shadow-glass p-2" @click.stop>
                <div class="dropdown-group">
                  <div class="dropdown-heading">Рекомендуемые</div>
                  <div class="dropdown-item" @click="selectCategory(null)">
                    <i class="fas fa-ban opacity-70 mr-2"></i> Без категории
                  </div>
                  <div class="dropdown-item" v-for="r in filteredRecommended" :key="r.slug" @click="selectCategory(r.slug)">
                    <i class="fas fa-star text-gray-300 mr-2"></i> {{ r.name }}
                  </div>
                </div>
                <div class="dropdown-divider"></div>
                <div class="dropdown-group">
                  <div class="dropdown-heading">Все категории</div>
                  <div class="dropdown-item" v-for="c in filteredCategories" :key="c.slug" @click="selectCategory(c.id)">
                    <i class="fas fa-folder text-gray-300 mr-2"></i> {{ c.name }}
                  </div>
                </div>
              </div>
            </div>
        </div>
        <div>
          <label class="block text-sm text-gray-300 mb-1">Содержание</label>
          <textarea v-model="form.content" rows="10" required class="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl text-white font-mono" placeholder="say Первая строка...\nsay Вторая строка..."></textarea>
          <p class="text-xs text-gray-400 mt-1">Каждая строка должна начинаться с ‘say ’ или ‘/b ’.</p>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button type="button" class="neon-button" @click="closeModal">Отмена</button>
          <NeonButton type="submit">Сохранить</NeonButton>
        </div>
      </form>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { lecturesApi, api } from '@/services/api'
import AnimatedIcon from '@/components/UI/AnimatedIcon.vue'
import SearchInput from '@/components/UI/SearchInput.vue'
import CategorySidebar from '@/components/CategorySidebar.vue'
import TemplateCard from '@/components/TemplateCard.vue'
import NeonButton from '@/components/UI/NeonButton.vue'

interface LectureDto { id:number; title:string; content:string; category?: { id:number; name:string; slug:string } | null }

const lectures = ref<LectureDto[]>([])
const categories = ref<Array<{ id:number; name:string; slug:string; count: number }>>([])
const loading = ref(false)
const searchQuery = ref('')
const activeCategory = ref('all')
const total = ref(0)
const showCreateModal = ref(false)
const editId = ref<number | null>(null)
const form = ref<{ title:string; content:string; category_id: number | string | null }>({ title:'', content:'', category_id: null })
const categoryQuery = ref('')
const categoryMenuOpen = ref(false)
const minLines = ref(0)
const sortOrder = ref<'asc' | 'desc'>('asc')
function toggleSortOrder() {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
}

function toSlug(v:string){ return (v||'').toLowerCase().trim().replace(/\s+/g,'-') }
function canonicalSlug(slug:string){
  const map:Record<string,string> = { 'zabolevaniya':'zabolevanija', 'pervaya-pomoshch':'pervaja-pomosch' }
  return map[slug] || slug
}

const filtered = computed(() => {
  let list = lectures.value;
  if (activeCategory.value !== 'all') {
    list = list.filter(t => canonicalSlug(t.category?.slug || '') === activeCategory.value);
  }
  if (searchQuery.value) {
    list = list.filter(t => t.title.toLowerCase().includes(searchQuery.value.toLowerCase()));
  }
  const min = minLines.value || 0;
  if (min > 0) list = list.filter(t => countVisibleLines(t.content) >= min);
  // сортировка по количеству строк
  list = list.slice().sort((a, b) => {
    const aLines = countVisibleLines(a.content);
    const bLines = countVisibleLines(b.content);
    return sortOrder.value === 'asc' ? aLines - bLines : bLines - aLines;
  });
  return list;
});

const grouped = computed(() => {
  const m = {};
  for (const t of filtered.value) {
    const name = t.category?.name || 'Без категории';
    const slug = toSlug(t.category?.slug || name);
    if (!m[slug]) m[slug] = { name, slug, items: [] };
    m[slug].items.push(t);
  }
  return Object.values(m);
});

const filteredCategories = computed(()=>{
  if(!categoryQuery.value.trim()) return categories.value
  const q = categoryQuery.value.toLowerCase()
  return categories.value.filter(c => c.name.toLowerCase().includes(q))
})

const recommended = ref([
  { name:'Для МВД', slug:'dlya-mvd' },
  { name:'Другое', slug:'drugoe' },
  { name:'Заболевания', slug:'zabolevanija' },
  { name:'Первая помощь', slug:'pervaja-pomosch' },
])

const filteredRecommended = computed(()=>{
  if(!categoryQuery.value.trim()) return recommended.value
  const q = categoryQuery.value.toLowerCase()
  return recommended.value.filter(c => c.name.toLowerCase().includes(q))
})

function countVisibleLines(content: string): number{
  return (content || '')
    .split('\n')
    .map(l => l.replace(/[\u00A0\s]+/g, ' ').replace(/^[\s\t]+|[\s\t]+$/g, ''))
    .filter(l => /\S/.test(l)).length
}

function mapTemplate(l:LectureDto){
  return { id:l.id, title:l.title, content:l.content, updated_at:new Date().toISOString(), lines_count: countVisibleLines(l.content) }
}

async function fetchAll(path: string){
  const out:any[] = []
  let url: string | null = path
  while (url) {
    const res = await api.get(url)
    const data = res.data
    if (Array.isArray(data)) { out.push(...data); break }
    out.push(...(data.results || []))
    url = data.next
  }
  return out
}

async function load(){
  loading.value = true
  try{
    const [items, cats, agg] = await Promise.all([
      fetchAll('lectures/'),
      fetchAll('lecture-categories/'),
      fetchAll('lecture-categories/with_counts/')
    ])
    lectures.value = items
    const countBySlug:Record<string,number> = {}
    for(const a of agg){
      const s = canonicalSlug(a['category__slug'] || '')
      if (!s) continue
      countBySlug[s] = a['count'] || 0
    }
    categories.value = cats.map((c:any)=>({ id:c.id, name:c.name, slug: canonicalSlug(c.slug), count: countBySlug[canonicalSlug(c.slug)] ?? 0 }))
    total.value = lectures.value.length
  } finally {
    loading.value = false
  }
}

onMounted(load)

function closeModal(){ showCreateModal.value = false; editId.value = null; form.value = { title:'', content:'', category_id: null } }
async function submitLecture(){
  if(!form.value.title.trim() || !form.value.content.trim()) return
  try{
    const payload:any = { title: form.value.title.trim(), content: form.value.content }
    const catId = await resolveCategoryId(form.value.category_id)
    if(catId) payload.category_id = catId
    if(editId.value){ await lecturesApi.updateLecture(editId.value, payload) }
    else { await lecturesApi.createLecture(payload) }
    closeModal(); await load()
  }catch(e){ console.error(e) }
}

function openEdit(t: LectureDto){
  editId.value = t.id
  form.value.title = t.title
  form.value.content = t.content
  form.value.category_id = (t.category?.id ?? null) as any
  showCreateModal.value = true
}

async function confirmDelete(t: LectureDto){
  if(!confirm(`Удалить лекцию «${t.title}»?`)) return
  try{ await lecturesApi.deleteLecture(t.id); await load() } catch(e){ console.error(e) }
}

async function resolveCategoryId(sel: number | string | null): Promise<number | null>{
  if(sel === null || sel === undefined) return null
  if(typeof sel === 'number') return sel
  // string slug from recommended
  const found = categories.value.find(c => c.slug === sel)
  if(found) return found.id
  const rec = recommended.value.find(r => r.slug === sel)
  const name = rec?.name || sel
  try{
    const created = await lecturesApi.createCategory({ name, slug: sel })
    // Update local categories list
    categories.value.push({ id: created.id, name: created.name, slug: created.slug })
    return created.id
  }catch(e){ console.error(e); return null }
}
// Import single .txt file
async function onImportFile(e: Event){
  const input = e.target as HTMLInputElement
  if(!input.files || input.files.length===0) return
  const file = input.files[0]
  try{
    const text = await file.text()
    await lecturesApi.createLecture({ title: file.name.replace(/\.txt$/i,''), content: text })
    await load()
  }catch(err){ console.error(err) }
  input.value = ''
}

const uiCategories = computed(()=>{
  const base = [
    { name: 'Все лекции', slug:'all', icon:'fas fa-border-all' },
    { name: 'Для МВД', slug:'dlya-mvd', icon:'fas fa-shield-halved' },
    { name: 'Другое', slug:'drugoe', icon:'fas fa-screwdriver-wrench' },
    { name: 'Заболевания', slug:'zabolevanija', icon:'fas fa-circle-plus' },
    { name: 'Первая помощь', slug:'pervaja-pomosch', icon:'fas fa-briefcase-medical' },
  ]
  const baseSet = new Set(base.map(b => b.slug))
  const dynamic = categories.value
    .map(c => ({ ...c, slug: canonicalSlug(c.slug) }))
    .filter(c => c.count > 0 && !baseSet.has(c.slug))
    .map(c => ({ name:c.name, slug:c.slug, icon:'fas fa-folder' }))
  return base.concat(dynamic)
})

const selectedCategoryLabel = computed(()=>{
  if(form.value.category_id === null) return 'Без категории'
  if(typeof form.value.category_id === 'string'){
    const r = recommended.value.find(x=>x.slug===form.value.category_id)
    return r?.name || form.value.category_id
  }
  const f = categories.value.find(x=>x.id===form.value.category_id)
  return f?.name || 'Без категории'
})

function selectCategory(val: number | string | null){
  form.value.category_id = val
  categoryMenuOpen.value = false
}
</script>

<style scoped>
.category-header{ border-bottom:1px solid var(--glass-border); background: rgba(255,255,255,0.02) }
.smaller-card :deep(.template-row){ height:58px !important }
.smaller-card :deep(h3){ font-size:14px !important }
.smaller-card :deep(.w-10.h-10){ width:28px !important; height:28px !important; font-size:12px !important }
.smaller-card :deep(.w-8.h-8){ width:28px !important; height:28px !important }
.smaller-card :deep(.expanded-content){ padding:12px !important; border-radius:12px !important }
.sort-btn {
  margin-left: -1px;
  border-top-left-radius: 0 !important;
  border-bottom-left-radius: 0 !important;
  border-top-right-radius: 6px !important;
  border-bottom-right-radius: 6px !important;
  background: rgba(0,0,0,0.18);
  cursor: pointer;
  transition: background 0.18s, color 0.18s;
}
.sort-btn:hover, .sort-btn:focus {
  background: rgba(139,92,246,0.18);
  color: #fff;
}
</style>


