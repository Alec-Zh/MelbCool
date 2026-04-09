<script setup>
import { ref, computed } from 'vue'
import NavBar from '../components/NavBar.vue'
import SuburbSearch from '../components/SuburbSearch.vue'
import SuburbCard from '../components/SuburbCard.vue'
import SuburbDetail from '../components/SuburbDetail.vue'
import MapPlaceholder from '../components/MapPlaceholder.vue'
import HeatLevelGuide from '../components/HeatLevelGuide.vue'

// ── Mock data (replace with API call once Lambda is ready) ──
const suburbs = ref([
  {
    suburb_name: 'Carlton',
    temperature: 42,
    tree_canopy_percent: 15,
    heat_level: 'higher',
    elderly_population: 1200,
    total_population: 8500,
    risk_level: 'high',
  },
  {
    suburb_name: 'Footscray',
    temperature: 41,
    tree_canopy_percent: 18,
    heat_level: 'higher',
    elderly_population: 980,
    total_population: 12000,
    risk_level: 'high',
  },
  {
    suburb_name: 'Sunshine',
    temperature: 41,
    tree_canopy_percent: 16,
    heat_level: 'higher',
    elderly_population: 1500,
    total_population: 15000,
    risk_level: 'high',
  },
  {
    suburb_name: 'Brunswick',
    temperature: 38,
    tree_canopy_percent: 24,
    heat_level: 'moderate',
    elderly_population: 870,
    total_population: 11000,
    risk_level: 'moderate',
  },
  {
    suburb_name: 'Fitzroy',
    temperature: 37,
    tree_canopy_percent: 22,
    heat_level: 'moderate',
    elderly_population: 620,
    total_population: 9000,
    risk_level: 'moderate',
  },
  {
    suburb_name: 'Richmond',
    temperature: 36,
    tree_canopy_percent: 20,
    heat_level: 'moderate',
    elderly_population: 740,
    total_population: 10500,
    risk_level: 'moderate',
  },
  {
    suburb_name: 'St Kilda',
    temperature: 33,
    tree_canopy_percent: 31,
    heat_level: 'lower',
    elderly_population: 1100,
    total_population: 13000,
    risk_level: 'low',
  },
  {
    suburb_name: 'Brighton',
    temperature: 31,
    tree_canopy_percent: 38,
    heat_level: 'lower',
    elderly_population: 2200,
    total_population: 18000,
    risk_level: 'low',
  },
  {
    suburb_name: 'Williamstown',
    temperature: 30,
    tree_canopy_percent: 35,
    heat_level: 'lower',
    elderly_population: 1800,
    total_population: 14000,
    risk_level: 'low',
  },
])

const search = ref('')
const selectedSuburb = ref(null)

const filtered = computed(() => {
  if (!search.value.trim()) return suburbs.value
  return suburbs.value.filter((s) =>
    s.suburb_name.toLowerCase().includes(search.value.toLowerCase()),
  )
})

function selectSuburb(suburb) {
  selectedSuburb.value = selectedSuburb.value?.suburb_name === suburb.suburb_name ? null : suburb
}
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

      <MapPlaceholder />

      <div class="suburb-list">
        <SuburbCard
          v-for="suburb in filtered"
          :key="suburb.suburb_name"
          :suburb="suburb"
          :selected="selectedSuburb?.suburb_name === suburb.suburb_name"
          @select="selectSuburb"
        />
        <p v-if="filtered.length === 0" class="no-results">No suburbs found.</p>
      </div>

      <SuburbDetail v-if="selectedSuburb" :suburb="selectedSuburb" />

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
