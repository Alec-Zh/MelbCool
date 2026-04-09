<script setup>
import HeatBadge from './HeatBadge.vue'

defineProps({
  suburb: {
    type: Object,
    required: true,
    // { suburb_name, temperature, tree_canopy_percent, heat_level }
  },
  selected: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['select'])
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
  margin-bottom: 0.6rem;
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
</style>
