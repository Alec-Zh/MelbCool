<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import HeatBadge from './HeatBadge.vue'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
dayjs.extend(utc)
dayjs.extend(timezone)

const props = defineProps({
  suburb: {
    type: Object,
    required: true,
  },
})

const updatedAt = computed(() => {
  if (!props.suburb.updated_at) return null
  return dayjs.utc(props.suburb.updated_at).tz('Australia/Melbourne').format('D MMM YYYY, h:mm A')
})

// ── Count-up animation ────────────────────────────────
function useCountUp(target, duration = 800) {
  const display = ref(0)
  let frame = null

  function animate(from, to) {
    cancelAnimationFrame(frame)
    const start = performance.now()
    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3) // ease-out cubic
      display.value = Math.round(from + (to - from) * eased)
      if (progress < 1) frame = requestAnimationFrame(step)
    }
    frame = requestAnimationFrame(step)
  }

  watch(target, (to, from) => animate(from ?? 0, to ?? 0), { immediate: true })
  return display
}

const tempDisplay = useCountUp(computed(() => Math.round(props.suburb.temperature ?? 0)))
const vegDisplay = useCountUp(computed(() => Math.round(props.suburb.tree_canopy_percent ?? 0)))
const elderlyDisplay = useCountUp(
  computed(() => props.suburb.elderly_population ?? 0),
  1000,
)
const totalDisplay = useCountUp(
  computed(() => props.suburb.total_population ?? 0),
  1000,
)

// ── Progress bar animation ────────────────────────────
const heatBarWidth = ref(0)
const vulnBarWidth = ref(0)

function animateBars() {
  heatBarWidth.value = 0
  vulnBarWidth.value = 0
  setTimeout(() => {
    heatBarWidth.value = Math.min(props.suburb.heat_score ?? 0, 100)
    vulnBarWidth.value = Math.min(props.suburb.vulnerability_score ?? 0, 100)
  }, 120) // slight delay so transition kicks in after mount
}

onMounted(animateBars)
watch(() => props.suburb.suburb_name, animateBars)

// ── Risk score colour ─────────────────────────────────
function scoreColor(score) {
  if (score >= 65) return '#EF4444'
  if (score >= 40) return '#F97316'
  return '#22C55E'
}

const heatAdvice = {
  higher: {
    title: '🌡️ It Is Hot Right Now',
    text: "It's currently hot in this suburb. Stay indoors and keep cool with air conditioning. Drink plenty of water and ask someone for help if you feel unwell.",
    bg: '#FEF2F2',
    border: '#FECACA',
    color: '#991B1B',
  },
  moderate: {
    title: '🌡️ It Is Warm Right Now',
    text: 'Temperatures are warm. Drink water regularly and rest in the shade if you go outside. Avoid being outdoors during the hottest part of the day.',
    bg: '#FFFBEB',
    border: '#FDE68A',
    color: '#92400E',
  },
  lower: {
    title: '🌡️ It Is Mild Right Now',
    text: 'Temperatures are comfortable at the moment. Keep hydrated and take care on warmer days.',
    bg: '#F0FDF4',
    border: '#BBF7D0',
    color: '#166534',
  },
}

const riskAdvice = {
  high: {
    title: '⚠️ High Risk Area',
    text: 'This suburb has many older residents and limited tree cover. Extra support and cooling resources may be needed during hot weather.',
    bg: '#FEF2F2',
    border: '#FECACA',
    color: '#991B1B',
  },
  moderate: {
    title: '⚠️ Moderate Risk Area',
    text: 'This suburb has some heat risk due to temperature, older residents, or limited greenery. Keep an eye on conditions during hot weather.',
    bg: '#FFFBEB',
    border: '#FDE68A',
    color: '#92400E',
  },
  low: {
    title: '✅ Lower Risk Area',
    text: 'Good tree coverage and cooler conditions make this suburb generally safer for older residents. Still take care on very hot days.',
    bg: '#F0FDF4',
    border: '#BBF7D0',
    color: '#166534',
  },
}

const riskConfig = {
  high: { label: 'High Risk', bg: '#FEE2E2', color: '#991B1B' },
  moderate: { label: 'Moderate Risk', bg: '#FEF3C7', color: '#92400E' },
  low: { label: 'Low Risk', bg: '#DCFCE7', color: '#166534' },
}
</script>

