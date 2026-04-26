<script setup>
const riskLevels = [
  {
    color: '#DC2626',
    label: 'High Risk',
    desc: 'High heat and very little tree shade in this area.',
  },
  {
    color: '#D97706',
    label: 'Moderate Risk',
    desc: 'Moderate heat or limited tree shade in this area.',
  },
  {
    color: '#16A34A',
    label: 'Low Risk',
    desc: 'Cooler conditions and good tree shade in this area.',
  },
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
      <div class="score-legend-section">
        <div class="section-header">📊 How scores work</div>
        <div class="score-legend">
          <div class="score-legend-item">
            <span>🌡 Heat Score</span>
            <span class="score-legend-desc">How hot it feels today, including UV exposure</span>
          </div>
          <div class="score-legend-item">
            <span>🌳 Shade Score</span>
            <span class="score-legend-desc">How much tree shade is available in the area</span>
          </div>
          <div class="score-legend-formula">
            Overall risk = Heat Score × 70% + Shade Score × 30%
          </div>
        </div>
      </div>
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
  height: 100%;
  box-sizing: border-box;
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

.score-legend {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  font-size: 0.82rem;
  color: var(--color-text-muted);
  line-height: 1.55;
}

.score-legend-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.score-legend-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.score-legend-desc {
  padding-left: 1.4rem;
  color: var(--color-text-muted);
}

.score-legend-formula {
  padding-top: 0.5rem;
  margin-top: 0.25rem;
  border-top: 1px solid var(--color-border);
  font-size: 0.78rem;
  color: var(--color-text-muted);
}
</style>
