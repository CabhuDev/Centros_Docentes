import { useEffect, useRef, useState } from 'react'
import { getCentros, lookup, exportCsv } from '../api'

// Extrae códigos de centro (8 dígitos) de un texto. Acepta el formato oficial
// con letra de tipo pegada (p. ej. "18700244C" del concurso de traslados) y los
// códigos sueltos. Evita confundirlos con números más largos (DNI de 8 dígitos
// puede colarse, pero se marcará como "no encontrado"). Quita duplicados.
// Prefijos de provincia (INE) de los centros de Andalucía. Sirve para descartar
// números de 8 dígitos que no son códigos de centro (DNI, nº de oficina…).
const PREFIJOS_PROV = new Set(['04', '11', '14', '18', '21', '23', '29', '41'])

function extraerCodigos(texto) {
  const out = []
  const vistos = new Set()
  // (^|no-dígito) + 8 dígitos + (no seguido de dígito). Sin lookbehind (compat.).
  const re = /(^|[^\d])(\d{7,8})(?!\d)/g
  let m
  while ((m = re.exec(texto)) !== null) {
    const cod = m[2].padStart(8, '0')   // Almería en Excel puede perder el 0
    if (PREFIJOS_PROV.has(cod.slice(0, 2)) && !vistos.has(cod)) {
      vistos.add(cod); out.push(cod)
    }
    re.lastIndex = m.index + m[0].length - 1  // permite códigos consecutivos
  }
  return out
}

// --- Lectura de ficheros: texto, PDF y Excel (librerías cargadas bajo demanda) ---
async function leerPdf(file) {
  const pdfjs = await import('pdfjs-dist')
  const workerUrl = (await import('pdfjs-dist/build/pdf.worker.min.mjs?url')).default
  pdfjs.GlobalWorkerOptions.workerSrc = workerUrl
  const buf = await file.arrayBuffer()
  const pdf = await pdfjs.getDocument({ data: buf }).promise
  let text = ''
  for (let p = 1; p <= pdf.numPages; p++) {
    const page = await pdf.getPage(p)
    const content = await page.getTextContent()
    text += content.items.map((i) => i.str).join(' ') + '\n'
  }
  return text
}

async function leerExcel(file) {
  const XLSX = await import('xlsx')
  const buf = await file.arrayBuffer()
  const wb = XLSX.read(buf, { type: 'array' })
  return wb.SheetNames.map((n) => XLSX.utils.sheet_to_csv(wb.Sheets[n])).join('\n')
}

async function leerFichero(file) {
  const ext = (file.name.split('.').pop() || '').toLowerCase()
  if (ext === 'pdf') return leerPdf(file)
  if (ext === 'xlsx' || ext === 'xls') return leerExcel(file)
  return file.text()
}

function descargar(nombre, texto, tipo = 'text/plain;charset=utf-8') {
  const blob = new Blob(['﻿' + texto], { type: tipo })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = nombre; a.click()
  URL.revokeObjectURL(url)
}

