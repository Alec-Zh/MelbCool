<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
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
const detailRef = ref(null)
const searchRef = ref(null)

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

async function selectSuburb(suburb) {
  async function scrollToSearch() {
    await nextTick()
    const offset = searchRef.value?.getBoundingClientRect().top + window.scrollY - 64 - 16
    window.scrollTo({ top: offset, behavior: 'smooth' })
  }

  // null means search was cleared — deselect and scroll back to search bar
  if (!suburb) {
    selectedSuburb.value = null
    scrollToSearch()
    return
  }

  const isSame = selectedSuburb.value?.suburb_name === suburb.suburb_name

  // Toggle: clicking the same suburb deselects and scrolls back to search bar
  if (isSame) {
    selectedSuburb.value = null
    scrollToSearch()
    return
  }

  selectedSuburb.value = suburb
  await nextTick()
  const el = detailRef.value
  if (el) {
    // 64px sticky navbar + 100px map peek so user can click map to deselect
    const offset = el.getBoundingClientRect().top + window.scrollY - 64 - 100
    window.scrollTo({ top: offset, behavior: 'smooth' })
  }
}

onMounted(fetchSuburbs)
</script>

<template>
  <div class="page">
    <NavBar />
    <main class="content">
      <div class="page-header">
        <h1 class="page-title">Heat Vulnerability Map</h1>
        <p class="page-desc">
          See how hot it is across inner Melbourne and which areas may need extra care during hot
          weather. Click on any suburb to view details.
        </p>
      </div>

      <div v-if="loading" class="status-msg">Loading suburb data...</div>
      <div v-else-if="error" class="status-msg error">{{ error }}</div>

      <template v-else>
        <!-- searchRef must be inside v-else so suburbs prop is populated before search is usable -->
        <div ref="searchRef">
          <SuburbSearch :suburbs="innerSuburbs" @select="selectSuburb" />
        </div>
        <SuburbMap
          :suburbs="innerSuburbs"
          :selectedSuburb="selectedSuburb"
          @select="selectSuburb"
        />
        <!-- Scroll target; SuburbDetail only renders when a suburb is selected -->
        <div ref="detailRef">
          <SuburbDetail v-if="selectedSuburb" :suburb="selectedSuburb" />
        </div>
      </template>

      <HeatLevelGuide />
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
