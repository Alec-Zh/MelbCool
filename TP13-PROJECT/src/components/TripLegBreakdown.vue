<script setup>
import { computed } from 'vue'

const props = defineProps({
  legs: { type: Array, required: true },
})

const segWidths = computed(() => {
  const total = props.legs.reduce((s, l) => s + l.score, 0) || 1
  return props.legs.map((l) => Math.round((l.score / total) * 100))
})
</script>

<template>
  <div class="card">
    <h2 class="section-title">Heat exposure at each stage</h2>
    <p class="subtitle">Each part of your trip is scored separately.</p>

    <div class="seg-bar">
      <div
        v-for="(leg, i) in legs"
        :key="i"
        class="seg"
        :style="{ width: segWidths[i] + '%', background: leg.color }"
        :title="`${leg.label}: ${leg.score}`"
      />
    </div>

    <div class="leg-list">
      <div v-for="(leg, i) in legs" :key="i" class="leg-item">
        <span class="leg-dot" :style="{ background: leg.color }" />
        <span class="leg-label">{{ leg.label }}</span>
        <span class="leg-mins">{{ leg.minutes }} min</span>
        <span class="leg-score" :style="{ color: leg.color }">
          Score {{ leg.score }} — {{ leg.riskLabel }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
}
.section-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 0.25rem;
}
.subtitle {
  font-size: 0.88rem;
  color: #888;
  margin: 0 0 1.1rem;
}
.seg-bar {
  display: flex;
  height: 16px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1rem;
  gap: 2px;
}
.seg {
  border-radius: 4px;
  transition: width 0.4s ease;
}
.leg-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}
.leg-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.92rem;
}
.leg-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}
.leg-label {
  font-weight: 600;
  min-width: 110px;
  color: #222;
}
.leg-mins {
  color: #888;
  min-width: 48px;
  font-size: 0.85rem;
}
.leg-score {
  font-weight: 600;
}
</style>
