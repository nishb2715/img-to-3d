const API_BASE = '/api'

export async function generateScene(file, detailLevel) {
  const form = new FormData()
  form.append('file', file)
  form.append('detail_level', detailLevel)
  const res = await fetch(`${API_BASE}/generate-3d`, { method: 'POST', body: form })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

export async function editScene(scene, prompt) {
  const res = await fetch(`${API_BASE}/edit-scene`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scene, prompt })
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}