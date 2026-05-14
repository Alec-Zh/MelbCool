<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  suburbs: { type: Array, default: () => [] },
  selectedSuburbId: { type: [Number, String], default: '' },
  transportMode: { type: String, default: 'walk' },
  durationMins: { type: Number, default: 30 },
  departureMinutes: { type: Number, default: 540 },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits([
  'update:selectedSuburbId',
  'update:transportMode',
  'update:durationMins',
  'update:departureMinutes',
  'submit',
])

// ── Searchable suburb dropdown ────────────────────────────────────────────────
const searchQuery = ref('')
const dropdownOpen = ref(false)

const selectedSuburb = computed(
  () => props.suburbs.find((s) => s.suburb_id === props.selectedSuburbId) ?? null,
)

const filteredSuburbs = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return props.suburbs
  return props.suburbs.filter((s) => s.suburb_name.toLowerCase().includes(q)).slice(0, 8)
})

function selectSuburb(suburb) {
  emit('update:selectedSuburbId', suburb.suburb_id)
  searchQuery.value = ''
  dropdownOpen.value = false
}

function onBlur() {
  setTimeout(() => {
    dropdownOpen.value = false
  }, 150)
}

function clearSuburb() {
  emit('update:selectedSuburbId', '')
  searchQuery.value = ''
  dropdownOpen.value = false
}

// ── Transport options ─────────────────────────────────────────────────────────
const transportOptions = [
  { value: 'walk', label: 'Walk', icon: '🚶' },
  { value: 'tram', label: 'Tram', icon: '🚃' },
  { value: 'bus', label: 'Bus', icon: '🚌' },
  { value: 'drive', label: 'Drive', icon: '🚗' },
]

// ── Duration options ──────────────────────────────────────────────────────────
const durationOptions = [15, 30, 45, 60]

// ── Time slider ───────────────────────────────────────────────────────────────
const sliderMin = 540
const sliderMax = 1200
const sliderStep = 10

function minutesToLabel(mins) {
  const h = Math.floor(mins / 60)
  const m = mins % 60
  const period = h >= 12 ? 'pm' : 'am'
  const displayH = h > 12 ? h - 12 : h === 0 ? 12 : h
  return m === 0
    ? `${displayH}:00 ${period}`
    : `${displayH}:${String(m).padStart(2, '0')} ${period}`
}

const departureLabel = computed(() => minutesToLabel(props.departureMinutes))
const sliderFill = computed(
  () => ((props.departureMinutes - sliderMin) / (sliderMax - sliderMin)) * 100,
)

const sliderTicks = [
  { mins: 540, label: '9am' },
  { mins: 660, label: '11am' },
  { mins: 780, label: '1pm' },
  { mins: 900, label: '3pm' },
  { mins: 1020, label: '5pm' },
  { mins: 1140, label: '7pm' },
  { mins: 1200, label: '8pm' },
]

const isFormValid = computed(() => !!props.selectedSuburbId && !!props.transportMode)
</script>

<template>
  <div class="card">
    <h2 class="section-title">Plan your trip</h2>

    <!-- Destination -->
    <div class="field">
      <label class="field-label">Where are you going?</label>
      <div class="search-wrap" @blur.capture="onBlur">
        <div
          v-if="selectedSuburb && !dropdownOpen"
          class="selected-display"
          @click="dropdownOpen = true"
        >
          <span class="selected-name">{{ selectedSuburb.suburb_name }}</span>
          <button class="clear-btn" @click.stop="clearSuburb" aria-label="Clear selection">
            <svg
              width="14"
              height="14"
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
        </div>
        <div v-else class="input-wrap">
          <svg
            class="search-icon"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
          >
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <input
            class="search-input"
            type="text"
            :placeholder="loading ? 'Loading…' : 'Type a suburb name…'"
            v-model="searchQuery"
            @focus="dropdownOpen = true"
            autocomplete="off"
          />
        </div>
        <ul v-if="dropdownOpen" class="dropdown" role="listbox">
          <li v-if="filteredSuburbs.length === 0" class="dropdown-empty">No suburbs found</li>
          <li
            v-for="s in filteredSuburbs"
            :key="s.suburb_id"
            class="dropdown-item"
            role="option"
            @mousedown.prevent="selectSuburb(s)"
          >
            {{ s.suburb_name }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Transport mode -->
    <div class="field">
      <span class="field-label">How are you getting there?</span>
      <div class="toggle-group">
        <button
          v-for="opt in transportOptions"
          :key="opt.value"
          type="button"
          class="toggle-btn"
          :class="{ active: transportMode === opt.value }"
          @click="emit('update:transportMode', opt.value)"
        >
          <span class="toggle-icon">{{ opt.icon }}</span>
          <span class="toggle-label">{{ opt.label }}</span>
        </button>
      </div>
    </div>

    <!-- Duration -->
    <div class="field">
      <span class="field-label">How long will the trip take?</span>
      <div class="toggle-group">
        <button
          v-for="d in durationOptions"
          :key="d"
          type="button"
          class="toggle-btn toggle-btn--dur"
          :class="{ active: durationMins === d }"
          @click="emit('update:durationMins', d)"
        >
          {{ d }} min
        </button>
      </div>
    </div>

    <!-- Departure time -->
    <div class="field">
      <label class="field-label">
        What time are you leaving?
        <span class="time-badge">{{ departureLabel }}</span>
      </label>
      <div class="slider-wrap">
        <input
          type="range"
          class="slider"
          :min="sliderMin"
          :max="sliderMax"
          :step="sliderStep"
          :value="departureMinutes"
          :style="{ '--fill': sliderFill + '%' }"
          @input="emit('update:departureMinutes', Number($event.target.value))"
        />
        <div class="slider-ticks">
          <span
            v-for="tick in sliderTicks"
            :key="tick.mins"
            :style="{ left: ((tick.mins - sliderMin) / (sliderMax - sliderMin)) * 100 + '%' }"
            >{{ tick.label }}</span
          >
        </div>
      </div>
    </div>

    <!-- Submit -->
    <button class="submit-btn" :disabled="!isFormValid" @click="emit('submit')">
      Check my trip risk →
    </button>
  </div>
</template>

<style scoped>
.card {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
}
.section-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--color-text, #1a1a1a);
  margin: 0 0 1.5rem;
}
.field {
  margin-bottom: 1.5rem;
}
.field:last-child {
  margin-bottom: 0;
}
.field-label {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.65rem;
  flex-wrap: wrap;
}

