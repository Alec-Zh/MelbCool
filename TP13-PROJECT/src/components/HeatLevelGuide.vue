<script setup>
const riskLevels = [
  { color: '#c0392b', label: 'High Risk',     desc: 'High heat and very little tree shade in this area.' },
  { color: '#e8903a', label: 'Moderate Risk', desc: 'Moderate heat or limited tree shade in this area.' },
  { color: '#4d9e5a', label: 'Low Risk',      desc: 'Cooler conditions and good tree shade in this area.' },
]
</script>

<template>
  <div class="guide">
    <p class="guide-title">Map Legend</p>

    <!-- How to use -->
    <div class="section">
      <div class="section-header">How to use this map</div>
      <ul class="how-to-list">
        <li>Your location appears as a <strong>green dot</strong> on the map</li>
        <li><strong>Tap any suburb</strong> to see its heat details</li>
        <li><strong>Tap again</strong> to return to the full map</li>
        <li>Use the <strong>search bar</strong> to find a suburb</li>
        <li>Press <strong>✕</strong> on the detail panel to go back</li>
      </ul>
    </div>

    <!-- Risk Level -->
    <div class="section">
      <div class="section-header">Risk Level</div>
      <ul class="item-list">
        <li v-for="item in riskLevels" :key="item.label" class="item">
          <span class="dot" :style="{ backgroundColor: item.color }"></span>
          <div class="item-text">
            <span class="item-label">{{ item.label }}</span>
            <span class="item-desc">{{ item.desc }}</span>
          </div>
        </li>
      </ul>
    </div>

    <!-- How scores work -->
    <div class="section">
      <div class="section-header">How scores work</div>
      <div class="score-list">
        <div class="score-item">
          <span class="score-label">Heat Score</span>
          <span class="score-desc">How hot it feels today, including UV exposure</span>
        </div>
        <div class="score-item">
          <span class="score-label">Shade Score</span>
          <span class="score-desc">How much tree shade is available in the area</span>
        </div>
        <div class="score-formula">
          Overall risk = Heat Score × 70% + Shade Score × 30%
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.guide {
  padding: 1.25rem;
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #d8eae6;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
  box-sizing: border-box;
}

.guide-title {
  font-size: 0.7rem;
  font-weight: 700;
  color: #2d7a3a;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.section-header {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1c2e2a;
  padding-bottom: 0.35rem;
  border-bottom: 1px solid #e8f0ee;
}

/* How to list — plain bullets */
.how-to-list {
  list-style: disc;
  padding-left: 1.1rem;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.how-to-list li {
  font-size: 0.88rem;
  color: #5a6e6a;
  line-height: 1.5;
  padding-left: 0.2rem;
}

.how-to-list li strong {
  color: #1c2e2a;
  font-weight: 600;
}

/* Risk items */
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
  align-items: flex-start;
  gap: 0.65rem;
  padding: 0.55rem 0.75rem;
  background: #f8faf9;
  border-radius: 8px;
  border: 1px solid #e8f0ee;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 3px;
}

.item-text {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.item-label {
  font-size: 0.88rem;
  font-weight: 600;
  color: #1c2e2a;
}

.item-desc {
  font-size: 0.82rem;
  color: #7a9490;
  line-height: 1.4;
}

/* Scores */
.score-list {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.score-item {
  display: flex;
  flex-direction: column;
  gap: 0.05rem;
}

.score-label {
  font-size: 0.88rem;
  font-weight: 600;
  color: #1c2e2a;
}

.score-desc {
  font-size: 0.82rem;
  color: #7a9490;
  line-height: 1.4;
}

.score-formula {
  margin-top: 0.2rem;
  padding-top: 0.45rem;
  border-top: 1px solid #e8f0ee;
  font-size: 0.8rem;
  color: #2d7a3a;
  font-style: italic;
}
</style>