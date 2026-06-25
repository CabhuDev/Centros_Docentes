// Cliente del backend. En dev, Vite redirige /api a FastAPI; en produccion,
// nginx hace de proxy a /api. Se puede sobreescribir con VITE_API_BASE.
const BASE = import.meta.env.VITE_API_BASE || ''

async function req(path, opts) {
  const r = await fetch(BASE + path, opts)
  if (!r.ok) {
    let detail = `Error ${r.status}`
    try { detail = (await r.json()).detail || detail } catch {}
    throw new Error(detail)
  }
  return r.json()
}

export function getMeta() {
  return req('/api/meta')
}

export function getCentros(params) {
  const sp = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === '') continue
    if (Array.isArray(v)) v.forEach((x) => sp.append(k, x))
    else sp.append(k, v)
  }
  return req('/api/centros?' + sp.toString())
}

export function geocode(address) {
  return req('/api/geocode', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ address }),
  })
}

export function getDistancias(origin, codigos, mode = 'driving') {
  return req('/api/distancias', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ origin, codigos, mode }),
  })
}

// Resuelve una lista de códigos a nombres/datos básicos.
export function lookup(codigos) {
  return req('/api/lookup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ codigos }),
  })
}

// Descarga el CSV (todos los campos de origen) de los centros indicados,
// en el orden dado. Devuelve un Blob.
export async function exportCsv(items, mode = 'driving') {
  const r = await fetch(BASE + '/api/export', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ items, mode }),
  })
  if (!r.ok) {
    let detail = `Error ${r.status}`
    try { detail = (await r.json()).detail || detail } catch {}
    throw new Error(detail)
  }
  return r.blob()
}
