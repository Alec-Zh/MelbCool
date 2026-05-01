<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  suburbs: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['suburb-found', 'out-of-range'])

// idle | locating | found | out-of-range | denied | error
const status = ref('idle')
const foundSuburbName = ref('')

function haversineKm(lat1, lon1, lat2, lon2) {
  const R = 6371
  const dLat = ((lat2 - lat1) * Math.PI) / 180
  const dLon = ((lon2 - lon1) * Math.PI) / 180
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) ** 2
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}

function findNearestSuburb(lat, lon) {
  let nearest = null
  let minDist = Infinity
  for (const s of props.suburbs) {
    const d = haversineKm(lat, lon, s.latitude, s.longitude)
    if (d < minDist) {
      minDist = d
      nearest = s
    }
  }
  // threshold: 4 km — covers suburb centre-to-edge comfortably
  return minDist <= 4 ? nearest : null
}

function locate() {
  if (!navigator.geolocation) {
    status.value = 'error'
    return
  }
  status.value = 'locating'
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const { latitude, longitude } = pos.coords
      const suburb = findNearestSuburb(latitude, longitude)
      if (suburb) {
        status.value = 'found'
        foundSuburbName.value = suburb.suburb_name
        emit('suburb-found', suburb)
      } else {
        status.value = 'out-of-range'
        emit('out-of-range')
      }
    },
    (err) => {
      status.value = err.code === err.PERMISSION_DENIED ? 'denied' : 'error'
    },
    { timeout: 10000, maximumAge: 60000 },
  )
}

// Auto-locate on mount — suburbs must already be loaded by parent
onMounted(() => {
  if (props.suburbs.length > 0) locate()
})
</script>

<template>
  <div class="lf-wrap">
    <!-- Locating spinner -->
    <div v-if="status === 'locating'" class="lf-pill lf-locating">
      <span class="lf-spinner" aria-hidden="true"></span>
      <span>Finding your location…</span>
    </div>

    <!-- Found -->
    <div v-else-if="status === 'found'" class="lf-row">
      <div class="lf-pill lf-found">
        <svg
          class="lf-icon"
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
          stroke-linecap="round"
          stroke-linejoin="round"
          aria-hidden="true"
        >
          <path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z" />
          <circle cx="12" cy="10" r="3" />
        </svg>
        <span>{{ foundSuburbName }}</span>
      </div>
      <button class="lf-refresh-btn" @click="locate" aria-label="Refresh location">
        🔄 Refresh location
      </button>
    </div>

    <!-- Out of range -->
    <div v-else-if="status === 'out-of-range'" class="lf-row">
      <div class="lf-pill lf-outrange">
        <svg
          class="lf-icon"
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
          stroke-linecap="round"
          stroke-linejoin="round"
          aria-hidden="true"
        >
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <span>Outside covered area</span>
      </div>
      <button class="lf-refresh-btn" @click="locate" aria-label="Try again">
        🔄 Try again
      </button>
    </div>

    <!-- Permission denied -->
    <div v-else-if="status === 'denied'" class="lf-pill lf-denied">
      <svg
        class="lf-icon"
        width="14"
        height="14"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        stroke-linecap="round"
        stroke-linejoin="round"
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="10" />
        <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
      </svg>
      <span>Location access denied</span>
    </div>

    <!-- Generic error -->
    <div v-else-if="status === 'error'" class="lf-row">
      <div class="lf-pill lf-denied">
        <svg
          class="lf-icon"
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
          stroke-linecap="round"
          stroke-linejoin="round"
          aria-hidden="true"
        >
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <span>Location unavailable</span>
      </div>
      <button class="lf-refresh-btn" @click="locate" aria-label="Try again">
        🔄 Try again
      </button>
    </div>

    <!-- Idle: show button before first attempt (shouldn't show long due to auto-locate) -->
    <button v-else class="lf-pill lf-idle" @click="locate">
      <svg
        class="lf-icon"
        width="14"
        height="14"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        stroke-linecap="round"
        stroke-linejoin="round"
        aria-hidden="true"
      >
        <path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z" />
        <circle cx="12" cy="10" r="3" />
      </svg>
      <span>Find my location</span>
    </button>
  </div>
</template>

<style scoped>
.lf-wrap {
  display: flex;
  align-items: center;
}

.lf-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

/* Base pill */
.lf-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.75rem;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 500;
  line-height: 1;
  white-space: nowrap;
  border: none;
  cursor: default;
  transition: background 0.15s;
}

/* Idle — clickable */
.lf-idle {
  background: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.25);
}
.lf-idle:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* Locating */
.lf-locating {
  background: rgba(255, 255, 255, 0.12);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

/* Found */
.lf-found {
  background: rgba(16, 185, 129, 0.2);
  color: #a7f3d0;
  border: 1px solid rgba(16, 185, 129, 0.35);
}

/* Out of range */
.lf-outrange {
  background: rgba(251, 191, 36, 0.15);
  color: #fde68a;
  border: 1px solid rgba(251, 191, 36, 0.3);
}

/* Denied / error */
.lf-denied {
  background: rgba(239, 68, 68, 0.12);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.25);
}

.lf-icon {
  flex-shrink: 0;
  opacity: 0.9;
}

/* Refresh — visible text button */
.lf-refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  border: 1.5px solid rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s, border-color 0.15s;
}
.lf-refresh-btn:hover {
  background: rgba(255, 255, 255, 0.28);
  border-color: rgba(255, 255, 255, 0.75);
}

/* Spinner */
.lf-spinner {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.25);
  border-top-color: rgba(255, 255, 255, 0.8);
  animation: lf-spin 0.7s linear infinite;
  flex-shrink: 0;
}

@keyframes lf-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>