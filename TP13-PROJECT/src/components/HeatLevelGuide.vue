<template>
  <div class="guide">
    <h3 class="guide-title">Heat Level Guide</h3>
    <ul class="guide-list">
      <li v-for="item in levels" :key="item.level" class="guide-item">
        <span class="dot" :style="{ backgroundColor: item.color }"></span>
        <div>
          <span class="guide-label">{{ item.label }}:</span>
          <span class="guide-desc"> {{ item.desc }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
const levels = [
  {
    level: 'higher',
    color: '#EF4444',
    label: 'Higher Heat',
    desc: 'Warmer temps, less tree cover, more elderly residents',
  },
  {
    level: 'moderate',
    color: '#F97316',
    label: 'Moderate Heat',
    desc: 'Average conditions, some cooling factors',
  },
  {
    level: 'lower',
    color: '#22C55E',
    label: 'Lower Heat',
    desc: 'Cooler temps, better tree cover, coastal areas',
  },
]
</script>

<style scoped>
.guide {
  padding: 1rem 1.25rem;
  border-top: 1px solid var(--color-border);
  background-color: var(--color-bg-subtle);
  border-radius: 0 0 var(--radius-card) var(--radius-card);
}

.guide-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.75rem;
}

.guide-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.guide-item {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  font-size: 0.85rem;
  color: var(--color-text);
  line-height: 1.4;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 3px;
}

.guide-label {
  font-weight: 600;
}

.guide-desc {
  color: var(--color-text-muted);
}
</style>
