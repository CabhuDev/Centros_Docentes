import { useState } from 'react'
import { exportCsv } from '../api'

export default function Preferences({ favs, move, remove, clear, drive, mode }) {
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')

  if (favs.length === 0) {
    return <div className="hint">Marca centros con ☆ para crear tu lista ordenada de preferencias.</div>
  }

  async function descargarCsv() {
    setBusy(true); setErr('')
    try {
      const items = favs.map((f) => {
        const d = drive[f.codigo]
        return {
          codigo: f.codigo,
          duration_text: d?.duration_text ?? null,
          distance_text: d?.distance_text ?? null,
          distancia_recta_km: f.distancia_recta_km ?? null,
        }
      })
      const blob = await exportCsv(items, mode)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'mis-centros-preferidos.csv'
      a.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      setErr(e.message)
    } finally {
      setBusy(false)
    }
  }

  function copiarLista() {
    const txt = favs.map((f, i) => {
      const d = drive[f.codigo]
      const extra = d ? ` — ${d.duration_text} (${d.distance_text})` : ''
      return `${i + 1}. [${f.codigo}] ${f.nombre} — ${f.municipio} (${f.provincia})${extra}`
    }).join('\n')
    navigator.clipboard?.writeText(txt)
  }

  return (
    <div className="prefs">
      {favs.map((f, i) => (
        <div className="pref-item" key={f.codigo}>
          <span className="num">{i + 1}</span>
          <span className="nm" title={f.nombre}>{f.nombre} · {f.municipio}</span>
          <span className="mv">
            <button title="Subir" onClick={() => move(i, -1)} disabled={i === 0}>▲</button>
            <button title="Bajar" onClick={() => move(i, 1)} disabled={i === favs.length - 1}>▼</button>
          </span>
          <button className="rm" title="Quitar" onClick={() => remove(f.codigo)}>✕</button>
        </div>
      ))}
      <div className="row" style={{ marginTop: 10 }}>
        <button className="btn sm" onClick={descargarCsv} disabled={busy}>
          {busy ? <span className="spinner" /> : '⬇ Descargar CSV'}
        </button>
        <button className="btn ghost sm" onClick={copiarLista}>Copiar</button>
        <button className="btn ghost sm" onClick={clear}>Vaciar</button>
      </div>
      <div className="hint">El CSV incluye todos los campos del directorio, en este orden.</div>
      {err && <div className="error">{err}</div>}
    </div>
  )
}