function Buscador({ etapaLabels }) {
  const [q, setQ] = useState('')
  const [res, setRes] = useState([])
  const [loading, setLoading] = useState(false)
  const t = useRef()

  useEffect(() => {
    clearTimeout(t.current)
    if (q.trim().length < 2) { setRes([]); return }
    t.current = setTimeout(async () => {
      setLoading(true)
      try {
        const r = await getCentros({ q: q.trim(), limit: 50 })
        setRes(r.items)
      } catch { /* ignore */ } finally { setLoading(false) }
    }, 250)
    return () => clearTimeout(t.current)
  }, [q])

  return (
    <section className="panel">
      <h2>Buscar centro</h2>
      <p className="muted">Por nombre o por código de centro.</p>
      <input
        className="input"
        placeholder="Ej.: Padre Suárez, IES Galileo, 18002991…"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        autoFocus
      />
      <div className="muted sm" style={{ margin: '8px 0' }}>
        {loading ? <span className="spinner" /> : q.trim().length >= 2 ? `${res.length} resultado(s)` : 'Escribe al menos 2 caracteres.'}
      </div>
      <div className="lookup-list">
        {res.map((c) => (
          <div className="lk-row" key={c.codigo}>
            <div>
              <div className="lk-name">{c.nombre || c.denominacion} <span className="code">{c.codigo}</span></div>
              <div className="muted sm">{c.denominacion} · {c.municipio} ({c.provincia}) · {c.titularidad}</div>
              <div className="badges">
                {c.etapas.map((e) => <span className="badge" key={e}>{etapaLabels[e] || e}</span>)}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

function Resolver() {
  const [texto, setTexto] = useState('')
  const [items, setItems] = useState(null)
  const [encontrados, setEncontrados] = useState(0)
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState('')
  const [fileName, setFileName] = useState('')

  const codigos = extraerCodigos(texto)

  async function resolver() {
    if (codigos.length === 0) { setErr('No se han detectado códigos (7-8 dígitos) en el texto.'); return }
    setErr(''); setLoading(true)
    try {
      const r = await lookup(codigos)
      setItems(r.items); setEncontrados(r.encontrados)
    } catch (e) { setErr(e.message) } finally { setLoading(false) }
  }

  async function onFile(e) {
    const f = e.target.files?.[0]
    if (!f) return
    setFileName(f.name); setErr(''); setItems(null); setLoading(true)
    try {
      const texto = await leerFichero(f)
      const cods = extraerCodigos(texto)
      // Para PDF/Excel mostramos directamente los códigos detectados (limpios);
      // para texto, dejamos el contenido tal cual por si quiere revisarlo.
      const ext = (f.name.split('.').pop() || '').toLowerCase()
      setTexto(['pdf', 'xlsx', 'xls'].includes(ext) ? cods.join('\n') : texto)
      if (cods.length === 0) setErr('No se han detectado códigos de centro (8 dígitos) en el fichero.')
    } catch (e) {
      setErr('No se pudo leer el fichero: ' + (e.message || e))
    } finally {
      setLoading(false)
      e.target.value = ''  // permite volver a subir el mismo fichero
    }
  }

  function copiarNombres() {
    const txt = items.filter((i) => i.encontrado).map((i) => i.nombre).join('\n')
    navigator.clipboard?.writeText(txt)
  }
  function descargarNombres() {
    const txt = items.map((i) => i.encontrado
      ? `${i.codigo}\t${i.nombre}\t${i.municipio} (${i.provincia})`
      : `${i.codigo}\t(no encontrado)`).join('\n')
    descargar('centros-nombres.txt', txt)
  }
  async function descargarCsv() {
    const its = items.filter((i) => i.encontrado).map((i) => ({ codigo: i.codigo }))
    if (its.length === 0) return
    const blob = await exportCsv(its)
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href = url; a.download = 'centros-listado.csv'; a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <section className="panel">
      <h2>Resolver listado</h2>
      <p className="muted">Pega un listado o sube un fichero (.txt, .csv, .xlsx, .pdf) con códigos de centro y te devuelvo los nombres. Detecta los códigos automáticamente, incluso en el PDF del concurso de traslados.</p>
      <textarea
        className="input area"
        rows={6}
        placeholder="Pega aquí los códigos (uno por línea, o mezclados con otro texto)…"
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
      />
      <div className="row" style={{ marginTop: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <label className="btn ghost sm" style={{ cursor: 'pointer' }}>
          Subir fichero…
          <input type="file" accept=".txt,.csv,.xlsx,.xls,.pdf" onChange={onFile} style={{ display: 'none' }} />
        </label>
        {fileName && <span className="muted sm">{fileName}</span>}
        <span className="muted sm">· {codigos.length} código(s) detectado(s)</span>
        <button className="btn sm" onClick={resolver} disabled={loading || codigos.length === 0}>
          {loading ? <span className="spinner" /> : 'Resolver nombres'}
        </button>
      </div>
      {err && <div className="error">{err}</div>}

      {items && (
        <div style={{ marginTop: 14 }}>
          <div className="muted sm" style={{ marginBottom: 8 }}>
            <b>{encontrados}</b> de {items.length} resueltos
            {items.length - encontrados > 0 && ` · ${items.length - encontrados} no encontrados`}
          </div>
          <div className="row" style={{ marginBottom: 10, flexWrap: 'wrap' }}>
            <button className="btn sm" onClick={copiarNombres}>Copiar nombres</button>
            <button className="btn ghost sm" onClick={descargarNombres}>Descargar nombres (.txt)</button>
            <button className="btn ghost sm" onClick={descargarCsv}>Descargar CSV completo</button>
          </div>
          <div className="lookup-list">
            {items.map((i, idx) => (
              <div className={'lk-row' + (i.encontrado ? '' : ' missing')} key={idx}>
                <div>
                  <div className="lk-name">
                    {i.encontrado ? i.nombre : 'No encontrado'} <span className="code">{i.codigo}</span>
                  </div>
                  {i.encontrado && (
                    <div className="muted sm">{i.denominacion} · {i.municipio} ({i.provincia}) · {i.titularidad}</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  )
}

export default function BuscarListado({ etapaLabels }) {
  return (
    <div className="buscar-tab">
      <Buscador etapaLabels={etapaLabels} />
      <Resolver />
    </div>
  )
}
