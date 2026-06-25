import { useState } from 'react'

export default function Filters({ meta, filters, setFilters }) {
  const [expanded, setExpanded] = useState({})
  if (!meta) return null
  const set = (patch) => setFilters({ ...filters, ...patch })

  const municipios = filters.provincia
    ? (meta.municipios_por_provincia[filters.provincia] || [])
    : []

  function toggle(listKey, value) {
    const cur = new Set(filters[listKey])
    cur.has(value) ? cur.delete(value) : cur.add(value)
    set({ [listKey]: [...cur] })
  }

  const seleccionadas = filters.etapas.length + filters.ensenanzas.length

  return (
    <div>
      <div className="field">
        <label>Búsqueda libre</label>
        <input
          className="input"
          placeholder="Nombre de centro, código…"
          value={filters.q}
          onChange={(e) => set({ q: e.target.value })}
        />
      </div>

      <div className="field">
        <label>Provincia</label>
        <select
          value={filters.provincia}
          onChange={(e) => set({ provincia: e.target.value, municipio: [] })}
        >
          <option value="">Todas</option>
          {meta.provincias.map((p) => <option key={p} value={p}>{p}</option>)}
        </select>
      </div>

      {filters.provincia && (
        <div className="field">
          <label>Municipio</label>
          <select
            value={filters.municipio[0] || ''}
            onChange={(e) => set({ municipio: e.target.value ? [e.target.value] : [] })}
          >
            <option value="">Todos</option>
            {municipios.map((m) => <option key={m} value={m}>{m}</option>)}
          </select>
        </div>
      )}

      <div className="field">
        <label>Titularidad</label>
        <div className="seg">
          {['', 'Público', 'Privado'].map((t) => (
            <button
              key={t || 'all'}
              className={filters.titularidad === t ? 'on' : ''}
              onClick={() => set({ titularidad: t, concertado: t === 'Privado' ? filters.concertado : null })}
            >
              {t || 'Todas'}
            </button>
          ))}
        </div>
        {filters.titularidad === 'Privado' && (
          <label className="check">
            <input
              type="checkbox"
              checked={filters.concertado === true}
              onChange={(e) => set({ concertado: e.target.checked ? true : null })}
            />
            Solo concertados
          </label>
        )}
      </div>

      <div className="field">
        <label>Etapas y enseñanzas que imparte</label>
        <div className="tree">
          {meta.etapas.map((et) => {
            const onEt = filters.etapas.includes(et.key)
            const hasSub = et.ensenanzas.length > 1
            const open = expanded[et.key]
            const subSel = et.ensenanzas.filter((s) => filters.ensenanzas.includes(s.key)).length
            return (
              <div className="tree-node" key={et.key}>
                <div className="tree-row">
                  <button
                    className={'chip' + (onEt ? ' on' : '')}
                    onClick={() => toggle('etapas', et.key)}
                  >
                    {et.label}
                  </button>
                  {hasSub && (
                    <button
                      className={'expand' + (subSel ? ' has' : '')}
                      title="Ver enseñanzas concretas"
                      onClick={() => setExpanded({ ...expanded, [et.key]: !open })}
                    >
                      {subSel ? `${subSel} ▾` : '▾'}
                    </button>
                  )}
                </div>
                {hasSub && open && (
                  <div className="chips sub">
                    {et.ensenanzas.map((s) => (
                      <button
                        key={s.key}
                        className={'chip xs' + (filters.ensenanzas.includes(s.key) ? ' on' : '')}
                        onClick={() => toggle('ensenanzas', s.key)}
                      >
                        {s.label}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {seleccionadas > 1 && (
          <div className="seg" style={{ marginTop: 10 }}>
            <button className={filters.match === 'any' ? 'on' : ''} onClick={() => set({ match: 'any' })}>
              Cualquiera
            </button>
            <button className={filters.match === 'all' ? 'on' : ''} onClick={() => set({ match: 'all' })}>
              Todas
            </button>
          </div>
        )}
        {seleccionadas > 0 && (
          <button className="btn ghost sm" style={{ marginTop: 10 }} onClick={() => set({ etapas: [], ensenanzas: [] })}>
            Limpiar enseñanzas
          </button>
        )}
      </div>
    </div>
  )
}
