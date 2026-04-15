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
})

const emit = defineEmits(['select'])

const mapContainer = ref(null)
let map = null
let geoJsonLayer = null

const DEFAULT_CENTER = [-37.8136, 144.9631]
const DEFAULT_ZOOM = 12
const SELECTED_ZOOM = 14

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
      `<strong>${suburb.suburb_name}</strong><br>🌡️ ${suburb.temperature}°C<br>⚠️ ${suburb.risk_level.charAt(0).toUpperCase() + suburb.risk_level.slice(1)} Risk`,
      { sticky: true, className: 'suburb-tooltip' },
    )
  }
}

async function initMap() {
  map = L.map(mapContainer.value, {
    center: DEFAULT_CENTER,
    zoom: DEFAULT_ZOOM,
    minZoom: 11,                 // prevent zooming out beyond Greater Melbourne
    maxZoom: 18,
    zoomControl: true,
    scrollWheelZoom: true,
    maxBounds: [
      [-39.5, 140.5],            // south-west corner of Victoria
      [-33.5, 150.5],            // north-east corner of Victoria
    ],
    maxBoundsViscosity: 1.0,     // hard boundary, user cannot drag outside
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
    map.flyTo(DEFAULT_CENTER, DEFAULT_ZOOM, { duration: 0.6 })
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
watch(() => props.selectedSuburb, (suburb) => {
  refreshStyles()
  flyToSuburb(suburb)
})
</script>

<template>
  <div class="map-wrap">
    <div ref="mapContainer" class="map-container"></div>
  </div>
</template>

<style scoped>
.map-wrap {
  width: 100%;
  border-radius: var(--radius-card);
  overflow: hidden;
  border: 1.5px solid var(--color-border);
  box-shadow: var(--shadow-card);
}

.map-container {
  width: 100%;
  height: 480px;
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
</style>