<script setup>
import { onMounted, onUnmounted, watch, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  suburbs: {
    type: Array,
    default: () => [],
  },
  selectedSuburb: {
    type: Object,
    default: null,
  },
  userLocation: {
    type: Object, // { lat, lng }
    default: null,
  },
})

const emit = defineEmits(['select'])

const mapContainer = ref(null)
let map = null
let geoJsonLayer = null
let locationMarker = null

const DEFAULT_CENTER = [-37.8136, 144.9631]
const DEFAULT_ZOOM = 12
const SELECTED_ZOOM = 14
let fitZoom = DEFAULT_ZOOM
let fitCenter = DEFAULT_CENTER

const riskColors = {
  high: { fill: '#EF4444', border: '#B91C1C' },
  moderate: { fill: '#F97316', border: '#C2410C' },
  low: { fill: '#22C55E', border: '#15803D' },
  default: { fill: '#94A3B8', border: '#64748B' },
}

function getStyle(feature) {
  const name = feature.properties.name
  const suburb = props.suburbs.find(
    (s) => s.suburb_name.toLowerCase().trim() === name.toLowerCase().trim(),
  )
  const level = suburb?.risk_level ?? 'default'
  const color = riskColors[level] ?? riskColors.default
  const isSelected =
    props.selectedSuburb?.suburb_name?.toLowerCase().trim() === name.toLowerCase().trim()

  return {
    fillColor: color.fill,
    fillOpacity: isSelected ? 0.85 : 0.45,
    color: color.border,
    weight: isSelected ? 2.5 : 1,
    opacity: 1,
  }
}

function onEachFeature(feature, layer) {
  layer.on({
    click: () => {
      const name = feature.properties.name
      const suburb = props.suburbs.find(
        (s) => s.suburb_name.toLowerCase().trim() === name.toLowerCase().trim(),
      )
      if (suburb) emit('select', suburb)
    },
    mouseover: (e) => {
      e.target.setStyle({ fillOpacity: 0.75, weight: 2 })
    },
    mouseout: (e) => {
      geoJsonLayer.resetStyle(e.target)
    },
  })

  const name = feature.properties.name
  const suburb = props.suburbs.find(
    (s) => s.suburb_name.toLowerCase().trim() === name.toLowerCase().trim(),
  )
  if (suburb) {
    layer.bindTooltip(
      `<strong>${suburb.suburb_name}</strong><br>⚠️ ${suburb.risk_level.charAt(0).toUpperCase() + suburb.risk_level.slice(1)} Risk<br>🌡️ Feels like ${Math.round(suburb.apparent_temperature ?? suburb.temperature)}°C`,
      { sticky: true, className: 'suburb-tooltip' },
    )
  }
}

async function initMap() {
  map = L.map(mapContainer.value, {
    center: DEFAULT_CENTER,
    zoom: DEFAULT_ZOOM,
    minZoom: 11, // prevent zooming out beyond Greater Melbourne
    maxZoom: 18,
    zoomControl: true,
    scrollWheelZoom: true,
    maxBounds: [
      [-39.5, 140.5], // south-west corner of Victoria
      [-33.5, 150.5], // north-east corner of Victoria
    ],
    maxBoundsViscosity: 1.0, // hard boundary, user cannot drag outside
  })

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap © CARTO',
    maxZoom: 18,
    minZoom: 11,
  }).addTo(map)

  try {
    const res = await fetch('/geojson/melbourne-suburbs.geojson')
    const geojson = await res.json()

    geoJsonLayer = L.geoJSON(geojson, {
      style: getStyle,
      onEachFeature,
    }).addTo(map)

    map.fitBounds(geoJsonLayer.getBounds(), { padding: [20, 20] })
    // Store the resulting zoom/center so deselect can fly back to exactly this view
    map.once('moveend', () => {
      fitZoom = map.getZoom()
      fitCenter = [map.getCenter().lat, map.getCenter().lng]
    })

    // 地图初始化完成后，如果 userLocation 已经有值（定位比地图快），补渲染 marker
    if (props.userLocation) {
      updateLocationMarker(props.userLocation)
    }
  } catch (e) {
    console.error('Failed to load GeoJSON:', e)
  }
}

function refreshStyles() {
  if (geoJsonLayer) {
    geoJsonLayer.setStyle(getStyle)
  }
}

// Fly to selected suburb centroid, or back to default when deselected
function flyToSuburb(suburb) {
  if (!map || !geoJsonLayer) return

  if (!suburb) {
    map.flyTo(fitCenter, fitZoom, { duration: 0.6 })
    return
  }

  // Find the matching GeoJSON layer and fly to its centre
  geoJsonLayer.eachLayer((layer) => {
    const name = layer.feature?.properties?.name
    if (name?.toLowerCase().trim() === suburb.suburb_name.toLowerCase().trim()) {
      const center = layer.getBounds().getCenter()
      map.flyTo(center, SELECTED_ZOOM, { duration: 0.8 })
    }
  })
}

function updateLocationMarker(location) {
  if (!map) return
  if (locationMarker) {
    locationMarker.remove()
    locationMarker = null
  }
  if (!location) return

  // 蓝色脉冲圆点
  const icon = L.divIcon({
    className: '',
    html: `<div class="user-location-marker"><div class="user-location-dot"></div><div class="user-location-pulse"></div></div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10],
  })

  locationMarker = L.marker([location.lat, location.lng], { icon, zIndexOffset: 1000 })
    .addTo(map)
    .bindTooltip('Your location', { permanent: false, className: 'suburb-tooltip' })
}

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
})

watch(() => props.suburbs, refreshStyles, { deep: true })
watch(
  () => props.selectedSuburb,
  (suburb) => {
    refreshStyles()
    flyToSuburb(suburb)
  },
)
watch(
  () => props.userLocation,
  (location) => {
    updateLocationMarker(location)
  },
)
</script>

<template>
  <div class="map-wrap">
    <div ref="mapContainer" class="map-container"></div>
  </div>
</template>

<style scoped>
.map-wrap {
  width: 100%;
  height: 100%;
  border-radius: var(--radius-card);
  overflow: hidden;
}

.map-container {
  width: 100%;
  height: 100%;
  min-height: 480px;
}
</style>

<style>
.suburb-tooltip {
  font-family: sans-serif;
  font-size: 0.85rem;
  padding: 6px 10px;
  border-radius: 8px;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.user-location-marker {
  position: relative;
  width: 20px;
  height: 20px;
}

.user-location-dot {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 12px;
  height: 12px;
  background: #2563eb;
  border: 2.5px solid #ffffff;
  border-radius: 50%;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
  z-index: 2;
}

.user-location-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 28px;
  height: 28px;
  background: rgba(37, 99, 235, 0.2);
  border-radius: 50%;
  animation: location-pulse 1.8s ease-out infinite;
  z-index: 1;
}

@keyframes location-pulse {
  0% {
    transform: translate(-50%, -50%) scale(0.5);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.8);
    opacity: 0;
  }
}
</style>
