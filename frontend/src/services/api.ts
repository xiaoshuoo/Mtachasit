import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: { 'Content-Type': 'application/json' },
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
  create: (data: any) => api.post('templates/', data),
  update: (id: number, data: any) => api.put(`templates/${id}/`, data),
  delete: (id: number) => api.delete(`templates/${id}/`),
  getCategories: (params?: Record<string, any>) => api.get('templates/categories/', { params }),
}

export const rossiTemplateApi = {
  getAll: (params?: Record<string, any>) => api.get('templates-rossi/', { params }),
  getById: (id: number) => api.get(`templates-rossi/${id}/`),
  create: (data: any) => api.post('templates-rossi/', data),
  update: (id: number, data: any) => api.put(`templates-rossi/${id}/`, data),
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


