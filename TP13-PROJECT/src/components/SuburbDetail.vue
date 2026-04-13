<script setup>
import { computed } from 'vue'
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

const heatAdvice = {
  higher: {
    title: '🌡️ Hot Conditions Right Now',
    text: "It's currently hot in this suburb. Avoid being outdoors during midday, stay cool indoors with air conditioning, and drink plenty of water. Ask someone for help if you're feeling unwell.",
    bg: '#FEF2F2',
    border: '#FECACA',
    color: '#991B1B',
  },
  moderate: {
    title: '🌡️ Warm Conditions Right Now',
    text: 'Temperatures are moderate. Stay hydrated and take breaks in the shade if you go outside. Avoid long periods outdoors during the warmest part of the day.',
    bg: '#FFFBEB',
    border: '#FDE68A',
    color: '#92400E',
  },
  lower: {
    title: '🌡️ Cool Conditions Right Now',
    text: 'Temperatures are relatively low at the moment. Normal precautions apply — keep hydrated and be mindful on warmer days.',
    bg: '#F0FDF4',
    border: '#BBF7D0',
    color: '#166534',
  },
}

const riskAdvice = {
  high: {
    title: '⚠️ High Vulnerability Area',
    text: 'This suburb has a high concentration of older residents and limited tree cover. Extra support and cooling resources may be needed here during hot weather.',
    bg: '#FEF2F2',
    border: '#FECACA',
    color: '#991B1B',
  },
  moderate: {
    title: '⚡ Moderate Vulnerability Area',
    text: 'Some combination of heat, older population, or limited greenery puts this suburb at moderate risk. Keep an eye on conditions during hot spells.',
    bg: '#FFFBEB',
    border: '#FDE68A',
    color: '#92400E',
  },
  low: {
    title: '✅ Lower Vulnerability Area',
    text: 'Good tree coverage and cooler conditions make this suburb generally safer for older residents during hot weather. Still take care on extreme heat days.',
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
  <div class="detail">
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

    <div class="stats-grid">
      <div class="stat-card">
        <span class="stat-icon">🌡</span>
        <span class="stat-label">Temperature</span>
        <span class="stat-value">{{ suburb.temperature }}°C</span>
        <span class="stat-sub">Current reading</span>
      </div>
      <div class="stat-card">
        <span class="stat-icon">🌳</span>
        <span class="stat-label">Tree Coverage</span>
        <span class="stat-value">{{ suburb.tree_canopy_percent }}%</span>
        <span class="stat-sub">Vegetation cover</span>
      </div>
      <div class="stat-card">
        <span class="stat-icon">👴</span>
        <span class="stat-label">Elderly Population</span>
        <span class="stat-value">{{ suburb.elderly_population?.toLocaleString() ?? '—' }}</span>
        <span class="stat-sub">Residents 60+ years</span>
      </div>
      <div class="stat-card">
        <span class="stat-icon">👥</span>
        <span class="stat-label">Total Population</span>
        <span class="stat-value">{{ suburb.total_population?.toLocaleString() ?? '—' }}</span>
        <span class="stat-sub">2021 Census</span>
      </div>
    </div>

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
  </div>
</template>

<style scoped>
.detail {
  padding: 1.5rem;
  background-color: var(--color-white);
  border-radius: var(--radius-card);
  border: 1px solid var(--color-border);
}

.detail-header {
  margin-bottom: 1.25rem;
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
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text);
}

.risk-tag {
  font-size: 0.82rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
}

.updated-at {
  font-size: 0.8rem;
  color: var(--color-text-muted);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.25rem;
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
  font-size: 1.2rem;
  margin-bottom: 0.2rem;
}

.stat-label {
  font-size: 0.8rem;
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
  font-size: 0.78rem;
  color: var(--color-text-muted);
}

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
  font-size: 0.95rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.advice-text {
  font-size: 0.9rem;
  line-height: 1.6;
}
</style>
