<script setup>
import { ref, computed, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import TripPlannerForm from '../components/TripPlannerForm.vue'
import TripForecastBar from '../components/TripForecastBar.vue'
import TripExposureScore from '../components/TripExposureScore.vue'
import TripLegBreakdown from '../components/TripLegBreakdown.vue'
import TripAlternatives from '../components/TripAlternatives.vue'
import TripMethodology from '../components/TripMethodology.vue'

const API_BASE = 'https://qcbqul6ys2.execute-api.ap-southeast-2.amazonaws.com'
const HOURLY_API = 'https://qcbqul6ys2.execute-api.ap-southeast-2.amazonaws.com'

function minutesToLabel(mins) {
  const h = Math.floor(mins / 60)
  const m = mins % 60
  const period = h >= 12 ? 'pm' : 'am'
  const displayH = h > 12 ? h - 12 : h === 0 ? 12 : h
  return m === 0
    ? `${displayH}:00 ${period}`
    : `${displayH}:${String(m).padStart(2, '0')} ${period}`
}

const TRANSPORT_NAMES = {
  walk: 'walking',
  tram: 'taking the tram',
  bus: 'taking the bus',
  drive: 'driving',
}
const TRANSPORT_LABELS = { walk: '🚶 Walk', tram: '🚃 Tram', bus: '🚌 Bus', drive: '🚗 Drive' }
const TRANSPORT_ICONS = { walk: '🚶', tram: '🚃', bus: '🚌', drive: '🚗' }

const allSuburbs = ref([])
const loading = ref(true)
const error = ref(null)
const showResults = ref(false)

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/suburbs`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    allSuburbs.value = (await res.json()).sort((a, b) => a.suburb_name.localeCompare(b.suburb_name))
  } catch (e) {
    error.value = 'Could not load suburb data. Please try again.'
    console.error(e)
  } finally {
    loading.value = false
  }
})

const selectedSuburbId = ref('')
const transportMode = ref('walk')
const durationMins = ref(30)
const departureMinutes = ref(540)

const selectedSuburb = computed(
  () => allSuburbs.value.find((s) => s.suburb_id === selectedSuburbId.value) ?? null,
)
const departureLabel = computed(() => minutesToLabel(departureMinutes.value))

const hourlyTemps = ref(null)

async function fetchHourly(suburbId) {
  try {
    const res = await fetch(`${HOURLY_API}/hourly/${suburbId}`)
    if (!res.ok) return
    const data = await res.json()
    hourlyTemps.value = data.hourly_apparent_temperature
  } catch (e) {
    console.warn('Hourly forecast unavailable, falling back to current data', e)
    hourlyTemps.value = null
  }
}

function getTempAtMinutes(mins) {
  const hour = Math.floor(mins / 60)
  if (hourlyTemps.value?.[hour] != null) return Math.round(hourlyTemps.value[hour] * 10) / 10
  return (
    Math.round(
      (selectedSuburb.value?.apparent_temperature ?? selectedSuburb.value?.temperature ?? 22) * 10,
    ) / 10
  )
}

const forecastTemp = computed(() => {
  if (!selectedSuburb.value) return null
  return getTempAtMinutes(departureMinutes.value)
})

function legScore(temp, shadeScore) {
  let base
  if (temp >= 35) base = Math.min(Math.round((temp - 35) * 3 + 70), 100)
  else if (temp >= 28) base = Math.round((temp - 28) * 4.3 + 40)
  else base = Math.max(Math.round(temp * 1.4), 0)
  return Math.min(base + Math.round(shadeScore * 0.2), 100)
}

function riskBand(score) {
  if (score >= 75) return { label: 'Very High', color: '#e8735a', bg: '#fdecea' } // coral
  if (score >= 50) return { label: 'High', color: '#e07b39', bg: '#fef3ec' } // orange
  if (score >= 25) return { label: 'Moderate', color: '#8b8000', bg: '#fefbe6' } // olive
  return { label: 'Low', color: '#4a7c59', bg: '#eef6f1' } // green
}

function weightedScore(legs) {
  const totalMins = legs.reduce((s, l) => s + l.minutes, 0)
  return Math.round(legs.reduce((s, l) => s + l.score * l.minutes, 0) / totalMins)
}

const LEG_COLORS = ['#e07b39', '#c8a800', '#d9534f', '#5b8dd9']

function buildLegs(mode, totalMins, temp, shade) {
  const transit = Math.max(totalMins - 10, 5)
  const defs = {
    walk: [{ label: 'Walking', minutes: totalMins, tempMod: 0, shadeMod: 0 }],
    tram: [
      { label: 'Walk to stop', minutes: 5, tempMod: 0, shadeMod: 0 },
      { label: 'Wait at stop', minutes: 5, tempMod: 0, shadeMod: -15 },
      { label: 'On tram', minutes: transit - 5, tempMod: -5, shadeMod: -30 },
      { label: 'Walk from stop', minutes: 5, tempMod: 0, shadeMod: 0 },
    ],
    bus: [
      { label: 'Walk to stop', minutes: 5, tempMod: 0, shadeMod: 0 },
      { label: 'Wait at stop', minutes: 5, tempMod: 0, shadeMod: -15 },
      { label: 'On bus', minutes: transit - 5, tempMod: -5, shadeMod: -30 },
      { label: 'Walk from stop', minutes: 5, tempMod: 0, shadeMod: 0 },
    ],
    drive: [
      { label: 'Walk to car', minutes: 3, tempMod: 0, shadeMod: 0 },
      { label: 'Driving', minutes: totalMins - 6, tempMod: -8, shadeMod: -40 },
      { label: 'Walk to dest.', minutes: 3, tempMod: 0, shadeMod: 0 },
    ],
  }
  return (defs[mode] ?? defs.walk).map((leg, i) => {
    const score = legScore(Math.max(temp + leg.tempMod, 10), Math.max(shade + leg.shadeMod, 0))
    return {
      label: leg.label,
      minutes: Math.max(leg.minutes, 1),
      score,
      color: LEG_COLORS[i % LEG_COLORS.length],
      riskLabel: riskBand(score).label,
    }
  })
}

const tripLegs = computed(() => {
  if (!selectedSuburb.value || forecastTemp.value === null) return null
  return buildLegs(
    transportMode.value,
    durationMins.value,
    forecastTemp.value,
    selectedSuburb.value.shade_score ?? 50,
  )
})

const overallScore = computed(() => (tripLegs.value ? weightedScore(tripLegs.value) : null))
const overallBand = computed(() =>
  overallScore.value !== null ? riskBand(overallScore.value) : null,
)

function pctDiff(base, alt) {
  return Math.round(((alt - base) / base) * 100)
}

function buildAlt(mode, duration, departMins, title, explanation, action) {
  if (!selectedSuburb.value) return null
  const temp = getTempAtMinutes(departMins)
  const shade = selectedSuburb.value.shade_score ?? 50
  const legs = buildLegs(mode, duration, temp, shade)
  const score = weightedScore(legs)
  const band = riskBand(score)
  const pct = pctDiff(overallScore.value, score)
  return {
    title,
    explanation,
    action,
    score,
    legs,
    pctChange: pct,
    ...band,
    params: { mode, duration, departMins },
  }
}

const alternatives = computed(() => {
  if (!overallScore.value || !selectedSuburb.value) return []
  const base = overallScore.value
  const curMode = transportMode.value
  const curDur = durationMins.value
  const curDepart = departureMinutes.value
  const suburb = selectedSuburb.value.suburb_name
  const alts = []

  const earlierDepart = Math.max(curDepart - 120, 540)
  if (earlierDepart !== curDepart) {
    const timeStr = minutesToLabel(earlierDepart)
    const altTemp = getTempAtMinutes(earlierDepart)
    const alt = buildAlt(
      curMode,
      curDur,
      earlierDepart,
      `Leave at ${timeStr}`,
      `At ${timeStr}, ${suburb} feels like ${altTemp}°C — cooler than your current departure time. Leaving earlier can make your trip much more comfortable.`,
      `Leave at ${timeStr}`,
    )
    if (alt) alts.push(alt)
  }

  if (curDepart < 1020) {
    const altTemp = getTempAtMinutes(1020)
    const alt = buildAlt(
      curMode,
      curDur,
      1020,
      'Leave after 5:00 pm',
      `By 5:00 pm, ${suburb} feels like ${altTemp}°C. The sun is lower and UV levels drop — making ${TRANSPORT_NAMES[curMode]} noticeably safer.`,
      'Leave at 5:00 pm',
    )
    if (alt) alts.push(alt)
  }

  const modePriority = ['drive', 'tram', 'bus', 'walk'].filter((m) => m !== curMode)
  for (const mode of modePriority) {
    const alt = buildAlt(
      mode,
      curDur,
      curDepart,
      `Switch to ${TRANSPORT_LABELS[mode]}`,
      `${TRANSPORT_LABELS[mode].split(' ')[1]} means less time walking in ${forecastTemp.value}°C heat. You'll spend more of your trip in a cooler, sheltered space.`,
      `Switch to ${TRANSPORT_LABELS[mode]}`,
    )
    if (alt && alt.score < base) {
      alts.push(alt)
      break
    }
  }

  if (curDur > 15) {
    const shorter = curDur === 60 ? 30 : 15
    const saved = curDur - shorter
    const alt = buildAlt(
      curMode,
      shorter,
      curDepart,
      `Shorten trip to ${shorter} min`,
      `Cutting ${saved} minutes off your trip means ${saved} fewer minutes in the heat. Even a small reduction in time outdoors helps your body cope better.`,
      `Plan a ${shorter}-minute trip`,
    )
    if (alt) alts.push(alt)
  }

  return alts
    .filter(Boolean)
    .sort((a, b) => a.score - b.score)
    .slice(0, 3)
})

