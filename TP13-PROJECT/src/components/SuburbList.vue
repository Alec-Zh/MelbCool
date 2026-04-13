<script setup>
import { computed } from 'vue'
import SuburbCard from './SuburbCard.vue'

const props = defineProps({
  suburbs: { type: Array, default: () => [] }, // 全部53个Inner Melbourne区
  selectedSuburb: { type: Object, default: null },
  search: { type: String, default: '' },
})

const emit = defineEmits(['select'])

// 默认：最高风险3 + 最低风险3
const defaultCards = computed(() => {
  const high3 = [...props.suburbs]
    .filter((s) => s.risk_level === 'high')
    .sort((a, b) => b.temperature - a.temperature || a.suburb_name.localeCompare(b.suburb_name))
    .slice(0, 3)
  const low3 = [...props.suburbs]
    .filter((s) => s.risk_level === 'low')
    .sort((a, b) => a.temperature - b.temperature || a.suburb_name.localeCompare(b.suburb_name))
    .slice(0, 3)
  return [...high3, ...low3]
})

// 搜索结果
const searchResults = computed(() =>
  props.suburbs.filter((s) => s.suburb_name.toLowerCase().includes(props.search.toLowerCase())),
)

// 显示的卡片
const displayedCards = computed(() => {
  if (props.search.trim()) return searchResults.value
  if (props.selectedSuburb) {
    const inDefault = defaultCards.value.some(
      (s) => s.suburb_name === props.selectedSuburb.suburb_name,
    )
    return inDefault ? defaultCards.value : [...defaultCards.value, props.selectedSuburb]
  }
  return defaultCards.value
})

const listLabel = computed(() => {
  if (props.search.trim())
    return `${searchResults.value.length} result${searchResults.value.length !== 1 ? 's' : ''} in Inner Melbourne`
  return 'Showing highest & lowest risk areas'
})
</script>

<template>
  <div class="suburb-list-wrap">
    <div class="list-header">
      <span class="list-label">{{ listLabel }}</span>
    </div>

    <div class="suburb-list">
      <SuburbCard
        v-for="suburb in displayedCards"
        :key="suburb.suburb_name"
        :suburb="suburb"
        :selected="selectedSuburb?.suburb_name === suburb.suburb_name"
        @select="emit('select', $event)"
      />
      <p v-if="displayedCards.length === 0" class="no-results">No suburbs found.</p>
    </div>
  </div>
</template>

<style scoped>
.suburb-list-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.list-header {
  display: flex;
  align-items: center;
}

.list-label {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  font-weight: 500;
}

.suburb-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.no-results {
  color: var(--color-text-muted);
  font-size: 0.95rem;
  grid-column: 1 / -1;
  text-align: center;
  padding: 2rem 0;
}
</style>
