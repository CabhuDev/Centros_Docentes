import { useState } from 'react'
import { geocode } from '../api'

export default function StartPoint({ origin, onSet }) {
  const [addr, setAddr] = useState('')
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState('')

  async function buscar(e) {
    e.preventDefault()
    if (!addr.trim()) return
    setLoading(true); setErr('')
    try {
      const r = await geocode(addr.trim())
      onSet({ lat: r.lat, lng: r.lng, label: r.formatted_address })
    } catch (e) {
      setErr(e.message)
    } finally {
      setLoading(false)
    }
  }

  function usarUbicacion() {
    if (!navigator.geolocation) { setErr('Tu navegador no permite geolocalización.'); return }
    setLoading(true); setErr('')
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        onSet({ lat: pos.coords.latitude, lng: pos.coords.longitude, label: 'Mi ubicación actual' })
        setLoading(false)
      },
      () => { setErr('No se pudo obtener tu ubicación.'); setLoading(false) },
    )
  }

  return (
    <div className="field">
      <label>📍 Punto de partida</label>
      <form className="row" onSubmit={buscar}>
        <input
          className="input"
          placeholder="Tu dirección o municipio…"
          value={addr}
          onChange={(e) => setAddr(e.target.value)}
        />
        <button className="btn" disabled={loading}>
          {loading ? <span className="spinner" /> : 'Buscar'}
        </button>
      </form>
      <button className="btn ghost sm" style={{ marginTop: 8 }} onClick={usarUbicacion} disabled={loading}>
        Usar mi ubicación actual
      </button>
      <div className="hint">…o haz clic en el mapa para fijar el punto.</div>
      {err && <div className="error">{err}</div>}
      {origin && (
        <div className="origin-pill">
          <span className="dot" />
          <span style={{ flex: 1 }}>{origin.label}</span>
          <button className="star" title="Quitar" onClick={() => onSet(null)} style={{ fontSize: 16 }}>✕</button>
        </div>
      )}
    </div>
  )
}
