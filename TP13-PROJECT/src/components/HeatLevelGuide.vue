<template>
  <div class="guide">
    <h3 class="guide-title">Understanding Heat Risk</h3>

    <!-- Heat Level -->
    <div class="section">
      <div class="section-label">🌡 Heat Level — based on current temperature</div>
      <ul class="guide-list">
        <li v-for="item in heatLevels" :key="item.level" class="guide-item">
          <span class="dot" :style="{ backgroundColor: item.color }"></span>
          <div>
            <span class="guide-label">{{ item.label }}</span>
            <span class="guide-desc"> {{ item.desc }}</span>
          </div>
        </li>
      </ul>
    </div>

    <!-- Risk Level -->
    <div class="section">
      <div class="section-label">⚠️ Risk Level — combined score for older residents</div>
      <ul class="guide-list">
        <li v-for="item in riskLevels" :key="item.level" class="guide-item">
          <span class="dot" :style="{ backgroundColor: item.color }"></span>
          <div>
            <span class="guide-label">{{ item.label }}</span>
            <span class="guide-desc"> {{ item.desc }}</span>
          </div>
        </li>
      </ul>
    </div>

    <!-- How it's calculated -->
    <div class="formula-box">
      <div class="formula-title">How risk is calculated</div>
      <div class="formula-row">
        <span class="formula-tag heat">Heat Score (50%)</span>
        <span class="formula-text">Real-time temperature — higher temp = higher score</span>
      </div>
      <div class="formula-row">
        <span class="formula-tag vuln">Vulnerability Score (50%)</span>
        <span class="formula-text"
          >Proportion of residents aged 60+ × elderly heat sensitivity + low vegetation coverage
          penalty</span
        >
      </div>
      <div class="formula-note">
        💡 Two suburbs at the same temperature may have different risk levels — areas with more
        older residents and less tree cover are rated higher risk.
      </div>
    </div>
  </div>
</template>

<script setup>
const heatLevels = [
  {
    level: 'higher',
    color: '#EF4444',
    label: 'Higher Heat (≥ 35°C):',
    desc: 'Dangerous heat for older adults. Avoid outdoor activity during midday.',
  },
  {
    level: 'moderate',
    color: '#F97316',
    label: 'Moderate Heat (28–34°C):',
    desc: 'Caution advised. Stay hydrated and seek shade regularly.',
  },
  {
    level: 'lower',
    color: '#22C55E',
    label: 'Lower Heat (< 28°C):',
    desc: 'Relatively safe. Normal precautions apply on warm days.',
  },
]

const riskLevels = [
  {
    level: 'high',
    color: '#DC2626',
    label: 'High Risk:',
    desc: 'High heat combined with large elderly population and low vegetation. Extra care needed.',
  },
  {
    level: 'moderate',
    color: '#D97706',
    label: 'Moderate Risk:',
    desc: 'Some combination of heat, elderly residents, or limited greenery. Stay alert.',
  },
  {
    level: 'low',
    color: '#16A34A',
    label: 'Low Risk:',
    desc: 'Cooler conditions, good tree cover, or lower elderly population density.',
  },
]
</script>

<style scoped>
.guide {
  padding: 1.25rem 1.5rem;
  background-color: var(--color-bg-subtle);
  border-radius: var(--radius-card);
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.guide-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.25rem;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.section-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-text);
}

.guide-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding-left: 0.25rem;
}

.guide-item {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  font-size: 0.85rem;
  color: var(--color-text);
  line-height: 1.5;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 4px;
}

.guide-label {
  font-weight: 600;
}

.guide-desc {
  color: var(--color-text-muted);
}

.formula-box {
  background-color: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.formula-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.15rem;
}

.formula-row {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  font-size: 0.82rem;
}

.formula-tag {
  flex-shrink: 0;
  padding: 0.2rem 0.6rem;
  border-radius: 50px;
  font-size: 0.78rem;
  font-weight: 700;
  white-space: nowrap;
}

.formula-tag.heat {
  background-color: #fee2e2;
  color: #991b1b;
}

.formula-tag.vuln {
  background-color: #dbeafe;
  color: #1e40af;
}

.formula-text {
  color: var(--color-text-muted);
  line-height: 1.5;
  padding-top: 0.15rem;
}

.formula-note {
  font-size: 0.82rem;
  color: var(--color-text-muted);
  line-height: 1.5;
  padding-top: 0.25rem;
  border-top: 1px solid var(--color-border);
}
</style>
