<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import HeatBadge from './HeatBadge.vue'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
dayjs.extend(utc)
dayjs.extend(timezone)

const props = defineProps({
  suburb: { type: Object, required: true },
})

const emit = defineEmits(['close'])

const updatedAt = computed(() => {
  if (!props.suburb.updated_at) return null
  return dayjs.utc(props.suburb.updated_at).tz('Australia/Melbourne').format('D MMM YYYY, h:mm A')
})

function useCountUp(target, duration = 800) {
  const display = ref(0)
  let frame = null
  function animate(from, to) {
    cancelAnimationFrame(frame)
    const start = performance.now()
    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      display.value = Math.round(from + (to - from) * eased)
      if (progress < 1) frame = requestAnimationFrame(step)
    }
    frame = requestAnimationFrame(step)
  }
  watch(target, (to, from) => animate(from ?? 0, to ?? 0), { immediate: true })
  return display
}

const tempDisplay = useCountUp(computed(() => Math.round(props.suburb.temperature ?? 0)))
const apparentTempDisplay = useCountUp(
  computed(() => Math.round(props.suburb.apparent_temperature ?? 0)),
)
const uvDisplay = useCountUp(computed(() => Math.round(props.suburb.uv_index ?? 0)))
const vegDisplay = useCountUp(computed(() => Math.round(props.suburb.tree_canopy_percent ?? 0)))

const heatBarWidth = ref(0)
const shadeBarWidth = ref(0)

function animateBars() {
  heatBarWidth.value = 0
  shadeBarWidth.value = 0
  setTimeout(() => {
    heatBarWidth.value = Math.min(props.suburb.heat_score ?? 0, 100)
    shadeBarWidth.value = Math.min(100 - (props.suburb.shade_score ?? 0), 100)
  }, 120)
}

onMounted(animateBars)
watch(() => props.suburb.suburb_name, animateBars)

// heat_score: higher = more dangerous = red
function heatScoreColor(score) {
  if (score >= 65) return '#EF4444'
  if (score >= 40) return '#F97316'
  return '#22C55E'
}

// shade bar shows coverage (inverted): higher coverage = greener
function shadeCoverageColor(shadeScore) {
  const coverage = 100 - shadeScore
  if (coverage >= 65) return '#22C55E'
  if (coverage >= 40) return '#F97316'
  return '#EF4444'
}

const riskConfig = {
  high: { label: 'High Risk', bg: '#FEE2E2', color: '#991B1B' },
  moderate: { label: 'Moderate Risk', bg: '#FEF3C7', color: '#92400E' },
  low: { label: 'Low Risk', bg: '#DCFCE7', color: '#166534' },
}
</script>

<template>
  <div class="detail">
    <!-- Header -->
    <div class="detail-header">
      <div class="detail-title-row">
        <h2 class="detail-name">{{ suburb.suburb_name }}</h2>
        <button class="close-btn" @click="emit('close')" aria-label="Back to legend">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      <!-- Risk first, then heat -->
      <div class="detail-badges">
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

      <div v-if="updatedAt" class="updated-at">Data updated {{ updatedAt }} (Melbourne time)</div>
    </div>

    <!-- Stat cards 2×2 -->
    <div class="stats-grid">
      <div class="stat-card">
        <span class="stat-icon">🌡</span>
        <span class="stat-label">Temperature</span>
        <span class="stat-value">{{ tempDisplay }}°C</span>
        <span class="stat-sub">Current reading</span>
      </div>
      <div class="stat-card">
        <span class="stat-icon">🌤</span>
        <span class="stat-label">Feels Like</span>
        <span class="stat-value">{{ apparentTempDisplay }}°C</span>
        <span class="stat-sub">How hot it actually feels</span>
      </div>
      <div class="stat-card">
        <span class="stat-icon">☀️</span>
        <span class="stat-label">UV Index</span>
        <span class="stat-value">{{ uvDisplay }}</span>
        <span class="stat-sub">Sun exposure level</span>
      </div>
      <div class="stat-card">
        <span class="stat-icon">🌳</span>
        <span class="stat-label">Tree Coverage</span>
        <span class="stat-value">{{ vegDisplay }}%</span>
        <span class="stat-sub">Shade available in area</span>
      </div>
    </div>

    <!-- Risk breakdown -->
    <div class="score-section">
      <div class="score-title">What makes this area risky?</div>

      <div class="score-row">
        <div class="score-meta">
          <span class="score-label">🌳 Shade Coverage</span>
          <span class="score-note">How much tree shade is available</span>
        </div>
        <div class="score-bar-wrap">
          <div
            class="score-bar"
            :style="{
              width: shadeBarWidth + '%',
              backgroundColor: shadeCoverageColor(suburb.shade_score ?? 0),
            }"
          ></div>
        </div>
        <span class="score-num">
          {{ Math.round(100 - (suburb.shade_score ?? 0)) }}<span class="score-denom">/100</span>
        </span>
      </div>

      <div class="score-row">
        <div class="score-meta">
          <span class="score-label">🌡 Heat Score</span>
          <span class="score-note">Based on how hot it feels and sun exposure today</span>
        </div>
        <div class="score-bar-wrap">
          <div
            class="score-bar"
            :style="{
              width: heatBarWidth + '%',
              backgroundColor: heatScoreColor(suburb.heat_score ?? 0),
            }"
          ></div>
        </div>
        <span class="score-num">
          {{ Math.round(suburb.heat_score ?? 0) }}<span class="score-denom">/100</span>
        </span>
      </div>

      <div class="score-note-bottom">
        Risk is mostly driven by today's heat conditions, with tree shade as a secondary factor.
      </div>
    </div>
  </div>
</template>

<style scoped>
.detail {
  padding: 1.25rem;
  background-color: var(--color-white);
  border-radius: var(--radius-card);
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
}

.detail-name {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--color-text);
  line-height: 1.2;
}

.close-btn {
  flex-shrink: 0;
  background: var(--color-bg-light, #f1f5f9);
  border: 1px solid var(--color-border);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-text-muted);
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
  margin-top: 2px;
}

.close-btn:hover {
  background-color: #e2e8f0;
  color: var(--color-text);
}

.detail-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.risk-tag {
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
}

.updated-at {
  font-size: 0.82rem;
  color: var(--color-text-muted);
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  padding: 0.85rem;
  background-color: var(--color-bg-light);
  border-radius: var(--radius-card);
  border: 1px solid var(--color-border);
}

.stat-icon {
  font-size: 1.2rem;
  margin-bottom: 0.1rem;
}

.stat-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--color-text-muted);
}

.stat-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--color-text);
  line-height: 1.1;
}

.stat-sub {
  font-size: 0.78rem;
  color: var(--color-text-muted);
}

.score-section {
  background-color: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.score-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-text);
}

.score-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.score-meta {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 150px;
}

.score-label {
  font-size: 0.88rem;
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
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-text);
  min-width: 48px;
  text-align: right;
}

.score-denom {
  font-size: 0.72rem;
  font-weight: 400;
  color: var(--color-text-muted);
}

.score-note-bottom {
  font-size: 0.82rem;
  color: var(--color-text-muted);
  padding-top: 0.5rem;
  border-top: 1px solid var(--color-border);
}
</style>