/* Searchable dropdown */
.search-wrap {
  position: relative;
}
.selected-display {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border: 2px solid var(--color-primary, #1a6eb5);
  border-radius: 8px;
  cursor: pointer;
  background: #fff;
}
.selected-name {
  font-weight: 600;
  font-size: 0.95rem;
  color: #1a1a1a;
}
.clear-btn {
  background: #f0f0f0;
  border: none;
  border-radius: 50%;
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #666;
  flex-shrink: 0;
}
.clear-btn:hover {
  background: #e0e0e0;
}
.input-wrap {
  position: relative;
}
.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
  pointer-events: none;
}
.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.2rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #222;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.2s;
}
.search-input:focus {
  border-color: var(--color-primary, #1a6eb5);
}
.dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: #fff;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  list-style: none;
  margin: 0;
  padding: 0.25rem 0;
  z-index: 100;
  max-height: 240px;
  overflow-y: auto;
}
.dropdown-empty {
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
  color: #888;
}
.dropdown-item {
  padding: 0.7rem 1rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: #1a1a1a;
  cursor: pointer;
  transition: background 0.15s;
}
.dropdown-item:hover {
  background: #f5f5f5;
}

/* Toggles */
.toggle-group {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.toggle-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
  padding: 0.6rem 1rem;
  border: 2px solid #ddd;
  border-radius: 10px;
  background: #fff;
  cursor: pointer;
  color: #555;
  transition:
    border-color 0.15s,
    background 0.15s,
    color 0.15s;
  min-width: 68px;
}
.toggle-btn:hover {
  border-color: var(--color-primary, #1a6eb5);
  color: var(--color-primary, #1a6eb5);
}
.toggle-btn.active {
  border-color: var(--color-primary, #1a6eb5);
  background: var(--color-primary, #1a6eb5);
  color: #fff;
}
.toggle-icon {
  font-size: 1.25rem;
}
.toggle-label {
  font-weight: 600;
  font-size: 0.82rem;
}
.toggle-btn--dur {
  flex-direction: row;
  font-weight: 600;
  font-size: 0.88rem;
  min-width: 68px;
  justify-content: center;
}

/* Slider */
.slider-wrap {
  position: relative;
  padding-bottom: 1.5rem;
}
.slider {
  width: 100%;
  height: 6px;
  appearance: none;
  border-radius: 4px;
  background: linear-gradient(
    to right,
    var(--color-primary, #1a6eb5) var(--fill, 0%),
    #ddd var(--fill, 0%)
  );
  outline: none;
  cursor: pointer;
}
.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-primary, #1a6eb5);
  border: 3px solid #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
}
.time-badge {
  font-size: 0.85rem;
  font-weight: 700;
  background: var(--color-primary, #1a6eb5);
  color: #fff;
  padding: 0.1rem 0.55rem;
  border-radius: 20px;
}
.slider-ticks {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1.2rem;
}
.slider-ticks span {
  position: absolute;
  transform: translateX(-50%);
  font-size: 0.72rem;
  color: #888;
  white-space: nowrap;
}

/* Submit */
.submit-btn {
  width: 100%;
  margin-top: 0.5rem;
  padding: 0.9rem;
  background: var(--color-primary, #1a6eb5);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition:
    filter 0.2s,
    opacity 0.2s;
}
.submit-btn:hover:not(:disabled) {
  filter: brightness(1.1);
}
.submit-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
