import { useEffect, useMemo, useRef, useState } from 'react'
import { getMeta, getCentros, getDistancias } from './api'
import StartPoint from './components/StartPoint'
import Filters from './components/Filters'
import CenterCard from './components/CenterCard'
import Preferences from './components/Preferences'
import MapView from './components/MapView'
import BuscarListado from './components/BuscarListado'

const DEFAULT_FILTERS = {
  q: '', provincia: '', municipio: [], titularidad: '', concertado: null,
  etapas: [], ensenanzas: [], match: 'any',
}
const LIMIT = 300        // máximo de centros que pide al backend
const SHOW = 300         // tarjetas visibles (toda la lista devuelta)
const DRIVE_TOP = 300    // centros para los que pedimos distancia/tiempo (todos)

// Modos de transporte de Google Distance Matrix.
const MODES = {
  driving:   { label: 'En coche',       short: 'en coche',       icon: '🚗', travel: 'driving' },
  transit:   { label: 'Transporte púb.', short: 'en transporte',  icon: '🚌', travel: 'transit' },
  bicycling: { label: 'En bici',        short: 'en bici',        icon: '🚲', travel: 'bicycling' },
  walking:   { label: 'Andando',        short: 'andando',        icon: '🚶', travel: 'walking' },
}

export default function App() {
  const [meta, setMeta] = useState(null)
  const [filters, setFilters] = useState(DEFAULT_FILTERS)
  const [origin, setOrigin] = useState(null)
  const [data, setData] = useState({ total: 0, items: [] })
  const [drive, setDrive] = useState({})
  const [mode, setMode] = useState('driving')
  const [sortBy, setSortBy] = useState('tiempo')
  const [tab, setTab] = useState('cercania')
  const [loading, setLoading] = useState(false)
  const [driveLoading, setDriveLoading] = useState(false)
  const [error, setError] = useState('')
  const [favs, setFavs] = useState(() => {
    try { return JSON.parse(localStorage.getItem('favs') || '[]') } catch { return [] }
  })

  const etapaLabels = useMemo(() => {
    const m = {}; meta?.etapas.forEach((e) => { m[e.key] = e.label }); return m
  }, [meta])

  useEffect(() => { getMeta().then(setMeta).catch((e) => setError(e.message)) }, [])
  useEffect(() => { localStorage.setItem('favs', JSON.stringify(favs)) }, [favs])

  // --- cargar centros (debounce) cuando cambian filtros u origen ---
  const tRef = useRef()
  useEffect(() => {
    clearTimeout(tRef.current)
    tRef.current = setTimeout(async () => {
      setLoading(true); setError('')
      try {
        const params = {
          q: filters.q || undefined,
          provincia: filters.provincia || undefined,
          municipio: filters.municipio.length ? filters.municipio : undefined,
          titularidad: filters.titularidad || undefined,
          concertado: filters.concertado === true ? true : undefined,
          etapas: filters.etapas.length ? filters.etapas : undefined,
          etapas_match: filters.match,
          ensenanzas: filters.ensenanzas.length ? filters.ensenanzas : undefined,
          ensenanzas_match: filters.match,
          lat: origin?.lat, lng: origin?.lng,
          limit: LIMIT,
        }
        const r = await getCentros(params)
        setData(r)
      } catch (e) { setError(e.message) } finally { setLoading(false) }
    }, 300)
    return () => clearTimeout(tRef.current)
  }, [filters, origin])

  // --- distancia/tiempo del modo elegido para TODOS los centros devueltos ---
  // Una sola petición; el backend trocea en lotes de 25 y los lanza en paralelo.
  // La "generación" evita que una respuesta vieja (otro origen/modo/filtro)
  // pise a la nueva. El debounce evita ráfagas al teclear.
  const driveGen = useRef(0)
  useEffect(() => {
    if (!origin || data.items.length === 0) { setDrive({}); return }
    const gen = ++driveGen.current
    const codigos = data.items.slice(0, DRIVE_TOP).map((c) => c.codigo)

    const t = setTimeout(() => {
      setDrive({})
      setDriveLoading(true)
      getDistancias({ lat: origin.lat, lng: origin.lng }, codigos, mode)
        .then((res) => {
          if (gen !== driveGen.current) return   // respuesta obsoleta
          const map = {}
          res.results.forEach((d) => { if (d.status === 'OK') map[d.codigo] = d })
          setDrive(map)
        })
        .catch(() => {})
        .finally(() => { if (gen === driveGen.current) setDriveLoading(false) })
    }, 300)

    return () => clearTimeout(t)
  }, [origin, data, mode])

  // Códigos para los que SÍ pedimos ruta (para distinguir "calculando" de "—").
  const requestedSet = useMemo(
    () => new Set(data.items.slice(0, DRIVE_TOP).map((c) => c.codigo)),
    [data],
  )

  // --- orden de la lista visible ---
  const items = useMemo(() => {
    const arr = [...data.items]
    if (origin && sortBy === 'tiempo') {
      arr.sort((a, b) => (drive[a.codigo]?.duration_s ?? 1e12) - (drive[b.codigo]?.duration_s ?? 1e12))
    } else if (origin && sortBy === 'ruta_km') {
      arr.sort((a, b) => (drive[a.codigo]?.distance_m ?? 1e12) - (drive[b.codigo]?.distance_m ?? 1e12))
    } // 'recta' ya viene ordenado del backend
    return arr.slice(0, SHOW)
  }, [data, drive, sortBy, origin])

  const favSet = useMemo(() => new Set(favs.map((f) => f.codigo)), [favs])

  function toggleFav(c) {
    setFavs((prev) => prev.some((f) => f.codigo === c.codigo)
      ? prev.filter((f) => f.codigo !== c.codigo)
      : [...prev, {
          codigo: c.codigo,
          nombre: c.nombre || c.denominacion,
          municipio: c.municipio,
          provincia: c.provincia,
          distancia_recta_km: c.distancia_recta_km ?? null,
        }])
  }
  function moveFav(i, dir) {
    setFavs((prev) => {
      const a = [...prev]; const j = i + dir
      if (j < 0 || j >= a.length) return prev
      ;[a[i], a[j]] = [a[j], a[i]]; return a
    })
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="logo">CD</div>
        <div>
          <h1>Centros Docentes de Andalucía</h1>
          <div className="sub">Curso {meta?.curso || '—'} · {meta?.total_centros || '—'} centros</div>
        </div>
        <nav className="tabs">
          <button className={tab === 'cercania' ? 'on' : ''} onClick={() => setTab('cercania')}>Por cercanía</button>
          <button className={tab === 'buscar' ? 'on' : ''} onClick={() => setTab('buscar')}>Buscar / Listado</button>
        </nav>
      </header>

      {tab === 'buscar' && <BuscarListado etapaLabels={etapaLabels} />}

      {tab === 'cercania' && (
      <div className="layout">
        <aside className="sidebar">
          <StartPoint origin={origin} onSet={setOrigin} />
          <div className="divider" />
          <Filters meta={meta} filters={filters} setFilters={setFilters} />
          <div className="divider" />
          <div className="field" style={{ marginBottom: 4 }}>
            <label>⭐ Mis preferencias ({favs.length})</label>
            <Preferences
              favs={favs} drive={drive} mode={mode}
              move={moveFav}
              remove={(cod) => setFavs((p) => p.filter((f) => f.codigo !== cod))}
              clear={() => setFavs([])}
            />
          </div>
        </aside>

        <main className="main">
          <div className="map-wrap">
            <MapView
              origin={origin}
              items={data.items}
              onPickOrigin={(lat, lng) => setOrigin({ lat, lng, label: `Punto en el mapa (${lat.toFixed(4)}, ${lng.toFixed(4)})` })}
            />
          </div>

          <div className="results">
            <div className="results-head">
              <div className="count">
                {loading ? <span className="spinner" /> : <b>{data.total}</b>} centros
                {data.devueltos < data.total && <> · mostrando los {data.devueltos} más cercanos (afina los filtros)</>}
                {driveLoading && <> · <span className="spinner" /> calculando rutas…</>}
              </div>
              <div className="controls">
                <div className="mode-seg" title="Modo de transporte">
                  {Object.entries(MODES).map(([k, v]) => (
                    <button
                      key={k}
                      className={mode === k ? 'on' : ''}
                      onClick={() => setMode(k)}
                      title={v.label}
                    >
                      {v.icon}
                    </button>
                  ))}
                </div>
                <div className="sort">
                  <label>Ordenar</label>
                  <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} disabled={!origin}>
                    <option value="tiempo">Tiempo de viaje</option>
                    <option value="ruta_km">Distancia por ruta</option>
                    <option value="recta">Línea recta</option>
                  </select>
                </div>
              </div>
            </div>

            {error && <div className="error">{error}</div>}

            {!origin && (
              <div className="empty">
                Indica tu <b>punto de partida</b> arriba a la izquierda para ordenar los centros por cercanía en coche.
              </div>
            )}

            {items.map((c) => (
              <CenterCard
                key={c.codigo}
                c={c}
                drive={drive[c.codigo]}
                loading={driveLoading && requestedSet.has(c.codigo)}
                mode={MODES[mode]}
                etapaLabels={etapaLabels}
                isFav={favSet.has(c.codigo)}
                onToggleFav={toggleFav}
                origin={origin}
              />
            ))}

            {origin && !loading && items.length === 0 && (
              <div className="empty">No hay centros con esos filtros. Prueba a quitar alguno.</div>
            )}
          </div>
        </main>
      </div>
      )}
    </div>
  )
}
