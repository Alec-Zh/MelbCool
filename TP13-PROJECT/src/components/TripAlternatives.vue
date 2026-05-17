<script setup>
import { ref } from 'vue'

defineProps({
  alternatives: { type: Array, required: true },
  baseScore: { type: Number, required: true },
})

const emit = defineEmits(['select-alt'])

const expanded = ref(null)

function toggle(i) {
  expanded.value = expanded.value === i ? null : i
}

function pctLabel(pct) {
  return pct < 0 ? `${Math.abs(pct)}% safer` : `${Math.abs(pct)}% riskier`
}
</script>

<template>
  <div class="alts-section card">
    <p class="alts-heading">💡 Could this trip be safer?</p>

    <div class="alt-pills">
      <button
        v-for="(alt, i) in alternatives"
        :key="i"
        class="alt-pill"
        :class="{ active: expanded === i, safer: alt.pctChange < 0, riskier: alt.pctChange >= 0 }"
        @click="toggle(i)"
      >
        <span class="pill-title">{{ alt.title }}</span>
        <span class="pill-badge" :class="alt.pctChange < 0 ? 'badge-safer' : 'badge-riskier'">{{
          pctLabel(alt.pctChange)
        }}</span>
      </button>
    </div>

    <transition name="expand">
      <div v-if="expanded !== null" class="alt-detail">
        <p class="alt-detail-text">{{ alternatives[expanded].explanation }}</p>
        <div class="alt-detail-footer">
          <span class="alt-detail-score" :style="{ color: alternatives[expanded].riskColor }">
            Score {{ alternatives[expanded].score }}/100 ·
            <strong>{{ alternatives[expanded].riskLabel }} Risk</strong>
          </span>
          <button class="alt-action" @click="emit('select-alt', alternatives[expanded].params)">
            {{ alternatives[expanded].action }} →
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.alts-section {
  padding: 1.1rem 1.25rem;
}
.alts-heading {
  font-size: 0.82rem;
  font-weight: 700;
  color: #5a6e6a;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  margin: 0 0 0.75rem;
}
.alt-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.alt-pill {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.3rem;
  padding: 0.65rem 1rem;
  border-radius: 12px;
  border: 2px solid #ddd;
  background: #fff;
  cursor: pointer;
  font-family: inherit;
  transition:
    border-color 0.15s,
    background 0.15s;
  text-align: left;
}
.alt-pill:hover,
.alt-pill.active {
  border-color: #2d7a3a;
  background: #f5fdf6;
}
.alt-pill.active {
  box-shadow: 0 0 0 3px rgba(45, 122, 58, 0.15);
}

.pill-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1c2e2a;
}

.pill-badge {
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.15rem 0.55rem;
  border-radius: 20px;
}
.badge-safer {
  background: #eef6f1;
  color: #2d7a3a;
}
.badge-riskier {
  background: #f5f5f5;
  color: #888;
}
.alt-detail {
  margin-top: 0.85rem;
  padding-top: 0.85rem;
  border-top: 1px solid #e8f0ee;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.alt-detail-text {
  font-size: 0.9rem;
  color: #3a4e4a;
  line-height: 1.6;
  margin: 0;
}
.alt-detail-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.alt-detail-score {
  font-size: 0.88rem;
}
.alt-action {
  background: none;
  border: 2px solid currentColor;
  border-radius: 8px;
  padding: 0.4rem 0.9rem;
  font-size: 0.88rem;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  color: #2d7a3a;
  transition:
    background 0.15s,
    color 0.15s;
}
.alt-action:hover {
  background: #2d7a3a;
  color: #fff;
}
.expand-enter-active,
.expand-leave-active {
  transition:
    opacity 0.2s,
    transform 0.2s;
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
