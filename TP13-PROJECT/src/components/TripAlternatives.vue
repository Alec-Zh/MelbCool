<script setup>
defineProps({
  alternatives: { type: Array, required: true },
  baseScore: { type: Number, required: true },
})

const emit = defineEmits(['select-alt'])

function pctLabel(pct) {
  return pct < 0 ? `↓ ${Math.abs(pct)}% safer` : `↑ ${Math.abs(pct)}% riskier`
}
function pctClass(pct) {
  return pct < 0 ? 'safer' : 'worse'
}

function miniWidths(legs) {
  const total = legs.reduce((s, l) => s + l.score, 0) || 1
  return legs.map((l) => Math.round((l.score / total) * 100))
}
</script>

<template>
  <div class="section">
    <h2 class="section-title">Could you make this trip safer?</h2>
    <p class="subtitle">Here are some options that would lower your heat exposure.</p>

    <div class="alt-list">
      <div
        v-for="(alt, i) in alternatives"
        :key="i"
        class="alt-card"
        :style="{ borderLeft: `4px solid ${alt.riskColor}` }"
      >
        <div class="alt-header">
          <div class="alt-rank">#{{ i + 1 }}</div>
          <div class="alt-title">{{ alt.title }}</div>
          <div class="pct-pill" :class="pctClass(alt.pctChange)">
            {{ pctLabel(alt.pctChange) }}
          </div>
        </div>

        <div class="alt-score-row">
          <span class="alt-score" :style="{ color: alt.riskColor }">
            {{ alt.score }}<span class="out-of"> / 100</span>
          </span>
          <span class="alt-badge" :style="{ background: alt.riskColor }"
            >{{ alt.riskLabel }} Risk</span
          >
        </div>

        <div class="mini-bar">
          <div
            v-for="(leg, j) in alt.legs"
            :key="j"
            class="mini-seg"
            :style="{ width: miniWidths(alt.legs)[j] + '%', background: leg.color }"
            :title="`${leg.label}: ${leg.score}`"
          />
        </div>

        <p class="alt-explanation">{{ alt.explanation }}</p>

        <button class="alt-action" @click="emit('select-alt', alt.params)">
          {{ alt.action }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.section-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 0.2rem;
}
.subtitle {
  font-size: 0.88rem;
  color: #888;
  margin: 0;
}
.alt-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.alt-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.alt-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.alt-rank {
  font-size: 0.78rem;
  font-weight: 700;
  color: #888;
  background: #f0f0f0;
  border-radius: 20px;
  padding: 0.15rem 0.5rem;
}
.alt-title {
  font-weight: 700;
  font-size: 0.95rem;
  color: #1a1a1a;
  flex: 1;
}
.pct-pill {
  font-size: 0.82rem;
  font-weight: 700;
  padding: 0.2rem 0.65rem;
  border-radius: 20px;
  white-space: nowrap;
}
.pct-pill.safer {
  background: #eef6f1;
  color: #4a7c59;
}
.pct-pill.worse {
  background: #fdecea;
  color: #d9534f;
}

.alt-score-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.alt-score {
  font-size: 1.9rem;
  font-weight: 800;
  line-height: 1;
}
.out-of {
  font-size: 0.9rem;
  font-weight: 500;
  color: #888;
}
.alt-badge {
  color: #fff;
  font-size: 0.82rem;
  font-weight: 700;
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
}
.mini-bar {
  display: flex;
  height: 10px;
  border-radius: 5px;
  overflow: hidden;
  gap: 2px;
}
.mini-seg {
  border-radius: 3px;
  transition: width 0.4s ease;
}

.alt-explanation {
  font-size: 0.9rem;
  color: #444;
  line-height: 1.6;
  margin: 0;
}
.alt-action {
  align-self: flex-start;
  background: none;
  border: 2px solid var(--color-primary, #1a6eb5);
  color: var(--color-primary, #1a6eb5);
  border-radius: 8px;
  padding: 0.5rem 1.1rem;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition:
    background 0.2s,
    color 0.2s;
}
.alt-action:hover {
  background: var(--color-primary, #1a6eb5);
  color: #fff;
}
</style>
