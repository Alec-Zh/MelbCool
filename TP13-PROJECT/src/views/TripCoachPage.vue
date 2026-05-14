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
const TRANSPORT_LABELS = { walk: 'Walk', tram: 'Tram', bus: 'Bus', drive: 'Drive' }
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

// ── Exposure-based leg model ────────────────────────────────────────────────
// Outdoor exposure ratios based on:
//   Walk: 100% outdoor (full trip)
//   Tram/Bus: 25% outdoor — based on PTV average walk+wait share of total trip time
//     (Currie & Delbosc, 2011, "Modelling the social exclusion pedestrian catchment")
//   Drive: 10% outdoor — AustRoads parking walk estimate ~1–2 min each end
//
// Outdoor segment uses full apparent_temperature + shade_score heat model.
// Sheltered segment applies temperature reduction (vehicle air conditioning assumed).

const EXPOSURE = {
  walk: { outdoorRatio: 1.0, tempMod: 0, shadeMod: 0 },
  tram: { outdoorRatio: 0.25, tempMod: -5, shadeMod: -30 },
  bus: { outdoorRatio: 0.25, tempMod: -5, shadeMod: -30 },
  drive: { outdoorRatio: 0.1, tempMod: -8, shadeMod: -40 },
}

function legScore(temp, shadeScore) {
  let base
  if (temp >= 35) base = Math.min(Math.round((temp - 35) * 3 + 70), 100)
  else if (temp >= 28) base = Math.round((temp - 28) * 4.3 + 40)
  else base = Math.max(Math.round(temp * 1.4), 0)
  return Math.min(base + Math.round(shadeScore * 0.2), 100)
}

function riskBand(score) {
  if (score >= 75) return { label: 'Very High', color: '#e8735a', bg: '#fdecea' }
  if (score >= 50) return { label: 'High', color: '#e07b39', bg: '#fef3ec' }
  if (score >= 25) return { label: 'Moderate', color: '#8b8000', bg: '#fefbe6' }
  return { label: 'Low', color: '#4a7c59', bg: '#eef6f1' }
}

function weightedScore(legs) {
  const totalMins = legs.reduce((s, l) => s + l.minutes, 0)
  return Math.round(legs.reduce((s, l) => s + l.score * l.minutes, 0) / totalMins)
}

