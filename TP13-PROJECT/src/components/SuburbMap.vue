<script setup>
import { onMounted, onUnmounted, watch, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  suburbs: {
    type: Array,
    default: () => [],
    // [{ suburb_name, risk_level, ... }]
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
      `<strong>${suburb.suburb_name}</strong><br>${suburb.temperature}°C · ${suburb.risk_level} heat`,
      { sticky: true, className: 'suburb-tooltip' },
    )
  }
}

async function initMap() {
  map = L.map(mapContainer.value, {
    center: [-37.8136, 144.9631],
    zoom: 11,
    zoomControl: true,
    scrollWheelZoom: true,
  })

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap © CARTO',
    maxZoom: 18,
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
watch(() => props.selectedSuburb, refreshStyles)
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
