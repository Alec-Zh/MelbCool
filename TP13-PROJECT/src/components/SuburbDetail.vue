<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import HeatBadge from './HeatBadge.vue'
import HeatAdviceCard from './HeatAdviceCard.vue'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
dayjs.extend(utc)
dayjs.extend(timezone)

const props = defineProps({
  suburb: { type: Object, required: true },
})

const emit = defineEmits(['close'])

const showAdvice = ref(false)

// Reset advice modal when suburb changes
watch(
  () => props.suburb.suburb_name,
  () => {
    showAdvice.value = false
  },
)

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
  if (score >= 65) return '#c0392b'
  if (score >= 40) return '#e8903a'
  return '#4d9e5a'
}

// shade bar shows coverage (inverted): higher coverage = greener
function shadeCoverageColor(shadeScore) {
  const coverage = 100 - shadeScore
  if (coverage >= 65) return '#4d9e5a'
  if (coverage >= 40) return '#e8903a'
  return '#c0392b'
}

const riskConfig = {
  high: { label: 'High Risk', bg: '#fce8e6', color: '#8b1a12' },
  moderate: { label: 'Moderate Risk', bg: '#fef1e0', color: '#7a4510' },
  low: { label: 'Low Risk', bg: '#e6f4e8', color: '#1e5c28' },
}

const adviceButtonConfig = {
  high: { label: 'View safety advice', bg: '#c0392b', color: '#fff' },
  moderate: { label: 'View safety advice', bg: '#c97a2a', color: '#fff' },
  low: { label: 'View safety advice', bg: '#2d7a3a', color: '#fff' },
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

      <!-- Risk badge -->
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

        <!-- 🧪 TEST ONLY — remove before production -->
        <span v-if="suburb.suburb_id === 9999" class="test-tag">TEST</span>
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
          <span class="score-label">Shade Coverage</span>
          <span class="score-note">How much tree shade is available</span>
        </div>
        <div class="seg-wrap">
          <div class="seg" :class="{ active: (suburb.shade_score ?? 0) < 40 }" style="--c: #4d9e5a">Good</div>
          <div class="seg" :class="{ active: (suburb.shade_score ?? 0) >= 40 && (suburb.shade_score ?? 0) < 65 }" style="--c: #e8903a">Limited</div>
          <div class="seg" :class="{ active: (suburb.shade_score ?? 0) >= 65 }" style="--c: #c0392b">Very little</div>
        </div>
      </div>

      <div class="score-row">
        <div class="score-meta">
          <span class="score-label">Heat Score</span>
          <span class="score-note">Based on how hot it feels and sun exposure today</span>
        </div>
        <div class="seg-wrap">
          <div class="seg" :class="{ active: (suburb.heat_score ?? 0) < 40 }" style="--c: #4d9e5a">Low</div>
          <div class="seg" :class="{ active: (suburb.heat_score ?? 0) >= 40 && (suburb.heat_score ?? 0) < 65 }" style="--c: #e8903a">Moderate</div>
          <div class="seg" :class="{ active: (suburb.heat_score ?? 0) >= 65 }" style="--c: #c0392b">High</div>
        </div>
      </div>

      <div class="score-note-bottom">
        Risk is mostly driven by today's heat conditions, with tree shade as a secondary factor.
      </div>
    </div>
    <!-- AC3.1.1 / AC3.2.1 — Safety advice button -->
    <button
      v-if="suburb.risk_level"
      class="advice-btn"
      :style="{
        backgroundColor: adviceButtonConfig[suburb.risk_level]?.bg,
        color: adviceButtonConfig[suburb.risk_level]?.color,
      }"
      @click="showAdvice = true"
    >
      <span class="advice-btn-icon">🛡️</span>
      View safety advice
      <svg
        class="advice-btn-arrow"
        width="14"
        height="14"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <line x1="5" y1="12" x2="19" y2="12" />
        <polyline points="12 5 19 12 12 19" />
      </svg>
    </button>

    <!-- AC3.1.1 / AC3.2.1 — Advice modal -->
    <HeatAdviceCard
      v-if="showAdvice"
      :riskLevel="suburb.risk_level"
      :heatScore="suburb.heat_score ?? 0"
      :shadeScore="suburb.shade_score ?? 0"
      @close="showAdvice = false"
    />
  </div>
</template>

<style scoped>
.detail {
  padding: 1.25rem;
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #d8eae6;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-shadow: none;
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
  font-size: 1.35rem;
  font-weight: 800;
  color: #1a1714;
  line-height: 1.2;
  letter-spacing: -0.01em;
}

.close-btn {
  flex-shrink: 0;
  background: #f0f7f5;
  border: 1px solid #d8eae6;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #6b6560;
  transition: background-color 0.15s, color 0.15s;
  margin-top: 2px;
}
.close-btn:hover {
  background-color: #ede9e1;
  color: #1a1714;
}

.detail-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.risk-tag {
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.25rem 0.8rem;
  border-radius: 50px;
  letter-spacing: 0.02em;
}

.updated-at {
  font-size: 0.78rem;
  color: #9e9890;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.6rem;
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  padding: 0.85rem;
  background: #f4faf8;
  border-radius: 10px;
  border: 1px solid #d8eae6;
  transition: border-color 0.2s;
}
.stat-card:hover {
  border-color: #4d9e5a;
}

.stat-icon {
  font-size: 1.1rem;
  margin-bottom: 0.1rem;
}

.stat-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b6560;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 1.45rem;
  font-weight: 800;
  color: #1a1714;
  line-height: 1.1;
  letter-spacing: -0.01em;
}

.stat-sub {
  font-size: 0.72rem;
  color: #9e9890;
  line-height: 1.4;
}

.score-section {
  background: #f0f7f5;
  border: 1px solid #d8eae6;
  border-radius: 10px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.score-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: #6b6560;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.score-row {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.score-bar-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.score-meta {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.score-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1a1714;
}

.score-note {
  font-size: 0.75rem;
  color: #9e9890;
}

.seg-wrap {
  display: flex;
  gap: 0.3rem;
  margin-top: 0.4rem;
}

.seg {
  flex: 1;
  padding: 0.3rem 0;
  text-align: center;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 6px;
  background: #f0f0f0;
  color: #aaa;
  transition: background 0.2s, color 0.2s;
}

.seg.active {
  background: var(--c);
  color: #ffffff;
}

.score-note-bottom {
  font-size: 0.78rem;
  color: #7a9490;
  padding-top: 0.5rem;
  border-top: 1px solid #e3ded5;
  font-style: italic;
}

/* Advice button */
.advice-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 10px;
  font-size: 0.92rem;
  font-weight: 700;
  cursor: pointer;
  transition: filter 0.15s, transform 0.1s;
  letter-spacing: 0.02em;
}
.advice-btn:hover {
  filter: brightness(1.12);
}
.advice-btn:active {
  transform: scale(0.98);
}

.advice-btn-icon { font-size: 1rem; }

.advice-btn-arrow {
  margin-left: auto;
  opacity: 0.7;
}

/* TEST badge */
.test-tag {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 50px;
  background: #1e1e1e;
  color: #facc15;
  letter-spacing: 0.08em;
}
</style>