function buildLegs(mode, totalMins, temp, shade) {
  const exp = EXPOSURE[mode] ?? EXPOSURE.walk
  const outdoorMins = Math.max(Math.round(totalMins * exp.outdoorRatio), 1)
  const shelteredMins = totalMins - outdoorMins

  const outdoorScore = legScore(temp, shade)
  const legs = [
    {
      label: 'Time outdoors',
      minutes: outdoorMins,
      score: outdoorScore,
      color: '#e07b39',
      riskLabel: riskBand(outdoorScore).label,
      isOutdoor: true,
    },
  ]

  if (shelteredMins > 0) {
    const shelteredScore = legScore(
      Math.max(temp + exp.tempMod, 10),
      Math.max(shade + exp.shadeMod, 0),
    )
    legs.push({
      label: mode === 'drive' ? 'Time in car' : 'Time on vehicle',
      minutes: shelteredMins,
      score: shelteredScore,
      color: '#5b8dd9',
      riskLabel: riskBand(shelteredScore).label,
      isOutdoor: false,
    })
  }

  return legs
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

  // Earlier departure
  const earlierDepart = Math.max(curDepart - 120, 540)
  if (earlierDepart !== curDepart) {
    const timeStr = minutesToLabel(earlierDepart)
    const altTemp = getTempAtMinutes(earlierDepart)
    const alt = buildAlt(
      curMode,
      curDur,
      earlierDepart,
      `Leave at ${timeStr}`,
      `At ${timeStr}, ${suburb} feels like ${altTemp}°C — cooler than your current departure time. Leaving earlier can make your trip more comfortable.`,
      `Leave at ${timeStr}`,
    )
    if (alt) alts.push(alt)
  }

  // After 5pm
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

  // Different transport mode (drive first as it minimises outdoor exposure)
  const modePriority = ['drive', 'tram', 'bus', 'walk'].filter((m) => m !== curMode)
  for (const mode of modePriority) {
    const alt = buildAlt(
      mode,
      curDur,
      curDepart,
      `Switch to ${TRANSPORT_LABELS[mode]}`,
      `${TRANSPORT_LABELS[mode]} means less time outdoors in ${forecastTemp.value}°C heat. You'll spend more of your trip in a cooler, sheltered space.`,
      `Switch to ${TRANSPORT_LABELS[mode]}`,
    )
    if (alt && alt.score < base) {
      alts.push(alt)
      break
    }
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
      <!-- Page header -->
      <div class="page-header card">
        <div class="page-header-text">
          <h1 class="page-title">Trip <span class="page-title-accent">Coach</span></h1>
          <p class="page-desc">
            Tell us about your trip and we'll show you
            <strong>how much heat you'll be exposed to</strong> — so you can decide the safest time
            and way to travel.
          </p>
        </div>
      </div>

      <div v-if="loading" class="status-msg">Loading suburb data…</div>
      <div v-else-if="error" class="status-msg error">{{ error }}</div>

      <template v-else>
        <!-- Page 1 — two column: form left, guide right -->
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
          <div class="plan-right">
            <div class="guide-card card">
              <p class="guide-title">How it works</p>
              <ul class="guide-list">
                <li>
                  Choose your <strong>destination</strong> and
                  <strong>how you're travelling</strong>
                </li>
                <li>
                  Tell us <strong>how long</strong> the trip takes and <strong>when</strong> you're
                  leaving
                </li>
                <li>We'll show how much time you'll spend <strong>outdoors in the heat</strong></li>
                <li>We'll suggest <strong>safer options</strong> if your trip looks risky</li>
              </ul>
            </div>

            <div class="guide-card card">
              <p class="guide-title">Time spent outdoors by transport</p>
              <div class="transport-compare">
                <div class="tc-row">
                  <span class="tc-mode">🚶 Walk</span>
                  <div class="tc-bar-wrap">
                    <div class="tc-bar" style="width: 100%; background: #c0392b"></div>
                  </div>
                  <span class="tc-pct">100%</span>
                </div>
                <div class="tc-row">
                  <span class="tc-mode">🚃 Tram</span>
                  <div class="tc-bar-wrap">
                    <div class="tc-bar" style="width: 25%; background: #e8903a"></div>
                  </div>
                  <span class="tc-pct">~25%</span>
                </div>
                <div class="tc-row">
                  <span class="tc-mode">🚌 Bus</span>
                  <div class="tc-bar-wrap">
                    <div class="tc-bar" style="width: 25%; background: #e8903a"></div>
                  </div>
                  <span class="tc-pct">~25%</span>
                </div>
                <div class="tc-row">
                  <span class="tc-mode">🚗 Drive</span>
                  <div class="tc-bar-wrap">
                    <div class="tc-bar" style="width: 10%; background: #4d9e5a"></div>
                  </div>
                  <span class="tc-pct">~10%</span>
                </div>
              </div>
              <p class="tc-note">Less time outdoors = lower heat exposure</p>
              <div class="tc-refs">
                <p class="tc-refs-title">Sources</p>
                <ul>
                  <li>
                    Currie &amp; Delbosc (2011). Modelling the social exclusion pedestrian catchment
                    area of urban transit. <em>Journal of Transport Geography.</em>
                  </li>
                  <li>
                    AustRoads (2020). Pedestrian access to car parks: typical walk distance
                    estimates.
                  </li>
                  <li>Open-Meteo (2024). Apparent temperature API — hourly forecast data.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Page 2 — results -->
        <div v-else class="results-wrap">
          <!-- Left: trip summary + methodology (sticky) -->
          <div class="col-left">
            <div class="summary-card card">
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
              <button class="reset-btn" @click="handleReset">← Plan a different trip</button>
            </div>

            <!-- Results guide -->
            <div class="guide-card card">
              <p class="guide-title">Reading your results</p>
              <ul class="guide-list">
                <li>
                  The <strong>risk score</strong> shows how much heat stress this trip may cause
                </li>
                <li>
                  <strong>Time outdoors</strong> is the part that matters most — that's when your
                  body heats up
                </li>
                <li>
                  Check the <strong>safer options</strong> below if your score is High or Very High
                </li>
              </ul>
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
            <TripLegBreakdown :legs="tripLegs" :transportMode="transportMode" />
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
  background: linear-gradient(160deg, #eaf4f4 0%, #f0f7ee 50%, #e8f4f0 100%);
}

.content {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 1.25rem 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card {
  background: #ffffff;
  border-radius: 14px;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    0 8px 24px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

/* Header card */
.page-header {
  padding: 1.75rem 1.6rem;
  background: linear-gradient(135deg, rgba(13, 58, 143, 0.95), rgba(11, 127, 121, 0.88));
  border: none;
}
.page-title {
  font-size: 1.95rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 0.35rem;
  letter-spacing: -0.02em;
}
.page-title-accent {
  color: #a3f77d;
}
.page-desc {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin: 0;
  max-width: 580px;
}
.page-desc strong {
  color: #ffffff;
  font-weight: 600;
}

/* Guide card */
.guide-card {
  padding: 1rem 1.25rem;
}
.guide-title {
  font-size: 0.72rem;
  font-weight: 700;
  color: #2d7a3a;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0 0 0.6rem;
}
.guide-list {
  list-style: disc;
  padding-left: 1.1rem;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.guide-list li {
  font-size: 0.875rem;
  color: #5a6e6a;
  line-height: 1.5;
}
.guide-list li strong {
  color: #1c2e2a;
  font-weight: 600;
}

/* Page 1 — two column */
.plan-wrap {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1.25rem;
  align-items: stretch;
}

.plan-right {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.plan-right .guide-card:last-child {
  flex: 1;
}

/* Transport comparison */
.transport-compare {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-top: 0.25rem;
}
.tc-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.tc-mode {
  font-size: 0.82rem;
  font-weight: 600;
  color: #1c2e2a;
  width: 58px;
  flex-shrink: 0;
}
.tc-bar-wrap {
  flex: 1;
  height: 10px;
  background: #f0f5f4;
  border-radius: 5px;
  overflow: hidden;
}
.tc-bar {
  height: 100%;
  border-radius: 5px;
  transition: width 0.4s ease;
}
.tc-pct {
  font-size: 0.78rem;
  font-weight: 700;
  color: #5a6e6a;
  width: 34px;
  text-align: right;
  flex-shrink: 0;
}
.tc-note {
  font-size: 0.76rem;
  color: #5a6e6a;
  margin: 0.5rem 0 0;
  padding-top: 0.5rem;
  border-top: 1px solid #e8f0ee;
  font-style: italic;
}
.tc-refs {
  margin-top: 0.75rem;
  padding-top: 0.6rem;
  border-top: 1px solid #e8f0ee;
}
.tc-refs-title {
  font-size: 0.72rem;
  font-weight: 700;
  color: #2d7a3a;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin: 0 0 0.4rem;
}
.tc-refs ul {
  list-style: disc;
  padding-left: 1rem;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.tc-refs li {
  font-size: 0.72rem;
  color: #5a6e6a;
  line-height: 1.5;
}
.tc-refs em {
  font-style: italic;
}

/* Page 2 */
.results-wrap {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 1.5rem;
  align-items: start;
}

.col-left {
  position: sticky;
  top: 76px;
  max-height: calc(100vh - 96px);
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #ddd transparent;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-bottom: 1rem;
}

.summary-card {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.summary-heading {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b8f8c;
  margin: 0 0 0.1rem;
}
.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  border-bottom: 1px solid #f0f5f4;
  padding-bottom: 0.5rem;
}
.summary-row:last-of-type {
  border-bottom: none;
  padding-bottom: 0;
}
.summary-label {
  color: #7a9490;
}
.summary-value {
  font-weight: 600;
  color: #1c2e2a;
}

.col-right {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.reset-btn {
  background: none;
  border: 1.5px solid #c8ddd9;
  color: #5a6e6a;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition:
    border-color 0.2s,
    color 0.2s;
  width: 100%;
  margin-top: 0.25rem;
}
.reset-btn:hover {
  border-color: #2d7a3a;
  color: #2d7a3a;
}

.status-msg {
  text-align: center;
  padding: 3rem 0;
  color: #7a9490;
  font-size: 1rem;
}
.status-msg.error {
  color: #c0392b;
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
  .plan-wrap {
    grid-template-columns: 1fr;
  }
  .plan-right {
    position: static;
  }
}
</style>
