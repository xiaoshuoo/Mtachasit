import axios from 'axios'

// Функция для динамического определения API URL
function getApiBaseUrl() {
  const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  return isLocalhost 
    ? 'http://localhost:8000/api/' 
    : 'https://mtachasit.onrender.com/api/'
}

// Создаем axios instance с динамическим baseURL
export const api = axios.create({
  headers: { 'Content-Type': 'application/json' },
})

// Перехватчик для динамического обновления baseURL
api.interceptors.request.use((config) => {
  config.baseURL = getApiBaseUrl()
  console.log('🌐 API Base URL:', config.baseURL)
  console.log('🔧 Environment:', window.location.hostname === 'localhost' ? 'LOCAL' : 'PRODUCTION')
  return config
})

// Optional: JWT auth helpers for you personally
export function setAuthToken(token: string | null) {
  if (token) api.defaults.headers.Authorization = `Bearer ${token}`
  else delete api.defaults.headers.Authorization
}

export const authApi = {
  async login(username: string, password: string) {
    const res = await api.post('token/', { username, password })
    const { access, refresh } = res.data
    try { localStorage.setItem('accessToken', access); localStorage.setItem('refreshToken', refresh) } catch {}
    setAuthToken(access)
    return res.data
  },
  async refresh(refresh: string) {
    const res = await api.post('token/refresh/', { refresh })
    const { access } = res.data
    try { localStorage.setItem('accessToken', access) } catch {}
    setAuthToken(access)
    return res.data
  },
  logout() {
    try { localStorage.removeItem('accessToken'); localStorage.removeItem('refreshToken') } catch {}
    setAuthToken(null)
  }
}

// Сброс битого токена на 401 для публичных списков лекций
api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const status = error?.response?.status
    const config = error?.config || {}
    if (status === 401 && !config.__isRetry) {
      // Drop broken token and retry once without Authorization
      try {
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
      } catch {}
      setAuthToken(null)
      config.__isRetry = true
      return api.request(config)
    }
    return Promise.reject(error)
  }
)

// инициализируем токен при загрузке фронта
try {
  const boot = localStorage.getItem('accessToken')
  if (boot) setAuthToken(boot)
} catch {}

export const templateApi = {
  getAll: (params?: Record<string, any>) => api.get('templates/', { params }),
  getById: (id: number) => api.get(`templates/${id}/`),
  create: async (data: any) => {
    console.log('📤 Creating template with data:', data)
    const response = await api.post('templates/', data)
    console.log('✅ Template created successfully:', response.data)
    return response
  },
  update: async (id: number, data: any) => {
    console.log('📤 Updating template', id, 'with data:', data)
    const response = await api.put(`templates/${id}/`, data)
    console.log('✅ Template updated successfully:', response.data)
    return response
  },
  delete: (id: number) => api.delete(`templates/${id}/`),
  getCategories: (params?: Record<string, any>) => api.get('templates/categories/', { params }),
}

export const rossiTemplateApi = {
  getAll: (params?: Record<string, any>) => api.get('templates-rossi/', { params }),
  getById: (id: number) => api.get(`templates-rossi/${id}/`),
  create: async (data: any) => {
    console.log('📤 Creating Rossi template with data:', data)
    const response = await api.post('templates-rossi/', data)
    console.log('✅ Rossi template created successfully:', response.data)
    return response
  },
  update: async (id: number, data: any) => {
    console.log('📤 Updating Rossi template', id, 'with data:', data)
    const response = await api.put(`templates-rossi/${id}/`, data)
    console.log('✅ Rossi template updated successfully:', response.data)
    return response
  },
  delete: (id: number) => api.delete(`templates-rossi/${id}/`),
  getCategories: () => api.get('templates-rossi/categories/'),
}

export const lecturesApi = {
  async counts(){
    const res = await api.get('lecture-categories/with_counts/')
    return res.data
  },
  async listLectures() {
    const res = await api.get('lectures/')
    return res.data
  },
  async listLectureItems(params?: any) {
    const res = await api.get('lectures/', { params })
    return res.data
  },
  async listCategories() {
    const res = await api.get('lecture-categories/')
    return res.data
  },
  async createCategory(payload: any) {
    const res = await api.post('lecture-categories/', payload)
    return res.data
  },
  async createLecture(payload: any) {
    const res = await api.post('lectures/', payload)
    return res.data
  },
  async updateLecture(id: number, payload: any) {
    const res = await api.put(`lectures/${id}/`, payload)
    return res.data
  },
  async deleteLecture(id: number) {
    const res = await api.delete(`lectures/${id}/`)
    return res.data
  }
}


