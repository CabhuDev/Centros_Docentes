const ETAPA_LABELS = {} // se rellena desde meta en App via prop

export default function CenterCard({ c, drive, loading, mode, etapaLabels, isFav, onToggleFav, origin }) {
  const travel = mode?.travel || 'driving'
  const directionsUrl = origin
    ? `https://www.google.com/maps/dir/?api=1&origin=${origin.lat},${origin.lng}&destination=${c.lat},${c.lng}&travelmode=${travel}`
    : `https://www.google.com/maps/search/?api=1&query=${c.lat},${c.lng}`

  return (
    <div className={'card' + (isFav ? ' fav' : '')}>
      <div className="card-top">
        <div>
          <h3>{c.nombre || c.denominacion}</h3>
          <div className="denom">{c.denominacion}</div>
          <div className="place">{c.domicilio ? c.domicilio + ' · ' : ''}{c.municipio} ({c.provincia})</div>
        </div>
        <button className={'star' + (isFav ? ' on' : '')} title={isFav ? 'Quitar de preferencias' : 'Añadir a preferencias'} onClick={() => onToggleFav(c)}>
          {isFav ? '★' : '☆'}
        </button>
      </div>

      <div className="metrics">
        <div className="metric">
          <span className="v car">
            {drive?.duration_text || (loading ? <span className="pending">calculando…</span> : '—')}
          </span>
          <span className="k">{mode?.short || 'tiempo'}</span>
        </div>
        <div className="metric">
          <span className="v car">{drive?.distance_text || (loading ? '…' : '—')}</span>
          <span className="k">por ruta</span>
        </div>
        <div className="metric">
          <span className="v">{c.distancia_recta_km != null ? c.distancia_recta_km + ' km' : '—'}</span>
          <span className="k">línea recta</span>
        </div>
      </div>

      <div className="badges">
        <span className={'badge tit' + (c.concertado ? ' concert' : '')}>
          {c.titularidad}{c.concertado ? ' · concertado' : ''}
        </span>
        {c.etapas.map((e) => <span className="badge" key={e}>{etapaLabels[e] || e}</span>)}
      </div>

      {c.info_extra && (
        <div className="notas">
          <div className="notas-aviso">
            <span className="dot" aria-hidden="true"></span>
            Notas de la comunidad · opiniones no verificadas
          </div>
          <p className="notas-texto">{c.info_extra}</p>
        </div>
      )}

      <div className="card-actions">
        <a className="link" href={directionsUrl} target="_blank" rel="noreferrer">{mode?.icon || '🚗'} Cómo llegar</a>
        {c.telefono && <a className="link" href={`tel:${c.telefono}`}>📞 {c.telefono}</a>}
        {c.email && <a className="link" href={`mailto:${c.email}`}>✉️ Email</a>}
      </div>
    </div>
  )
}
