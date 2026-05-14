<script setup>
defineProps({
  legs: { type: Array, required: true },
  transportMode: { type: String, default: 'walk' },
})
</script>

<template>
  <div class="card">
    <h2 class="section-title">Time outdoors vs sheltered</h2>
    <p class="subtitle">Heat exposure depends on how much of your trip is spent outside.</p>

    <div class="leg-list">
      <div v-for="(leg, i) in legs" :key="i" class="leg-item">
        <div class="leg-left">
          <span class="leg-dot" :style="{ background: leg.color }" />
          <div class="leg-text">
            <span class="leg-label">{{ leg.label }}</span>
            <span class="leg-mins">{{ leg.minutes }} min</span>
          </div>
        </div>
        <div class="seg-group">
          <div class="seg" :class="{ active: leg.riskLabel === 'Low' }" style="--c: #4d9e5a">
            Low
          </div>
          <div class="seg" :class="{ active: leg.riskLabel === 'Moderate' }" style="--c: #e8903a">
            Moderate
          </div>
          <div
            class="seg"
            :class="{ active: leg.riskLabel === 'High' || leg.riskLabel === 'Very High' }"
            style="--c: #c0392b"
          >
            High
          </div>
        </div>
      </div>
    </div>

    <p class="source-note">
      Outdoor exposure estimated from transport type. Walk = 100% outdoor; Tram/Bus ≈ 25% outdoor
      (Currie &amp; Delbosc, 2011); Drive ≈ 10% outdoor (AustRoads parking walk estimate).
    </p>
  </div>
</template>

<style scoped>
.card {
  background: #fff;
  border-radius: 14px;
  padding: 1.5rem;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    0 8px 24px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.05);
}
.section-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1c2e2a;
  margin: 0 0 0.25rem;
}
.subtitle {
  font-size: 0.85rem;
  color: #7a9490;
  margin: 0 0 1.1rem;
  line-height: 1.5;
}
.leg-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.leg-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
.leg-left {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  min-width: 160px;
}
.leg-dot {
  width: 11px;
  height: 11px;
  border-radius: 50%;
  flex-shrink: 0;
}
.leg-text {
  display: flex;
  flex-direction: column;
  gap: 0.05rem;
}
.leg-label {
  font-size: 0.88rem;
  font-weight: 600;
  color: #1c2e2a;
}
.leg-mins {
  font-size: 0.78rem;
  color: #7a9490;
}
.seg-group {
  display: flex;
  gap: 0.25rem;
  flex: 1;
  max-width: 200px;
}
.seg {
  flex: 1;
  padding: 0.25rem 0;
  text-align: center;
  font-size: 0.72rem;
  font-weight: 600;
  border-radius: 5px;
  background: #f0f0f0;
  color: #bbb;
  transition:
    background 0.2s,
    color 0.2s;
}
.seg.active {
  background: var(--c);
  color: #fff;
}
.source-note {
  margin: 1rem 0 0;
  padding-top: 0.75rem;
  border-top: 1px solid #e8f0ee;
  font-size: 0.75rem;
  color: #5a6e6a;
  line-height: 1.55;
}
</style>
