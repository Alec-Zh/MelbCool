<script setup>
defineProps({
  legs: { type: Array, required: true },
  transportMode: { type: String, default: 'walk' },
})

function riskEmoji(label) {
  if (label === 'Low') return '✅'
  if (label === 'Moderate') return '⚠️'
  return '🔴'
}

function riskColor(label) {
  if (label === 'Low') return '#4d9e5a'
  if (label === 'Moderate') return '#e8903a'
  return '#c0392b'
}

function riskBg(label) {
  if (label === 'Low') return '#eef6f1'
  if (label === 'Moderate') return '#fef3ec'
  return '#fdecea'
}
</script>

<template>
  <div class="card">
    <h2 class="section-title">Where is the heat risk?</h2>
    <p class="subtitle">Your trip is split into time outside and time in a vehicle or shelter.</p>

    <div class="leg-list">
      <div
        v-for="(leg, i) in legs"
        :key="i"
        class="leg-card"
        :style="{
          background: riskBg(leg.riskLabel),
          borderLeft: `4px solid ${riskColor(leg.riskLabel)}`,
        }"
      >
        <div class="leg-top">
          <span class="leg-emoji">{{ leg.isOutdoor ? '☀️' : '🏠' }}</span>
          <div class="leg-info">
            <span class="leg-label">{{ leg.label }}</span>
            <span class="leg-mins">{{ leg.minutes }} minutes</span>
          </div>
          <div class="leg-risk">
            <span class="risk-emoji">{{ riskEmoji(leg.riskLabel) }}</span>
            <span class="risk-text" :style="{ color: riskColor(leg.riskLabel) }">
              {{ leg.riskLabel }} risk
            </span>
          </div>
        </div>
        <div class="leg-bar-wrap">
          <div
            class="leg-bar"
            :style="{ width: Math.min(leg.score, 100) + '%', background: riskColor(leg.riskLabel) }"
          />
        </div>
      </div>
    </div>

    <p class="source-note">
      Outdoor time estimated by transport type. Walking = fully outdoor. Tram/bus ≈ 25% outdoor.
      Driving ≈ 10% outdoor.
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
  font-size: 1.05rem;
  font-weight: 700;
  color: #1c2e2a;
  margin: 0 0 0.25rem;
}
.subtitle {
  font-size: 0.9rem;
  color: #7a9490;
  margin: 0 0 1.1rem;
  line-height: 1.5;
}

.leg-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.leg-card {
  border-radius: 10px;
  padding: 0.9rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.leg-top {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.leg-emoji {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.leg-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.leg-label {
  font-size: 1rem;
  font-weight: 700;
  color: #1c2e2a;
}

.leg-mins {
  font-size: 0.88rem;
  color: #7a9490;
}

.leg-risk {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.1rem;
}

.risk-emoji {
  font-size: 1.2rem;
}

.risk-text {
  font-size: 0.88rem;
  font-weight: 700;
}

.leg-bar-wrap {
  height: 8px;
  background: rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  overflow: hidden;
}

.leg-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.4s ease;
}

.source-note {
  margin: 1rem 0 0;
  padding-top: 0.75rem;
  border-top: 1px solid #e8f0ee;
  font-size: 0.8rem;
  color: #7a9490;
  line-height: 1.55;
}
</style>
