<script setup>
defineProps({
  item: { type: Object, required: true },
  selected: { type: Boolean, default: false },
})

defineEmits(['toggle'])
</script>

<template>
  <button
    class="citem"
    :class="{
      'citem--good': selected && item.category === 'good',
      'citem--bad': selected && item.category === 'bad',
      'citem--warn': !selected && item.category === 'bad',
    }"
    @click="$emit('toggle', item.id)"
    :aria-pressed="selected"
  >
    <!-- Icon -->
    <span class="ci-ico" aria-hidden="true">{{ item.icon }}</span>

    <!-- Info -->
    <div class="ci-inf">
      <div class="ci-name">
        {{ item.name }}
        <!-- Warning indicator for bad items (AC 4.3.2) -->
        <span v-if="item.category === 'bad'" class="warn-icon" aria-label="Unsafe item">⚠</span>
      </div>
      <div class="ci-eff">{{ item.effect }}</div>
      <!-- Explanation for bad items (AC 4.3.3) -->
      <div v-if="item.category === 'bad' && item.explanation" class="ci-explain">
        {{ item.explanation }}
      </div>
    </div>

    <!-- Selection indicator -->
    <span class="ci-check" aria-hidden="true">
      <svg
        v-if="selected && item.category === 'good'"
        width="12"
        height="12"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="3"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <polyline points="20 6 9 17 4 12" />
      </svg>
      <svg
        v-else-if="selected && item.category === 'bad'"
        width="12"
        height="12"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="3"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      </svg>
    </span>
  </button>
</template>

<style scoped>
.citem {
  width: 100%;
  background: #ffffff;
  border: 1px solid #d8eae6;
  border-radius: 10px;
  padding: 8px 10px;
  cursor: pointer;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  transition:
    border-color 0.15s,
    background-color 0.15s;
  text-align: left;
  font-family: inherit;
}

.citem:hover {
  border-color: #4d9e5a;
  background: #f4faf8;
}

/* Selected good item — green */
.citem--good {
  border-color: #4d9e5a;
  background: #f4faf8;
}

/* Selected bad item — red */
.citem--bad {
  border-color: #c0392b;
  background: #fce8e6;
}

/* Unselected bad item — subtle warm border */
.citem--warn {
  border-color: #f5a78a;
}

.citem--warn:hover {
  border-color: #c0392b;
  background: #fce8e6;
}

.ci-ico {
  font-size: 18px;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
  margin-top: 1px;
}

.ci-inf {
  flex: 1;
  min-width: 0;
}

.ci-name {
  font-size: 12px;
  font-weight: 600;
  color: #1a1714;
  line-height: 1.2;
  display: flex;
  align-items: center;
  gap: 5px;
}

.warn-icon {
  font-size: 11px;
  color: #c0392b;
  flex-shrink: 0;
}

.ci-eff {
  font-size: 11px;
  color: #9e9890;
  margin-top: 1px;
  line-height: 1.4;
}

.citem--good .ci-eff {
  color: #2d7a3a;
}

.citem--bad .ci-eff {
  color: #8b1a12;
}

/* AC 4.3.3 — explanation text for bad items */
.ci-explain {
  font-size: 11px;
  color: #c0392b;
  margin-top: 3px;
  font-style: italic;
  line-height: 1.4;
}

/* Selection check circle */
.ci-check {
  width: 18px;
  height: 18px;
  border: 1.5px solid #d8eae6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
  transition: all 0.15s;
}

.citem--good .ci-check {
  background: #4d9e5a;
  border-color: #4d9e5a;
  color: #ffffff;
}

.citem--bad .ci-check {
  background: #c0392b;
  border-color: #c0392b;
  color: #ffffff;
}
</style>
