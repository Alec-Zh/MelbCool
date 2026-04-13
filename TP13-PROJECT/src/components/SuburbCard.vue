<script setup>
import HeatBadge from './HeatBadge.vue'

defineProps({
  suburb: {
    type: Object,
    required: true,
  },
  selected: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['select'])

const riskConfig = {
  high: { label: 'High Risk', bg: '#FEE2E2', color: '#991B1B' },
  moderate: { label: 'Moderate Risk', bg: '#FEF3C7', color: '#92400E' },
  low: { label: 'Low Risk', bg: '#DCFCE7', color: '#166534' },
}
</script>

<template>
  <div
    class="card"
    :class="{ selected }"
    @click="$emit('select', suburb)"
    role="button"
    :aria-pressed="selected"
  >
    <div class="card-top">
      <span class="suburb-name">{{ suburb.suburb_name }}</span>
      <HeatBadge :level="suburb.heat_level" />
    </div>
    <div class="card-meta">
      <span class="meta-item">
        <span class="meta-icon">🌡</span>
        {{ suburb.temperature }}°C
      </span>
      <span class="meta-item">
        <span class="meta-icon">🌳</span>
        {{ suburb.tree_canopy_percent }}% trees
      </span>
    </div>
    <div class="card-footer">
      <span
        v-if="suburb.risk_level"
        class="risk-tag"
        :style="{
          backgroundColor: riskConfig[suburb.risk_level]?.bg,
          color: riskConfig[suburb.risk_level]?.color,
        }"
      >
        {{ riskConfig[suburb.risk_level]?.label ?? suburb.risk_level }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.card {
  padding: 1rem 1.25rem;
  border-radius: var(--radius-card);
  border: 1.5px solid var(--color-border);
  background-color: var(--color-white);
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card:hover {
  border-color: var(--color-primary);
  background-color: var(--color-bg-light);
}

.card.selected {
  border-color: var(--color-primary);
  background-color: var(--color-bg-subtle);
  box-shadow: 0 0 0 3px rgba(13, 58, 143, 0.1);
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.suburb-name {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-text);
}

.card-meta {
  display: flex;
  gap: 1rem;
}

.meta-item {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.meta-icon {
  font-size: 0.9rem;
}

.card-footer {
  display: flex;
  align-items: center;
}

.risk-tag {
  font-size: 0.78rem;
  font-weight: 600;
  padding: 0.2rem 0.65rem;
  border-radius: 50px;
}
</style>
