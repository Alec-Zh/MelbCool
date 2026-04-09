<script setup>
import HeatBadge from './HeatBadge.vue'

defineProps({
  suburb: {
    type: Object,
    required: true,
    // { suburb_name, temperature, tree_canopy_percent, heat_level,
    //   elderly_population, total_population, risk_level }
  },
})

const advice = {
  higher: {
    title: 'Higher Heat Area',
    text: 'This area experiences warmer conditions during hot weather. Consider spending time in air-conditioned locations during the warmest part of the day. Stay hydrated and take regular breaks in cool spaces.',
    bg: '#FEF2F2',
    border: '#FECACA',
    color: '#991B1B',
  },
  moderate: {
    title: 'Moderate Heat Area',
    text: 'This area has average heat conditions. Take usual precautions during hot days — stay hydrated, wear sunscreen, and seek shade when needed.',
    bg: '#FFFBEB',
    border: '#FDE68A',
    color: '#92400E',
  },
  lower: {
    title: 'Lower Heat Area',
    text: 'This area benefits from good tree coverage and cooler conditions. Still take care during extreme heat days and keep hydrated.',
    bg: '#F0FDF4',
    border: '#BBF7D0',
    color: '#166534',
  },
}
</script>

<template>
  <div class="detail">
    <div class="detail-header">
      <h2 class="detail-name">{{ suburb.suburb_name }}</h2>
      <HeatBadge :level="suburb.heat_level" />
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <span class="stat-icon">🌡</span>
        <span class="stat-label">Temperature</span>
        <span class="stat-value">{{ suburb.temperature }}°C</span>
        <span class="stat-sub">Current forecast</span>
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
        <span class="stat-sub">Residents 65+ years</span>
      </div>
    </div>

    <div
      class="advice-box"
      :style="{
        backgroundColor: advice[suburb.heat_level].bg,
        borderColor: advice[suburb.heat_level].border,
      }"
    >
      <div class="advice-title" :style="{ color: advice[suburb.heat_level].color }">
        ⚠ {{ advice[suburb.heat_level].title }}
      </div>
      <p class="advice-text" :style="{ color: advice[suburb.heat_level].color }">
        {{ advice[suburb.heat_level].text }}
      </p>
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
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.detail-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.25rem;
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
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--color-text);
  line-height: 1.1;
}

.stat-sub {
  font-size: 0.78rem;
  color: var(--color-text-muted);
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
