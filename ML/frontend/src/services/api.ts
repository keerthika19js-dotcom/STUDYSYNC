const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
export function token() { return localStorage.getItem('studysync_token') }
export async function api<T = any>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers)
  if (options.body && !(options.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  if (token()) headers.set('Authorization', `Bearer ${token()}`)
  let response: Response
  try { response = await fetch(`${API_BASE}${path}`, { ...options, headers }) }
  catch { throw new Error('Could not reach STUDYSYNC. Check that the backend is running at localhost:8000.') }
  const body = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(body.detail || body.message || `Request failed (${response.status})`)
  return body as T
}
export function saveSession(data: {access_token:string; student:{student_id:string;name:string;email:string}}) {
  localStorage.setItem('studysync_token', data.access_token)
  localStorage.setItem('studysync_student', JSON.stringify(data.student))
}
export function clearSession() { localStorage.removeItem('studysync_token'); localStorage.removeItem('studysync_student') }
export function storedStudent() { try { return JSON.parse(localStorage.getItem('studysync_student') || 'null') } catch { return null } }