<template>
  <Transition name="slide-up" appear>
    <div class="detail">
      <!-- Header -->
      <div class="detail-header">
        <div class="detail-title-row">
          <h2 class="detail-name">{{ suburb.suburb_name }}</h2>
          <div class="detail-badges">
            <HeatBadge :level="suburb.heat_level" />
            <span
              v-if="suburb.risk_level"
              class="risk-tag"
              :style="{
                backgroundColor: riskConfig[suburb.risk_level]?.bg,
                color: riskConfig[suburb.risk_level]?.color,
              }"
            >
              {{ riskConfig[suburb.risk_level]?.label }}
            </span>
          </div>
        </div>
        <div v-if="updatedAt" class="updated-at">
          🕐 Data updated {{ updatedAt }} (Melbourne time)
        </div>
      </div>

      <!-- Stat cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <span class="stat-icon">🌡</span>
          <span class="stat-label">Temperature</span>
          <span class="stat-value">{{ tempDisplay }}°C</span>
          <span class="stat-sub">Current reading</span>
        </div>
        <div class="stat-card">
          <span class="stat-icon">🌳</span>
          <span class="stat-label">Tree Coverage</span>
          <span class="stat-value">{{ vegDisplay }}%</span>
          <span class="stat-sub">% of area covered by trees</span>
        </div>
        <div class="stat-card">
          <span class="stat-icon">👴</span>
          <span class="stat-label">Older Residents</span>
          <span class="stat-value">{{ elderlyDisplay.toLocaleString() }}</span>
          <span class="stat-sub">Residents aged 60+</span>
        </div>
        <div class="stat-card">
          <span class="stat-icon">👥</span>
          <span class="stat-label">Total Population</span>
          <span class="stat-value">{{ totalDisplay.toLocaleString() }}</span>
          <span class="stat-sub">2021 Census</span>
        </div>
      </div>

      <!-- Advice boxes -->
      <div class="advice-row">
        <div
          class="advice-box"
          :style="{
            backgroundColor: heatAdvice[suburb.heat_level]?.bg,
            borderColor: heatAdvice[suburb.heat_level]?.border,
          }"
        >
          <div class="advice-title" :style="{ color: heatAdvice[suburb.heat_level]?.color }">
            {{ heatAdvice[suburb.heat_level]?.title }}
          </div>
          <p class="advice-text" :style="{ color: heatAdvice[suburb.heat_level]?.color }">
            {{ heatAdvice[suburb.heat_level]?.text }}
          </p>
        </div>
        <div
          v-if="suburb.risk_level"
          class="advice-box"
          :style="{
            backgroundColor: riskAdvice[suburb.risk_level]?.bg,
            borderColor: riskAdvice[suburb.risk_level]?.border,
          }"
        >
          <div class="advice-title" :style="{ color: riskAdvice[suburb.risk_level]?.color }">
            {{ riskAdvice[suburb.risk_level]?.title }}
          </div>
          <p class="advice-text" :style="{ color: riskAdvice[suburb.risk_level]?.color }">
            {{ riskAdvice[suburb.risk_level]?.text }}
          </p>
        </div>
      </div>

      <!-- How risk is calculated -->
      <div class="score-section">
        <div class="score-title">How risk is calculated</div>

        <div class="score-row">
          <div class="score-meta">
            <span class="score-label heat-label">🌡 Heat Score</span>
            <span class="score-note">Based on current temperature</span>
          </div>
          <div class="score-bar-wrap">
            <div
              class="score-bar heat-bar"
              :style="{
                width: heatBarWidth + '%',
                backgroundColor: scoreColor(suburb.heat_score ?? 0),
              }"
            ></div>
          </div>
          <span class="score-num"
            >{{ Math.round(suburb.heat_score ?? 0) }}<span class="score-denom">/100</span></span
          >
        </div>

        <div class="score-row">
          <div class="score-meta">
            <span class="score-label vuln-label">👴 Vulnerability Score</span>
            <span class="score-note">Based on older residents and tree cover</span>
          </div>
          <div class="score-bar-wrap">
            <div
              class="score-bar vuln-bar"
              :style="{
                width: vulnBarWidth + '%',
                backgroundColor: scoreColor(suburb.vulnerability_score ?? 0),
              }"
            ></div>
          </div>
          <span class="score-num"
            >{{ Math.round(suburb.vulnerability_score ?? 0)
            }}<span class="score-denom">/100</span></span
          >
        </div>

        <div class="score-note-bottom">
          💡 Risk level combines both scores equally. Areas with more older residents and less tree
          cover are rated higher risk.
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* ── Slide-up entrance animation ── */
.slide-up-enter-active {
  transition:
    opacity 0.4s ease,
    transform 0.4s ease;
}
.slide-up-enter-from {
  opacity: 0;
  transform: translateY(16px);
}

.detail {
  padding: 1.5rem;
  background-color: var(--color-white);
  border-radius: var(--radius-card);
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.detail-header {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.detail-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.detail-badges {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-name {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--color-text);
}

.risk-tag {
  font-size: 0.9rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
}

.updated-at {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

/* ── Stat cards ── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.2rem;
  padding: 1rem;
  background-color: var(--color-bg-light);
  border-radius: var(--radius-card);
  border: 1px solid var(--color-border);
}

.stat-icon {
  font-size: 1.3rem;
  margin-bottom: 0.2rem;
}
.stat-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text);
  line-height: 1.1;
}
.stat-sub {
  font-size: 0.82rem;
  color: var(--color-text-muted);
}

/* ── Advice boxes ── */
.advice-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 640px) {
  .advice-row {
    grid-template-columns: 1fr;
  }
}

.advice-box {
  border: 1px solid;
  border-radius: var(--radius-card);
  padding: 1rem 1.25rem;
}
.advice-title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.advice-text {
  font-size: 0.95rem;
  line-height: 1.7;
}

/* ── Score section ── */
.score-section {
  background-color: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  padding: 1.1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.score-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-text);
}

.score-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.score-meta {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 190px;
}

.score-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text);
}

.score-note {
  font-size: 0.78rem;
  color: var(--color-text-muted);
}

.score-bar-wrap {
  flex: 1;
  height: 10px;
  background-color: var(--color-border);
  border-radius: 50px;
  overflow: hidden;
}

.score-bar {
  height: 100%;
  border-radius: 50px;
  width: 0%;
  transition: width 0.9s cubic-bezier(0.25, 1, 0.5, 1);
}

.score-num {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-text);
  min-width: 52px;
  text-align: right;
}

.score-denom {
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--color-text-muted);
}

.score-note-bottom {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  line-height: 1.6;
  padding-top: 0.25rem;
  border-top: 1px solid var(--color-border);
}
</style>
