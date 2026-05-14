<script setup>
defineProps({
  suburb: { type: Object, default: null },
})

const uvLabel = (uv) => {
  if (uv >= 11) return 'Extreme'
  if (uv >= 8) return 'Very High'
  if (uv >= 6) return 'High'
  if (uv >= 3) return 'Moderate'
  return 'Low'
}

const riskConfig = {
  high: { label: 'High risk', bg: '#fce8e6', color: '#8b1a12' },
  moderate: { label: 'Moderate risk', bg: '#fef1e0', color: '#7a4510' },
  low: { label: 'Low risk', bg: '#e6f4e8', color: '#1e5c28' },
}
</script>

<template>
  <div class="wcard" v-if="suburb">
    <!-- Temperature block -->
    <div class="temp-block">
      <span class="temp-val">{{ Math.round(suburb.apparent_temperature) }}</span>
      <span class="temp-unit">°C</span>
      <span class="temp-label">Feels like</span>
    </div>

    <div class="wdiv" aria-hidden="true"></div>

    <!-- Detail grid -->
    <div class="wdets">
      <div class="wdet">
        <span class="wdet-lbl">Temperature</span>
        <span class="wdet-val">{{ Math.round(suburb.temperature) }}°C</span>
      </div>
      <div class="wdet">
        <span class="wdet-lbl">UV Index</span>
        <span class="wdet-val"
          >{{ Math.round(suburb.uv_index) }} — {{ uvLabel(suburb.uv_index) }}</span
        >
      </div>
      <div class="wdet">
        <span class="wdet-lbl">Tree coverage</span>
        <span class="wdet-val">{{ Math.round(suburb.tree_canopy_percent) }}%</span>
      </div>
      <div class="wdet">
        <span class="wdet-lbl">Suburb</span>
        <span class="wdet-val wdet-suburb">{{ suburb.suburb_name }}</span>
      </div>
    </div>

    <!-- Risk badge -->
    <span
      v-if="suburb.risk_level"
      class="risk-badge"
      :style="{
        backgroundColor: riskConfig[suburb.risk_level]?.bg,
        color: riskConfig[suburb.risk_level]?.color,
      }"
    >
      {{ riskConfig[suburb.risk_level]?.label }}
    </span>
  </div>

  <!-- Skeleton while loading -->
  <div class="wcard wcard--empty" v-else>
    <span class="empty-msg">Select a suburb above to see current heat conditions.</span>
  </div>
</template>

<style scoped>
.wcard {
  background: #f4faf8;
  border: 1px solid #d8eae6;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.wcard--empty {
  justify-content: center;
  padding: 1.25rem;
}

.empty-msg {
  font-size: 0.88rem;
  color: #9e9890;
}

.temp-block {
  display: flex;
  align-items: baseline;
  gap: 0.1rem;
  flex-wrap: wrap;
  flex-direction: row;
  position: relative;
}

.temp-val {
  font-size: 2.6rem;
  font-weight: 800;
  color: #1a1714;
  letter-spacing: -2px;
  line-height: 1;
}

.temp-unit {
  font-size: 1.2rem;
  font-weight: 400;
  color: #6b6560;
  align-self: flex-start;
  margin-top: 4px;
}

.temp-label {
  position: absolute;
  bottom: -14px;
  left: 0;
  font-size: 10px;
  color: #9e9890;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.wdiv {
  width: 1px;
  background: #d8eae6;
  align-self: stretch;
  flex-shrink: 0;
  min-height: 48px;
}

.wdets {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px 16px;
  min-width: 160px;
}

.wdet {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.wdet-lbl {
  font-size: 10px;
  color: #9e9890;
  line-height: 1;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.wdet-val {
  font-size: 13px;
  font-weight: 700;
  color: #1a1714;
}

.wdet-suburb {
  font-size: 12px;
}

.risk-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 50px;
  white-space: nowrap;
  flex-shrink: 0;
  letter-spacing: 0.03em;
}

@media (max-width: 480px) {
  .wcard {
    gap: 0.75rem;
  }
  .wdiv {
    display: none;
  }
  .wdets {
    min-width: 0;
    width: 100%;
  }
}
</style>
