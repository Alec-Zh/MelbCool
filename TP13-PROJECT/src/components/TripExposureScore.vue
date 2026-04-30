<script setup>
defineProps({
  score: { type: Number, required: true },
  riskLabel: { type: String, required: true },
  riskColor: { type: String, required: true },
  riskBg: { type: String, required: true },
})
</script>

<template>
  <div class="card" :style="{ borderLeft: `5px solid ${riskColor}`, background: riskBg }">
    <div class="row">
      <div>
        <p class="label">How risky is this trip?</p>
        <p class="score" :style="{ color: riskColor }">
          {{ score }}<span class="out-of"> / 100</span>
        </p>
      </div>
      <div class="badge-wrap">
        <div class="badge" :style="{ background: riskColor }">{{ riskLabel }} Risk</div>
        <p class="hint">Higher score = more heat exposure</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
}
.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}
.label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #555;
  margin: 0 0 0.25rem;
}
.score {
  font-size: 3.2rem;
  font-weight: 800;
  margin: 0;
  line-height: 1;
}
.out-of {
  font-size: 1.1rem;
  font-weight: 500;
  color: #888;
}
.badge-wrap {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.4rem;
}
.badge {
  color: #fff;
  font-weight: 700;
  font-size: 0.95rem;
  padding: 0.5rem 1.1rem;
  border-radius: 30px;
}
.hint {
  font-size: 0.78rem;
  color: #888;
  margin: 0;
  text-align: right;
}
</style>
