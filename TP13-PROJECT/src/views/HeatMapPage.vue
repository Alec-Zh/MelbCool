<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import SuburbSearch from '../components/SuburbSearch.vue'
import SuburbList from '../components/SuburbList.vue'
import SuburbDetail from '../components/SuburbDetail.vue'
import SuburbMap from '../components/SuburbMap.vue'
import HeatLevelGuide from '../components/HeatLevelGuide.vue'

const API_BASE = 'https://qcbqul6ys2.execute-api.ap-southeast-2.amazonaws.com'

const INNER_MELBOURNE = new Set([
  'Abbotsford',
  'Albert Park',
  'Alphington - Fairfield',
  'Armadale',
  'Ascot Vale',
  'Brunswick - North',
  'Brunswick - South',
  'Brunswick East',
  'Brunswick West',
  'Carlton',
  'Carlton North - Princes Hill',
  'Clifton Hill - Alphington',
  'Coburg - East',
  'Coburg - West',
  'Collingwood',
  'Docklands',
  'East Melbourne',
  'Elwood',
  'Essendon (West) - Aberfeldie',
  'Essendon - East',
  'Fitzroy',
  'Fitzroy North',
  'Flemington',
  'Flemington Racecourse',
  'Kensington (Vic.)',
  'Melbourne CBD - East',
  'Melbourne CBD - North',
  'Melbourne CBD - West',
  'Moonee Ponds',
  'North Melbourne',
  'Northcote - East',
  'Northcote - West',
  'Parkville',
  'Pascoe Vale South',
  'Port Melbourne',
  'Port Melbourne Industrial',
  'Prahran - Windsor',
  'Richmond (South) - Cremorne',
  'Richmond - North',
  'Royal Botanic Gardens Victoria',
  'South Melbourne',
  'South Yarra - North',
  'South Yarra - South',
  'South Yarra - West',
  'Southbank (West) - South Wharf',
  'Southbank - East',
  'St Kilda - Central',
  'St Kilda - West',
  'St Kilda East',
  'Thornbury',
  'Toorak',
  'West Melbourne - Industrial',
  'West Melbourne - Residential',
])

const allSuburbs = ref([])
const loading = ref(true)
const error = ref(null)
const search = ref('')
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
  selectedSuburb.value = selectedSuburb.value?.suburb_name === suburb.suburb_name ? null : suburb
  if (selectedSuburb.value) search.value = ''
}

onMounted(fetchSuburbs)

watch(search, (val) => {
  if (val.trim()) selectedSuburb.value = null
})
</script>

<template>
  <div class="page">
    <NavBar />
    <main class="content">
      <div class="page-header">
        <h1 class="page-title">Heat Vulnerability Map</h1>
        <p class="page-desc">
          Explore heat levels across Melbourne suburbs based on temperature, tree coverage, and
          elderly population density.
        </p>
      </div>

      <SuburbSearch v-model="search" />

      <div v-if="loading" class="status-msg">Loading suburb data...</div>
      <div v-else-if="error" class="status-msg error">{{ error }}</div>

      <template v-else>
        <SuburbMap
          :suburbs="innerSuburbs"
          :selectedSuburb="selectedSuburb"
          @select="selectSuburb"
        />
        <SuburbList
          :suburbs="innerSuburbs"
          :selectedSuburb="selectedSuburb"
          :search="search"
          @select="selectSuburb"
        />
        <SuburbDetail v-if="selectedSuburb" :suburb="selectedSuburb" />
      </template>

      <HeatLevelGuide />
    </main>
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
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  margin-bottom: 0.5rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 0.4rem;
}

.page-desc {
  font-size: 1rem;
  color: var(--color-text-muted);
  line-height: 1.6;
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
