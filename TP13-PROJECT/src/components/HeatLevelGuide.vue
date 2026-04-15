<script setup>
import { ref } from 'vue'

const heatLevels = [
  {
    level: 'higher',
    color: '#EF4444',
    label: 'Hot (≥ 35°C)',
    desc: 'Dangerous heat for older adults. Stay indoors, keep cool, and drink plenty of water.',
  },
  {
    level: 'moderate',
    color: '#F97316',
    label: 'Warm (28–34°C)',
    desc: 'Take care outdoors. Stay hydrated and rest in the shade regularly.',
  },
  {
    level: 'lower',
    color: '#22C55E',
    label: 'Mild (< 28°C)',
    desc: 'Conditions are comfortable. Still stay hydrated on warmer days.',
  },
]

const riskLevels = [
  {
    level: 'high',
    color: '#DC2626',
    label: 'High Risk',
    desc: 'This area has high heat, many older residents, and little tree cover. Extra care is needed.',
  },
  {
    level: 'moderate',
    color: '#D97706',
    label: 'Moderate Risk',
    desc: 'Some heat risk due to temperature, older residents, or limited greenery. Stay alert.',
  },
  {
    level: 'low',
    color: '#16A34A',
    label: 'Low Risk',
    desc: 'Cooler temperatures and good tree cover make this area safer during hot weather.',
  },
]

// Track which item is expanded: 'heat-0', 'risk-1', etc.
const expanded = ref(new Set())

function toggle(key) {
  if (expanded.value.has(key)) {
    expanded.value.delete(key)
  } else {
    expanded.value.add(key)
  }
  // trigger reactivity
  expanded.value = new Set(expanded.value)
}
</script>

<template>
  <div class="guide">
    <h3 class="guide-title">Understanding Heat Risk</h3>

    <div class="columns">
      <!-- Heat Level column -->
      <div class="column">
        <div class="col-header">🌡 Heat Level</div>
        <ul class="item-list">
          <li
            v-for="(item, i) in heatLevels"
            :key="item.level"
            class="item"
            :class="{ active: expanded.has(`heat-${i}`) }"
            @click="toggle(`heat-${i}`)"
          >
            <div class="item-row">
              <span class="dot" :style="{ backgroundColor: item.color }"></span>
              <span class="item-label">{{ item.label }}</span>
              <span class="chevron">{{ expanded.has(`heat-${i}`) ? '▲' : '▼' }}</span>
            </div>
            <Transition name="expand">
              <div v-if="expanded.has(`heat-${i}`)" class="item-desc">{{ item.desc }}</div>
            </Transition>
          </li>
        </ul>
      </div>

      <!-- Risk Level column -->
      <div class="column">
        <div class="col-header">⚠️ Risk Level</div>
        <ul class="item-list">
          <li
            v-for="(item, i) in riskLevels"
            :key="item.level"
            class="item"
            :class="{ active: expanded.has(`risk-${i}`) }"
            @click="toggle(`risk-${i}`)"
          >
            <div class="item-row">
              <span class="dot" :style="{ backgroundColor: item.color }"></span>
              <span class="item-label">{{ item.label }}</span>
              <span class="chevron">{{ expanded.has(`risk-${i}`) ? '▲' : '▼' }}</span>
            </div>
            <Transition name="expand">
              <div v-if="expanded.has(`risk-${i}`)" class="item-desc">{{ item.desc }}</div>
            </Transition>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.guide {
  padding: 1.25rem 1.5rem;
  background-color: var(--color-bg-subtle);
  border-radius: var(--radius-card);
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.guide-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-text);
}

.columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 640px) {
  .columns {
    grid-template-columns: 1fr;
  }
}

.column {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.col-header {
  font-size: 0.9rem;
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
  gap: 0.4rem;
}

.item {
  background-color: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  padding: 0.6rem 0.85rem;
  cursor: pointer;
  transition:
    border-color 0.15s ease,
    box-shadow 0.15s ease;
  user-select: none;
}

.item:hover {
  border-color: var(--color-primary);
}

.item.active {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(13, 58, 143, 0.08);
}

.item-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.item-label {
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--color-text);
  flex: 1;
}

.chevron {
  font-size: 0.65rem;
  color: var(--color-text-muted);
}

.item-desc {
  font-size: 0.88rem;
  color: var(--color-text-muted);
  line-height: 1.6;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid var(--color-border);
}

/* Expand transition */
.expand-enter-active,
.expand-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
