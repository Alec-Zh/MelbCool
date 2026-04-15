<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  suburbs: {
    type: Array,
    default: () => [], // full list of suburb objects passed from parent
  },
})

const emit = defineEmits(['select'])

const query = ref('')
const isOpen = ref(false)

const results = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return []
  return props.suburbs
    .filter((s) => s.suburb_name.toLowerCase().includes(q))
    .slice(0, 8) // cap dropdown at 8 items
})

function select(suburb) {
  query.value = suburb.suburb_name
  isOpen.value = false
  emit('select', suburb)
}

function onInput() {
  isOpen.value = true
}

function onBlur() {
  // Delay close so click on dropdown item registers first
  setTimeout(() => {
    isOpen.value = false
  }, 150)
}

function clear() {
  query.value = ''
  isOpen.value = false
  emit('select', null)
}
</script>

<template>
  <div class="search-wrap">
    <span class="search-icon">🔍</span>
    <input
      type="text"
      class="search-input"
      placeholder="Search suburbs..."
      v-model="query"
      @input="onInput"
      @blur="onBlur"
      @focus="onInput"
      aria-label="Search suburbs"
      autocomplete="off"
    />
    <button v-if="query" class="clear-btn" @mousedown.prevent="clear" aria-label="Clear search">
      ✕
    </button>

    <ul v-if="isOpen && query.trim()" class="dropdown" role="listbox">
      <li v-if="results.length === 0" class="dropdown-empty">
        No results in Inner Melbourne — please try a different suburb name.
      </li>
      <li
        v-for="suburb in results"
        :key="suburb.suburb_name"
        class="dropdown-item"
        :class="suburb.risk_level"
        role="option"
        @mousedown.prevent="select(suburb)"
      >
        <span class="item-name">{{ suburb.suburb_name }}</span>
        <span class="item-meta">{{ suburb.temperature }}°C · {{ suburb.risk_level }} risk</span>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.search-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.9rem;
  font-size: 1rem;
  pointer-events: none;
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 0.85rem 2.5rem 0.85rem 2.5rem;
  border-radius: var(--radius-card);
  border: 1.5px solid var(--color-border);
  background-color: var(--color-white);
  font-size: 1rem;
  color: var(--color-text);
  outline: none;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(13, 58, 143, 0.1);
}

.search-input::placeholder {
  color: var(--color-text-muted);
}

.clear-btn {
  position: absolute;
  right: 0.9rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.85rem;
  color: var(--color-text-muted);
  padding: 0.2rem 0.4rem;
  border-radius: 50%;
  line-height: 1;
  transition: color 0.15s ease;
}

.clear-btn:hover {
  color: var(--color-text);
}

.dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  background-color: var(--color-white);
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  list-style: none;
  margin: 0;
  padding: 0.25rem 0;
  z-index: 1001;
  overflow: hidden;
}

.dropdown-empty {
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
  color: var(--color-text-muted);
  font-style: italic;
}

.dropdown-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.65rem 1rem;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.dropdown-item:hover {
  background-color: var(--color-bg-light);
}

.item-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-text);
}

.item-meta {
  font-size: 0.8rem;
  color: var(--color-text-muted);
}

/* Risk level accent on the left edge */
.dropdown-item.high     { border-left: 3px solid #EF4444; }
.dropdown-item.moderate { border-left: 3px solid #F97316; }
.dropdown-item.low      { border-left: 3px solid #22C55E; }
</style>