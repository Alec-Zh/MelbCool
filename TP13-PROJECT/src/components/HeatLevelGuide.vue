<script setup>
const riskLevels = [
  { color: '#DC2626', label: 'High Risk', desc: 'High heat score and high vulnerability score.' },
  {
    color: '#D97706',
    label: 'Moderate Risk',
    desc: 'Moderate combined heat and vulnerability score.',
  },
  { color: '#16A34A', label: 'Low Risk', desc: 'Low combined heat and vulnerability score.' },
]

const heatLevels = [
  { color: '#EF4444', label: 'Hot', range: '≥ 35°C' },
  { color: '#F97316', label: 'Warm', range: '28–34°C' },
  { color: '#22C55E', label: 'Mild', range: '< 28°C' },
]
</script>

<template>
  <div class="guide">
    <h3 class="guide-title">Map Legend</h3>

    <!-- Risk Level first -->
    <div class="section">
      <div class="section-header">⚠️ Risk Level</div>
      <ul class="item-list">
        <li v-for="item in riskLevels" :key="item.label" class="item item-block">
          <div class="item-row">
            <span class="dot" :style="{ backgroundColor: item.color }"></span>
            <span class="item-label">{{ item.label }}</span>
          </div>
          <span class="item-desc">{{ item.desc }}</span>
        </li>
      </ul>
      <p class="section-note">
        Risk = Vulnerability Score × 50% + Heat Score × 50%.<br />
        Vulnerability is based on residents aged 60+ (ABS 2021 Census) and tree canopy coverage.
      </p>
    </div>

    <!-- Heat Level second -->
    <div class="section">
      <div class="section-header">🌡 Heat Level</div>
      <ul class="item-list">
        <li v-for="item in heatLevels" :key="item.label" class="item">
          <span class="dot" :style="{ backgroundColor: item.color }"></span>
          <span class="item-label">{{ item.label }}</span>
          <span class="item-range">{{ item.range }}</span>
        </li>
      </ul>
      <p class="section-note">Based on current temperature from Open-Meteo.</p>
    </div>
  </div>
</template>

<style scoped>
.guide {
  padding: 1.25rem;
  background-color: var(--color-white);
  border-radius: var(--radius-card);
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.guide-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.section-header {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-muted);
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--color-border);
}

.item-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.5rem 0.75rem;
  background-color: var(--color-bg-light, #f8fafc);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
}

.item-block {
  flex-direction: column;
  align-items: flex-start;
  gap: 0.3rem;
}

.item-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.dot {
  width: 11px;
  height: 11px;
  border-radius: 50%;
  flex-shrink: 0;
}

.item-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text);
  flex: 1;
}

.item-range {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}

.item-desc {
  font-size: 0.82rem;
  color: var(--color-text-muted);
  line-height: 1.5;
  padding-left: 1.4rem;
}

.section-note {
  font-size: 0.8rem;
  color: var(--color-text-muted);
  line-height: 1.55;
  margin: 0;
}
</style>
