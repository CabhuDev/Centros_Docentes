import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents } from 'react-leaflet'
import L from 'leaflet'
import { useEffect } from 'react'

const centerIcon = L.divIcon({ className: '', html: '<div class="marker-pin"></div>', iconSize: [16, 16], iconAnchor: [8, 16] })
const originIcon = L.divIcon({ className: '', html: '<div class="marker-pin origin"></div>', iconSize: [20, 20], iconAnchor: [10, 20] })

function Recenter({ origin, items }) {
  const map = useMap()
  useEffect(() => {
    const pts = []
    if (origin) pts.push([origin.lat, origin.lng])
    items.slice(0, 25).forEach((c) => pts.push([c.lat, c.lng]))
    if (pts.length === 1) map.setView(pts[0], 13)
    else if (pts.length > 1) map.fitBounds(pts, { padding: [40, 40], maxZoom: 14 })
  }, [origin, items, map])
  return null
}

function ClickToSetOrigin({ onPick }) {
  useMapEvents({ click(e) { onPick(e.latlng.lat, e.latlng.lng) } })
  return null
}

export default function MapView({ origin, items, onPickOrigin, onSelect }) {
  return (
    <MapContainer center={[37.5, -4.7]} zoom={7} scrollWheelZoom>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <ClickToSetOrigin onPick={onPickOrigin} />
      <Recenter origin={origin} items={items} />
      {origin && (
        <Marker position={[origin.lat, origin.lng]} icon={originIcon}>
          <Popup>Tu punto de partida</Popup>
        </Marker>
      )}
      {items.slice(0, 60).map((c) => (
        <Marker
          key={c.codigo}
          position={[c.lat, c.lng]}
          icon={centerIcon}
          eventHandlers={{ click: () => onSelect && onSelect(c.codigo) }}
        >
          <Popup>
            <b>{c.nombre}</b>
            <br />{c.denominacion}
            <br />{c.municipio} · {c.titularidad}
            {c.distancia_recta_km != null && <><br />{c.distancia_recta_km} km en línea recta</>}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}
