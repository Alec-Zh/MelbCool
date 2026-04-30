<script setup>
defineProps({
  suburbName: { type: String, required: true },
  forecastTemp: { type: Number, required: true },
  treeCanopy: { type: Number, default: null },
  departureLabel: { type: String, required: true },
  transportMode: { type: String, required: true },
  durationMins: { type: Number, required: true },
})

const transportLabel = {
  walk: '🚶 Walking',
  tram: '🚃 Tram',
  bus: '🚌 Bus',
  drive: '🚗 Driving',
}
</script>

<template>
  <div class="card">
    <p class="card-heading">Your trip at a glance</p>
    <div class="row">
      <div class="item">
        <span class="label">Going to</span>
        <span class="value">{{ suburbName }}</span>
      </div>
      <div class="item">
        <span class="label">Feels like outside at {{ departureLabel }}</span>
        <span class="value temp">{{ forecastTemp }}°C</span>
      </div>
      <div class="item">
        <span class="label">Tree shade in area</span>
        <span class="value">{{ treeCanopy != null ? treeCanopy + '%' : '—' }}</span>
      </div>
      <div class="item">
        <span class="label">How you're travelling</span>
        <span class="value transport"
          >{{ transportLabel[transportMode] }} · {{ durationMins }} min</span
        >
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  background: #fff;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
}
.card-heading {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #888;
  margin: 0 0 1rem;
}
.row {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 110px;
}
.label {
  font-size: 0.8rem;
  color: #888;
}
.value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a1a1a;
}
.temp {
  font-size: 1.6rem;
}
.transport {
  font-size: 1rem;
}
</style>
