<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  suburbs: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['select'])

const query = ref('')
const isOpen = ref(false)

const results = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return []
  return props.suburbs.filter((s) => s.suburb_name.toLowerCase().includes(q)).slice(0, 8)
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
    <!-- SVG search icon -->
    <span class="search-icon" aria-hidden="true">
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
    </span>

    <input
      type="text"
      class="search-input"
      placeholder="Search suburbs (e.g. Carlton, Richmond...)"
      v-model="query"
      @input="onInput"
      @blur="onBlur"
      @focus="onInput"
      aria-label="Search suburbs"
      autocomplete="off"
    />

    <button v-if="query" class="clear-btn" @mousedown.prevent="clear" aria-label="Clear search">
      <svg
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        stroke-linecap="round"
      >
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      </svg>
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
        <span class="item-meta"
          >Feels like {{ Math.round(suburb.apparent_temperature ?? suburb.temperature) }}°C ·
          {{ suburb.risk_level.charAt(0).toUpperCase() + suburb.risk_level.slice(1) }} risk</span
        >
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
  left: 1rem;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  pointer-events: none;
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 0.95rem 3rem 0.95rem 3rem;
  border-radius: var(--radius-card);
  border: 1.5px solid var(--color-border);
  background-color: var(--color-white);
  font-size: 1.05rem;
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
  font-size: 1rem;
}

.clear-btn {
  position: absolute;
  right: 0.75rem;
  background: var(--color-bg-light, #f1f5f9);
  border: 1px solid var(--color-border);
  border-radius: 50%;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
  flex-shrink: 0;
}

.clear-btn:hover {
  background-color: #e2e8f0;
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
  padding: 1rem 1.25rem;
  font-size: 0.95rem;
  color: var(--color-text-muted);
}

.dropdown-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.dropdown-item:hover {
  background-color: var(--color-bg-light);
}

.item-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text);
}

.item-meta {
  font-size: 0.875rem;
  color: var(--color-text-muted);
}

.dropdown-item.high {
  border-left: 3px solid #ef4444;
}
.dropdown-item.moderate {
  border-left: 3px solid #f97316;
}
.dropdown-item.low {
  border-left: 3px solid #22c55e;
}
</style>