async function handleSubmit() {
  if (!selectedSuburb.value) return
  await fetchHourly(selectedSuburb.value.suburb_id)
  showResults.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleReset() {
  showResults.value = false
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleSelectAlt(params) {
  transportMode.value = params.mode
  durationMins.value = params.duration
  departureMinutes.value = params.departMins
  showResults.value = false
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <div class="page">
    <NavBar />

    <main class="content">
      <!-- Page header — same structure as HeatMapPage -->
      <div class="page-header">
        <h1 class="page-title">🧭 Trip Coach</h1>
        <p class="page-desc">Plan your trip and see how safe it is in the heat</p>
      </div>

      <div v-if="loading" class="status-msg">Loading suburb data…</div>
      <div v-else-if="error" class="status-msg error">{{ error }}</div>

      <template v-else>
        <!-- Page 1 — centred form -->
        <div v-if="!showResults" class="plan-wrap">
          <TripPlannerForm
            :suburbs="allSuburbs"
            v-model:selectedSuburbId="selectedSuburbId"
            v-model:transportMode="transportMode"
            v-model:durationMins="durationMins"
            v-model:departureMinutes="departureMinutes"
            :loading="loading"
            @submit="handleSubmit"
          />
        </div>

        <!-- Page 2 — two columns -->
        <div v-else class="results-wrap">
          <!-- Left: trip summary + methodology (sticky) -->
          <div class="col-left">
            <div class="summary-card">
              <p class="summary-heading">Your trip</p>
              <div class="summary-row">
                <span class="summary-label">Going to</span>
                <span class="summary-value">{{ selectedSuburb.suburb_name }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">How</span>
                <span class="summary-value">
                  {{ TRANSPORT_ICONS[transportMode] }}
                  {{ transportMode.charAt(0).toUpperCase() + transportMode.slice(1) }}
                </span>
              </div>
              <div class="summary-row">
                <span class="summary-label">How long</span>
                <span class="summary-value">{{ durationMins }} min</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">Leaving at</span>
                <span class="summary-value">{{ departureLabel }}</span>
              </div>
              <button class="reset-btn" @click="handleReset">← Start a new trip</button>
            </div>

            <TripMethodology />
          </div>

          <!-- Right: results -->
          <div class="col-right">
            <TripForecastBar
              :suburbName="selectedSuburb.suburb_name"
              :forecastTemp="forecastTemp"
              :treeCanopy="selectedSuburb.tree_canopy_percent"
              :departureLabel="departureLabel"
              :transportMode="transportMode"
              :durationMins="durationMins"
            />
            <TripExposureScore
              :score="overallScore"
              :riskLabel="overallBand.label"
              :riskColor="overallBand.color"
              :riskBg="overallBand.bg"
            />
            <TripLegBreakdown :legs="tripLegs" />
            <TripAlternatives
              v-if="alternatives.length"
              :alternatives="alternatives"
              :baseScore="overallScore"
              @select-alt="handleSelectAlt"
            />
          </div>
        </div>
      </template>
    </main>

    <Footer />
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* Same as HeatMapPage: content constrains width, header uses negative margin */
.content {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.page-header {
  background: linear-gradient(135deg, #0d3a8f 0%, #1a56c4 100%);
  margin: 0 -1.5rem;
  padding: 2.25rem 1.5rem;
}
.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.4rem;
}
.page-desc {
  font-size: 1.05rem;
  color: rgba(255, 255, 255, 0.88);
  line-height: 1.65;
  max-width: 620px;
}

/* Page 1 — centred form */
.plan-wrap {
  max-width: 600px;
  margin: 0.5rem auto 0;
  width: 100%;
}

/* Page 2 — two columns */
.results-wrap {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 1.5rem;
  align-items: start;
}

/* Left: sticky */
.col-left {
  position: sticky;
  top: 88px;
  max-height: calc(100vh - 108px);
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #ddd transparent;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-bottom: 1rem;
}

/* Trip summary card */
.summary-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.summary-heading {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #888;
  margin: 0 0 0.2rem;
}
.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.92rem;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 0.5rem;
}
.summary-row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}
.summary-label {
  color: #888;
}
.summary-value {
  font-weight: 600;
  color: #1a1a1a;
}

/* Right: results */
.col-right {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.reset-btn {
  background: none;
  border: 2px solid #bbb;
  color: #555;
  border-radius: 8px;
  padding: 0.65rem 1.1rem;
  font-size: 0.92rem;
  font-weight: 600;
  cursor: pointer;
  transition:
    border-color 0.2s,
    color 0.2s;
  width: 100%;
  margin-top: 0.5rem;
}
.reset-btn:hover {
  border-color: var(--color-primary, #1a6eb5);
  color: var(--color-primary, #1a6eb5);
}

.status-msg {
  text-align: center;
  padding: 3rem 0;
  color: var(--color-text-muted);
  font-size: 1rem;
}
.status-msg.error {
  color: #991b1b;
}

@media (max-width: 860px) {
  .results-wrap {
    grid-template-columns: 1fr;
  }
  .col-left {
    position: static;
    max-height: none;
    overflow-y: visible;
  }
}
</style>
