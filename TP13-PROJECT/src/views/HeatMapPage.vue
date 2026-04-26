<script setup>
import { ref, computed, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import SuburbSearch from '../components/SuburbSearch.vue'
import SuburbDetail from '../components/SuburbDetail.vue'
import SuburbMap from '../components/SuburbMap.vue'
import HeatLevelGuide from '../components/HeatLevelGuide.vue'
import Footer from '../components/Footer.vue'

const API_BASE = 'https://qcbqul6ys2.execute-api.ap-southeast-2.amazonaws.com'

const INNER_MELBOURNE = new Set([
  'Aberfeldie',
  'Airport West',
  'Albert Park (Vic.)',
  'Armadale (Vic.)',
  'Ascot Vale',
  'Avondale Heights',
  'Balaclava (Vic.)',
  'Brunswick (Vic.)',
  'Brunswick East',
  'Brunswick West',
  'Burnley',
  'Carlton (Vic.)',
  'Carlton North',
  'Clifton Hill',
  'Coburg',
  'Coburg North',
  'Collingwood (Vic.)',
  'Cremorne (Vic.)',
  'Docklands',
  'East Melbourne',
  'Elwood',
  'Essendon',
  'Essendon Fields',
  'Essendon North',
  'Essendon West',
  'Fairfield (Vic.)',
  'Fawkner',
  'Fitzroy (Vic.)',
  'Fitzroy North',
  'Flemington',
  'Glenroy (Vic.)',
  'Gowanbrae',
  'Hadfield',
  'Keilor East',
  'Kensington (Vic.)',
  'Kooyong',
  'Malvern (Vic.)',
  'Malvern East',
  'Melbourne',
  'Middle Park (Vic.)',
  'Moonee Ponds',
  'Niddrie',
  'North Melbourne',
  'Oak Park',
  'Parkville (Vic.)',
  'Pascoe Vale',
  'Pascoe Vale South',
  'Port Melbourne',
  'Prahran',
  'Princes Hill',
  'Richmond (Vic.)',
  'Ripponlea',
  'South Melbourne',
  'South Wharf',
  'South Yarra',
  'Southbank',
  'St Kilda (Vic.)',
  'St Kilda West',
  'Strathmore (Vic.)',
  'Strathmore Heights',
  'Toorak',
  'Travancore',
  'West Melbourne',
  'Windsor (Vic.)',
])

const allSuburbs = ref([])
const loading = ref(true)
const error = ref(null)
const selectedSuburb = ref(null)

const innerSuburbs = computed(() =>
  allSuburbs.value.filter((s) => INNER_MELBOURNE.has(s.suburb_name)),
)

async function fetchSuburbs() {
  try {
    loading.value = true
    error.value = null
    const res = await fetch(`${API_BASE}/suburbs`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    allSuburbs.value = await res.json()
  } catch (e) {
    error.value = 'Failed to load suburb data. Please try again.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

function selectSuburb(suburb) {
  if (!suburb) {
    selectedSuburb.value = null
    return
  }
  const isSame = selectedSuburb.value?.suburb_name === suburb.suburb_name
  selectedSuburb.value = isSame ? null : suburb
}

function clearSelection() {
  selectedSuburb.value = null
}

onMounted(fetchSuburbs)
</script>

<template>
  <div class="page">
    <NavBar />
    <main class="content">
      <!-- Page header -->
      <div class="page-header">
        <h1 class="page-title">Heat Safety Map</h1>
        <p class="page-desc">
          See how hot it feels right now across inner Melbourne suburbs.
          <strong>Click any suburb</strong> on the map or use the search bar to view details.
        </p>
      </div>

      <div v-if="loading" class="status-msg">Loading suburb data...</div>
      <div v-else-if="error" class="status-msg error">{{ error }}</div>

      <template v-else>
        <SuburbSearch :suburbs="innerSuburbs" @select="selectSuburb" />

        <!-- Map + right panel side by side -->
        <div class="map-panel-row">
          <!-- Map -->
          <div class="map-col">
            <SuburbMap
              :suburbs="innerSuburbs"
              :selectedSuburb="selectedSuburb"
              @select="selectSuburb"
            />
          </div>

          <!-- Right panel: legend by default, detail when suburb selected -->
          <div class="right-col">
            <Transition name="panel-switch" mode="out-in">
              <SuburbDetail
                v-if="selectedSuburb"
                :key="selectedSuburb.suburb_name"
                :suburb="selectedSuburb"
                @close="clearSelection"
              />
              <HeatLevelGuide v-else />
            </Transition>
          </div>
        </div>
      </template>
    </main>
    <Footer />
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.page-header {
  background: linear-gradient(135deg, #0d3a8f 0%, #1a56c4 100%);
  margin: 0 -1.5rem;
  padding: 2.25rem 1.5rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.4rem;
}

.page-desc {
  font-size: 1.05rem;
  color: rgba(255, 255, 255, 0.88);
  line-height: 1.65;
  max-width: 620px;
}

.page-desc strong {
  color: #ffffff;
}

/* Map + right panel */
.map-panel-row {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 1.25rem;
  align-items: stretch;
}

.map-col {
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.right-col {
  position: sticky;
  top: 88px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  /* hide scrollbar visually but keep functionality */
  scrollbar-width: thin;
  scrollbar-color: var(--color-border) transparent;
}

@media (max-width: 960px) {
  .map-panel-row {
    grid-template-columns: 1fr;
  }
  .right-col {
    position: static;
    max-height: none;
  }
}

/* Panel switch transition */
.panel-switch-enter-active,
.panel-switch-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}
.panel-switch-enter-from {
  opacity: 0;
  transform: translateX(10px);
}
.panel-switch-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

.status-msg {
  text-align: center;
  padding: 3rem 0;
  color: var(--color-text-muted);
  font-size: 1rem;
}

.status-msg.error {
  color: #991b1b;
}
</style>
