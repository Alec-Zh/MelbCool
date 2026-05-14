<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import OutfitWeatherCard from '../components/OutfitWeatherCard.vue'
import OutfitItemCard from '../components/OutfitItemCard.vue'

const API_BASE = 'https://qcbqul6ys2.execute-api.ap-southeast-2.amazonaws.com'

const route = useRoute()

// ── Suburb data ──────────────────────────────────────────────────────────────
const allSuburbs = ref([])
const loading = ref(true)
const error = ref(null)
const selectedSuburbId = ref('')

const selectedSuburb = computed(
  () => allSuburbs.value.find((s) => s.suburb_id === Number(selectedSuburbId.value)) ?? null,
)

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/suburbs`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    allSuburbs.value = (await res.json()).sort((a, b) => a.suburb_name.localeCompare(b.suburb_name))
    // Prefer suburbId from route query (passed from SuburbDetail),
    // fall back to first suburb in list
    const queryId = route.query.suburbId
    if (queryId && allSuburbs.value.find((s) => s.suburb_id === Number(queryId))) {
      selectedSuburbId.value = String(queryId)
    } else if (allSuburbs.value.length) {
      selectedSuburbId.value = String(allSuburbs.value[0].suburb_id)
    }
  } catch (e) {
    error.value = 'Could not load suburb data. Please try again.'
    console.error(e)
  } finally {
    loading.value = false
  }
})

// AC 4.1.3 — reset selected outfit when suburb changes
watch(selectedSuburbId, () => {
  selectedItems.value = new Set()
})

// ── Climate mode (temperature-based) ─────────────────────────────────────────
const climateMode = computed(() => {
  const t = selectedSuburb.value?.apparent_temperature ?? 25
  if (t < 18) return 'cool'
  if (t < 28) return 'mild'
  return 'hot'
})

const uvHigh = computed(() => (selectedSuburb.value?.uv_index ?? 0) >= 3)

// ── Master item list ──────────────────────────────────────────────────────────
// modes: which climateMode values this item appears in, and as what category
// uvOnly: if true, only shown when uv_index >= 3 (independent of temperature)
// effect/explanation: keyed by climateMode for context-aware text
const ALL_ITEMS = [
  {
    id: 'hat',
    name: 'Wide-brim hat',
    icon: '🎩',
    modes: { hot: 'good', mild: 'good', cool: 'good' },
    effect: {
      hot: 'Blocks UV and reduces heat stress on your head and neck',
      mild: 'Good sun protection even on mild days',
      cool: 'Keeps head warm and still provides some UV cover',
    },
    explanation: {},
    heatAdj: -1.5,
    layer: 'lh',
    uvOnly: false,
  },
  {
    id: 'shirt',
    name: 'Light cotton shirt',
    icon: '👕',
    modes: { hot: 'good', mild: 'good', cool: 'bad' },
    effect: {
      hot: 'Breathable and reflects heat — ideal for hot weather',
      mild: 'Comfortable and breathable on a mild day',
      cool: 'Too light for today — likely too cold outside',
    },
    explanation: {
      cool: 'Light fabrics provide little insulation in cool conditions.',
    },
    heatAdj: -1.5,
    layer: 'ls',
    uvOnly: false,
  },
  {
    id: 'pants',
    name: 'Loose light pants',
    icon: '👖',
    modes: { hot: 'good', mild: 'good', cool: 'bad' },
    effect: {
      hot: 'Good airflow and UV coverage for hot conditions',
      mild: 'Comfortable with enough air circulation',
      cool: "Not warm enough for today's temperature",
    },
    explanation: {
      cool: "Light pants won't keep you warm in cool or cold weather.",
    },
    heatAdj: -1.0,
    layer: 'lp',
    uvOnly: false,
  },
  {
    id: 'sg',
    name: 'Sunglasses',
    icon: '🕶️',
    modes: { hot: 'good', mild: 'good', cool: 'good' },
    effect: {
      hot: 'UV is high — eye protection is essential today',
      mild: 'UV is moderate or above — sunglasses are recommended',
      cool: 'UV can still be significant in cool weather — protect your eyes',
    },
    explanation: {},
    heatAdj: -0.3,
    layer: 'lsg',
    uvOnly: true,
  },
  {
    id: 'water',
    name: 'Water bottle',
    icon: '🍶',
    modes: { hot: 'good', mild: 'good', cool: 'good' },
    effect: {
      hot: 'Drink every 15–20 min outdoors — dehydration risk is high',
      mild: "Stay hydrated, especially if you're active outside",
      cool: 'Good habit even in cool weather — easy to forget when not sweating',
    },
    explanation: {},
    heatAdj: -0.8,
    layer: 'lw',
    uvOnly: false,
  },
  {
    id: 'sc',
    name: 'Sunscreen SPF 50+',
    icon: '🧴',
    modes: { hot: 'good', mild: 'good', cool: 'good' },
    effect: {
      hot: 'Apply before going out and reapply every 2 hours',
      mild: 'UV is moderate or above — sunscreen is still important',
      cool: "UV doesn't disappear in winter — apply before heading out",
    },
    explanation: {},
    heatAdj: -0.3,
    layer: 'lsc',
    uvOnly: true,
  },
  {
    id: 'warmjacket',
    name: 'Warm jacket',
    icon: '🧥',
    modes: { cool: 'good' },
    effect: {
      cool: 'Good insulation for cool conditions — keeps core temperature stable',
    },
    explanation: {},
    heatAdj: 1.5,
    layer: 'lj',
    uvOnly: false,
  },
  {
    id: 'jacket',
    name: 'Dark heavy jacket',
    icon: '🧥',
    modes: { hot: 'bad', mild: 'bad' },
    effect: {
      hot: 'Traps heat — significantly raises your body temperature',
      mild: 'Too warm for today — raises heat exposure unnecessarily',
    },
    explanation: {
      hot: 'Heavy dark jackets trap heat and block airflow in warm conditions.',
      mild: 'Even on mild days, heavy jackets can cause overheating during activity.',
    },
    heatAdj: 3.5,
    layer: 'lj',
    uvOnly: false,
  },
  {
    id: 'dshirt',
    name: 'Tight dark shirt',
    icon: '👔',
    modes: { hot: 'bad', mild: 'bad' },
    effect: {
      hot: 'Absorbs heat and restricts airflow — uncomfortable and risky',
      mild: 'Dark tight fabric absorbs more heat than needed today',
    },
    explanation: {
      hot: 'Dark fabric absorbs sunlight and tight fit reduces air circulation.',
      mild: 'Even on mild days, dark tight clothing can make you warmer than expected.',
    },
    heatAdj: 2.5,
    layer: 'ld',
    uvOnly: false,
  },
]

// ── Dynamic item lists based on climate mode + UV ─────────────────────────────
const activeItems = computed(() => {
  const mode = climateMode.value
  return ALL_ITEMS.filter((item) => {
    if (!item.modes[mode]) return false
    if (item.uvOnly && !uvHigh.value) return false
    return true
  }).map((item) => ({
    ...item,
    category: item.modes[climateMode.value],
    effect: item.effect[climateMode.value] ?? '',
    explanation: item.explanation[climateMode.value] ?? null,
  }))
})

const goodItems = computed(() => activeItems.value.filter((i) => i.category === 'good'))
const badItems = computed(() => activeItems.value.filter((i) => i.category === 'bad'))

// ── Selection state (AC 4.2.3) ───────────────────────────────────────────────
const selectedItems = ref(new Set())

function toggleItem(id) {
  const next = new Set(selectedItems.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  selectedItems.value = next
}

function isSelected(id) {
  return selectedItems.value.has(id)
}

// ── Heat exposure score (AC 4.2.2) ──────────────────────────────────────────
const exposureTemp = computed(() => {
  const base = selectedSuburb.value?.apparent_temperature ?? null
  if (base === null) return null
  let adj = 0
  selectedItems.value.forEach((id) => {
    const item = ALL_ITEMS.find((i) => i.id === id)
    if (item) adj += item.heatAdj
  })
  return Math.round((base + adj) * 10) / 10
})

const exposureBarPct = computed(() => {
  if (exposureTemp.value === null) return 0
  return Math.max(3, Math.min(97, ((exposureTemp.value - 10) / (45 - 10)) * 100))
})

const exposureConfig = computed(() => {
  const t = exposureTemp.value
  const mode = climateMode.value
  if (t === null) return { color: '#9e9890', label: 'Select a suburb to begin', pulse: false }
  if (mode === 'cool') {
    if (t < 14)
      return { color: '#185FA5', label: 'Cold — dress warmly before heading out', pulse: false }
    if (t < 18)
      return { color: '#4d9e5a', label: 'Cool — comfortable with the right layers', pulse: false }
  }
  if (t < 31) return { color: '#4d9e5a', label: 'Low — good outfit for today', pulse: false }
  if (t < 34) return { color: '#e8903a', label: 'Moderate — take care outside', pulse: false }
  if (t < 37) return { color: '#c0392b', label: 'High — limit time outdoors', pulse: false }
  return { color: '#8b1a12', label: 'Danger — seek cool shelter now', pulse: true }
})

// ── Personalised advice (climate + UV aware) ──────────────────────────────────
const adviceItems = computed(() => {
  const s = selectedItems.value
  const mode = climateMode.value
  const uv = uvHigh.value

  if (!s.size) {
    return [{ color: '#9e9890', text: 'Select clothing items above to see personalised advice.' }]
  }

  const msgs = []

  if (mode === 'cool') {
    if (s.has('warmjacket'))
      msgs.push({
        color: '#2d7a3a',
        text: 'Good choice — a warm jacket helps maintain body temperature in cool conditions.',
      })
    if (s.has('shirt') && !s.has('warmjacket'))
      msgs.push({
        color: '#c0392b',
        text: "A light cotton shirt alone won't keep you warm today — consider adding a warm layer on top.",
      })
    if (s.has('pants'))
      msgs.push({
        color: '#c0392b',
        text: 'Light pants may not be warm enough today. Thicker trousers will be more comfortable.',
      })
    if (s.has('hat'))
      msgs.push({
        color: '#2d7a3a',
        text: 'Good idea — a hat helps retain heat in cool conditions and still provides some UV cover.',
      })
    if (s.has('water'))
      msgs.push({
        color: '#185FA5',
        text: "Good habit — it's easy to forget hydration in cool weather, but it's still important.",
      })
  } else if (mode === 'mild') {
    if (s.has('jacket'))
      msgs.push({
        color: '#e8903a',
        text: "A heavy jacket is too warm for today — you may overheat, especially if you're active.",
      })
    if (s.has('dshirt'))
      msgs.push({
        color: '#e8903a',
        text: 'Tight dark shirts absorb heat and reduce airflow — a lighter top would be more comfortable today.',
      })
    if (s.has('hat'))
      msgs.push({
        color: '#2d7a3a',
        text: 'Wide-brim hat is a good choice — even on mild days, sun protection matters.',
      })
    if (s.has('shirt'))
      msgs.push({
        color: '#2d7a3a',
        text: 'Light cotton is comfortable and breathable on a mild day.',
      })
    if (s.has('water'))
      msgs.push({
        color: '#185FA5',
        text: "Good habit — staying hydrated is important even when it doesn't feel hot.",
      })
  } else {
    if (s.has('jacket'))
      msgs.push({
        color: '#c0392b',
        text: 'Dark heavy jacket is dangerous today — it traps heat and significantly raises your body temperature. Remove it.',
      })
    if (s.has('dshirt'))
      msgs.push({
        color: '#c0392b',
        text: "Tight dark shirt absorbs heat and blocks airflow. This is unsafe in today's heat.",
      })
    if (s.has('hat'))
      msgs.push({
        color: '#2d7a3a',
        text: 'Wide-brim hat is essential in this heat — it blocks UV and reduces heat stress on your head and neck.',
      })
    if (s.has('shirt'))
      msgs.push({
        color: '#2d7a3a',
        text: 'Light cotton shirt is a great choice — it breathes well and reflects sunlight.',
      })
    if (s.has('pants'))
      msgs.push({
        color: '#2d7a3a',
        text: 'Loose light pants keep your legs cool and protected from UV at the same time.',
      })
    if (s.has('water'))
      msgs.push({
        color: '#185FA5',
        text: 'Carry water and drink every 15–20 minutes when outside. Dehydration is a serious risk today.',
      })
  }

  if (uv) {
    if (s.has('sg'))
      msgs.push({
        color: '#2d7a3a',
        text: 'Sunglasses are important today — UV is high enough to cause eye strain and long-term damage.',
      })
    if (s.has('sc'))
      msgs.push({
        color: '#2d7a3a',
        text: 'SPF 50+ sunscreen is the right call. Apply 20 minutes before going out and reapply every 2 hours.',
      })
    if (!s.has('sg') && !s.has('sc') && mode !== 'cool')
      msgs.push({
        color: '#e8903a',
        text: 'UV is high today — add sunglasses and sunscreen before heading out.',
      })
  }

  if (!s.has('water') && mode !== 'cool')
    msgs.push({
      color: '#e8903a',
      text: "Don't forget water — dehydration is easy to miss until it's too late, especially for older adults.",
    })

  return msgs
})
</script>

<template>
  <div class="page">
    <NavBar />

    <main class="content">
      <!-- Page header -->
      <div class="page-header card">
        <h1 class="page-title">Outfit <span class="page-title-accent">Advisor</span></h1>
        <p class="page-desc">
          See what to wear based on today's heat and UV conditions.
          <strong>Select clothing items</strong> to check your personal heat exposure.
        </p>
      </div>

      <div v-if="loading" class="status-msg">Loading suburb data...</div>
      <div v-else-if="error" class="status-msg status-msg--error">{{ error }}</div>

      <template v-else>
        <!-- Suburb selector (AC 4.1.3) -->
        <div class="selector-row card">
          <label for="suburb-select" class="selector-label">
            <svg
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
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
            Suburb
          </label>
          <select id="suburb-select" v-model="selectedSuburbId" class="suburb-select">
            <option v-for="s in allSuburbs" :key="s.suburb_id" :value="String(s.suburb_id)">
              {{ s.suburb_name }}
            </option>
          </select>
        </div>

        <!-- AC 4.1.2 — Weather summary card -->
        <OutfitWeatherCard :suburb="selectedSuburb" />

        <!-- Climate mode indicator -->
        <div class="mode-banner" :class="`mode-banner--${climateMode}`">
          <span v-if="climateMode === 'cool'"
            >🧣 Cool day — recommendations are adjusted for lower temperatures</span
          >
          <span v-else-if="climateMode === 'mild'"
            >🌤 Mild day — balanced recommendations for comfortable conditions</span
          >
          <span v-else>☀️ Hot day — heat safety recommendations are active</span>
          <span v-if="!uvHigh" class="uv-note">
            | UV is low — sunglasses and sunscreen not shown</span
          >
        </div>

        <!-- Main grid: mannequin + item list -->
        <!-- How to use — full width above main grid -->
        <div class="guide-card card">
          <p class="guide-title">How to use</p>
          <ul class="guide-list guide-list--row">
            <li>Tap any item to add it to your outfit</li>
            <li>The mannequin updates as you select</li>
            <li>Green items lower your heat exposure</li>
            <li>Red items raise your heat risk</li>
            <li>Your score updates in real time</li>
          </ul>
        </div>

        <div class="main-grid">
          <!-- Left column: mannequin only -->
          <div class="left-col">
            <!-- Mannequin + score (AC 4.2.1 + 4.2.2) -->
            <div class="mannequin-col card">
              <p class="col-label">Outfit preview</p>

              <svg
                viewBox="0 0 160 282"
                xmlns="http://www.w3.org/2000/svg"
                class="mannequin-svg"
                aria-label="Outfit mannequin preview"
                role="img"
              >
                <!-- Base body -->
                <rect x="54" y="154" width="24" height="84" rx="9" fill="#F5C8A8" />
                <rect x="82" y="154" width="24" height="84" rx="9" fill="#F5C8A8" />
                <ellipse cx="66" cy="242" rx="16" ry="7" fill="#E0A882" />
                <ellipse cx="94" cy="242" rx="16" ry="7" fill="#E0A882" />
                <rect x="27" y="90" width="22" height="63" rx="9" fill="#F5C8A8" />
                <rect x="111" y="90" width="22" height="63" rx="9" fill="#F5C8A8" />
                <rect x="50" y="87" width="60" height="72" rx="9" fill="#F5C8A8" />
                <rect x="73" y="74" width="14" height="16" fill="#F5C8A8" />
                <circle cx="80" cy="54" r="27" fill="#F5C8A8" />
                <circle cx="72" cy="50" r="3.5" fill="#2d7a3a" />
                <circle cx="88" cy="50" r="3.5" fill="#2d7a3a" />
                <circle cx="73.5" cy="48.5" r="1.3" fill="white" />
                <circle cx="89.5" cy="48.5" r="1.3" fill="white" />
                <ellipse cx="80" cy="57" rx="2" ry="2.5" fill="#E0A882" />
                <path
                  d="M73 64 Q80 70 87 64"
                  stroke="#C48060"
                  stroke-width="2"
                  fill="none"
                  stroke-linecap="round"
                />
                <!-- Pants -->
                <g :style="{ display: isSelected('pants') ? '' : 'none' }">
                  <rect x="48" y="152" width="64" height="9" rx="3" fill="#7FA4BE" />
                  <rect x="48" y="158" width="30" height="80" rx="9" fill="#A8C4D8" />
                  <rect x="82" y="158" width="30" height="80" rx="9" fill="#A8C4D8" />
                </g>
                <!-- Light shirt -->
                <g
                  :style="{
                    display:
                      isSelected('shirt') && !isSelected('jacket') && !isSelected('dshirt')
                        ? ''
                        : 'none',
                  }"
                >
                  <rect x="25" y="88" width="25" height="65" rx="9" fill="#9FC4E8" />
                  <rect x="110" y="88" width="25" height="65" rx="9" fill="#9FC4E8" />
                  <rect x="48" y="85" width="64" height="74" rx="9" fill="#9FC4E8" />
                  <polygon points="80,85 68,106 92,106" fill="#7DAED8" />
                  <line x1="80" y1="106" x2="80" y2="158" stroke="#7DAED8" stroke-width="2" />
                </g>
                <!-- Jacket (shared layer: dark heavy jacket in hot/mild, warm jacket in cool) -->
                <g
                  :style="{
                    display: isSelected('jacket') || isSelected('warmjacket') ? '' : 'none',
                  }"
                >
                  <rect x="21" y="85" width="30" height="70" rx="10" fill="#2C2C2A" />
                  <rect x="109" y="85" width="30" height="70" rx="10" fill="#2C2C2A" />
                  <rect x="44" y="82" width="72" height="80" rx="10" fill="#2C2C2A" />
                  <polygon points="80,82 62,110 80,118" fill="#3A3A38" />
                  <polygon points="80,82 98,110 80,118" fill="#3A3A38" />
                  <line x1="80" y1="118" x2="80" y2="162" stroke="#3A3A38" stroke-width="2.5" />
                  <rect x="68" y="78" width="24" height="10" rx="5" fill="#3A3A38" />
                </g>
                <!-- Dark shirt (bad) -->
                <g
                  :style="{ display: isSelected('dshirt') && !isSelected('jacket') ? '' : 'none' }"
                >
                  <rect x="25" y="88" width="25" height="65" rx="9" fill="#2A2A2A" />
                  <rect x="110" y="88" width="25" height="65" rx="9" fill="#2A2A2A" />
                  <rect x="48" y="85" width="64" height="74" rx="9" fill="#2A2A2A" />
                  <polygon points="80,85 68,106 92,106" fill="#222" />
                </g>
                <!-- Hat -->
                <g :style="{ display: isSelected('hat') ? '' : 'none' }">
                  <ellipse cx="80" cy="31" rx="44" ry="9" fill="#C4A866" />
                  <rect x="59" y="9" width="42" height="28" rx="6" fill="#D4B886" />
                  <rect x="59" y="32" width="42" height="6" fill="#8B6914" />
                  <ellipse cx="80" cy="31" rx="44" ry="5" fill="#A08030" opacity=".3" />
                </g>
                <!-- Sunglasses -->
                <g :style="{ display: isSelected('sg') ? '' : 'none' }">
                  <rect x="64" y="45" width="15" height="11" rx="5" fill="#1a1a2e" opacity=".9" />
                  <rect x="81" y="45" width="15" height="11" rx="5" fill="#1a1a2e" opacity=".9" />
                  <line x1="79" y1="50" x2="81" y2="50" stroke="#555" stroke-width="1.5" />
                  <line x1="64" y1="50" x2="54" y2="53" stroke="#555" stroke-width="1.5" />
                  <line x1="96" y1="50" x2="106" y2="53" stroke="#555" stroke-width="1.5" />
                  <rect x="67" y="47" width="5" height="3" rx="2" fill="white" opacity=".22" />
                  <rect x="84" y="47" width="5" height="3" rx="2" fill="white" opacity=".22" />
                </g>
                <!-- Water bottle -->
                <g :style="{ display: isSelected('water') ? '' : 'none' }">
                  <rect x="116" y="120" width="13" height="33" rx="5" fill="#4d9e5a" />
                  <rect x="117" y="121" width="5" height="27" rx="3" fill="#7dc486" opacity=".4" />
                  <rect x="117" y="113" width="11" height="9" rx="3" fill="#2d7a3a" />
                  <line
                    x1="121"
                    y1="113"
                    x2="121"
                    y2="102"
                    stroke="#2d7a3a"
                    stroke-width="2.5"
                    stroke-linecap="round"
                  />
                  <rect x="118" y="132" width="9" height="2" rx="1" fill="white" opacity=".35" />
                </g>
                <!-- Sunscreen -->
                <g :style="{ display: isSelected('sc') ? '' : 'none' }">
                  <rect x="22" y="122" width="13" height="28" rx="4" fill="#FAC775" />
                  <rect x="22" y="113" width="13" height="11" rx="3" fill="#EF9F27" />
                  <rect x="27" y="106" width="4" height="9" rx="2" fill="#BA7517" />
                  <text
                    x="28.5"
                    y="137"
                    text-anchor="middle"
                    font-size="5.5"
                    fill="#6B4800"
                    font-weight="bold"
                    font-family="sans-serif"
                  >
                    SPF
                  </text>
                  <rect x="24" y="128" width="9" height="2" rx="1" fill="white" opacity=".35" />
                </g>
              </svg>

              <!-- Heat exposure score display -->
              <div class="score-area" v-if="exposureTemp !== null">
                <div class="score-row">
                  <span class="score-lbl">Heat exposure</span>
                  <span class="score-val" :style="{ color: exposureConfig.color }">
                    {{ exposureTemp.toFixed(1) }}°C
                  </span>
                </div>
                <div class="score-bar-bg">
                  <div
                    class="score-bar-fill"
                    :class="{ 'score-bar-fill--pulse': exposureConfig.pulse }"
                    :style="{
                      width: exposureBarPct + '%',
                      backgroundColor: exposureConfig.color,
                    }"
                  ></div>
                </div>
                <p class="score-status" :style="{ color: exposureConfig.color }">
                  {{ exposureConfig.label }}
                </p>
              </div>
            </div>

            <!-- Guide card -->
          </div>
          <!-- end left-col -->

          <!-- Item list (AC 4.1.1, 4.3.1, 4.3.2, 4.3.3) -->
          <div class="items-col">
            <!-- Good choices section (AC 4.3.1) -->
            <p class="section-label section-label--good">Good choices</p>
            <div class="items-list">
              <OutfitItemCard
                v-for="item in goodItems"
                :key="item.id"
                :item="item"
                :selected="isSelected(item.id)"
                @toggle="toggleItem"
              />
            </div>

            <!-- Avoid today section (AC 4.3.1) -->
            <p class="section-label section-label--bad">Avoid today</p>
            <div class="items-list">
              <OutfitItemCard
                v-for="item in badItems"
                :key="item.id"
                :item="item"
                :selected="isSelected(item.id)"
                @toggle="toggleItem"
              />
            </div>
          </div>
        </div>

        <!-- Advice card -->
        <div class="advice-card card">
          <p class="advice-title">Personalised heat advice</p>
          <ul class="advice-list">
            <li v-for="(msg, i) in adviceItems" :key="i" class="advice-item">
              <span class="advice-dot" :style="{ backgroundColor: msg.color }"></span>
              <span class="advice-text">{{ msg.text }}</span>
            </li>
          </ul>
        </div>

        <!-- Full-width navigation row -->
        <div class="nav-links">
          <RouterLink to="/heatmap" class="nav-link-btn">
            <svg
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
              <line x1="2" y1="12" x2="22" y2="12" />
              <path
                d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"
              />
            </svg>
            Check heat map
          </RouterLink>
          <RouterLink to="/trip-coach" class="nav-link-btn">
            <svg
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
              <polyline points="12 6 12 12 16 14" />
            </svg>
            Plan a trip
          </RouterLink>
        </div>
      </template>
    </main>

    <Footer />
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  background: linear-gradient(160deg, #eaf4f4 0%, #f0f7ee 50%, #e8f4f0 100%);
}

.content {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 1.25rem 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card {
  background: #ffffff;
  border-radius: 14px;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    0 8px 24px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

/* Page header */
.page-header {
  padding: 1.75rem 1.6rem;
  background: linear-gradient(135deg, rgba(13, 58, 143, 0.95), rgba(11, 127, 121, 0.88));
  border: none;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.page-title {
  font-size: 1.95rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  letter-spacing: -0.02em;
}

.page-title-accent {
  color: #a3f77d;
}

.page-desc {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin: 0;
}

.page-desc strong {
  color: #ffffff;
  font-weight: 600;
}

/* Suburb selector */
.selector-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 1rem;
}

.selector-label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #6b6560;
  white-space: nowrap;
  flex-shrink: 0;
}

.suburb-select {
  flex: 1;
  border: 1px solid #d8eae6;
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 15px;
  background: #f4faf8;
  color: #1a1714;
  cursor: pointer;
  font-family: inherit;
}

.suburb-select:focus {
  outline: 2px solid #4d9e5a;
  outline-offset: 1px;
}

/* Climate mode banner */
.mode-banner {
  padding: 0.65rem 1rem;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}

.mode-banner--hot {
  background: #fce8e6;
  color: #8b1a12;
}

.mode-banner--mild {
  background: #fef1e0;
  color: #7a4510;
}

.mode-banner--cool {
  background: #e6f0fb;
  color: #0c447c;
}

.uv-note {
  font-weight: 600;
}

/* Main grid */
.main-grid {
  display: grid;
  grid-template-columns: 156px minmax(0, 1fr);
  gap: 1rem;
  align-items: start;
}

/* Left column — mannequin only */
.left-col {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-self: start;
}

/* Mannequin column */
.mannequin-col {
  padding: 0.875rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  flex-grow: 1;
}

/* Guide card — full width horizontal strip */
.guide-card {
  padding: 0.875rem 1.25rem;
}

.guide-title {
  font-size: 14px;
  font-weight: 700;
  color: #2d7a3a;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  margin: 0 0 8px;
}

.guide-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.guide-list--row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px 16px;
}

.guide-list li {
  font-size: 15px;
  color: #6b6560;
  line-height: 1.5;
  padding-left: 13px;
  position: relative;
}

.guide-list li::before {
  content: '';
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #4d9e5a;
  position: absolute;
  left: 0;
  top: 6px;
}

.col-label {
  font-size: 14px;
  font-weight: 700;
  color: #9e9890;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin: 0;
}

.mannequin-svg {
  width: 100%;
  max-width: 120px;
}

/* Score display */
.score-area {
  width: 100%;
  margin-top: 4px;
  padding-top: 8px;
  border-top: 1px solid #d8eae6;
}

.score-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 4px;
}

.score-lbl {
  font-size: 14px;
  color: #9e9890;
}

.score-val {
  font-size: 1rem;
  font-weight: 800;
  transition: color 0.4s;
}

.score-bar-bg {
  height: 7px;
  background: #e8f0ee;
  border-radius: 4px;
  overflow: hidden;
  margin: 4px 0;
}

.score-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition:
    width 0.5s ease,
    background-color 0.4s;
}

@keyframes bar-pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.score-bar-fill--pulse {
  animation: bar-pulse 1.1s infinite;
}

.score-status {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.4;
  margin: 0;
  transition: color 0.4s;
}

/* Items column */
.items-col {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* Navigation links at bottom of items-col */
.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0.9rem 1rem;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  transition:
    filter 0.15s,
    transform 0.1s;
  letter-spacing: 0.02em;
}

.nav-link-btn:active {
  transform: scale(0.98);
}

.nav-link-btn:nth-child(1) {
  background: #2d7a3a;
  color: #ffffff;
  border: none;
}

.nav-link-btn:nth-child(1):hover {
  filter: brightness(1.12);
}

.nav-link-btn:nth-child(2) {
  background: #185fa5;
  color: #ffffff;
  border: none;
}

.nav-link-btn:nth-child(2):hover {
  filter: brightness(1.15);
}

.section-label {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  margin: 0;
  padding-top: 4px;
}

.section-label--good {
  color: #2d7a3a;
}

.section-label--bad {
  color: #c0392b;
  margin-top: 6px;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

/* Advice card */
.advice-card {
  padding: 1rem 1.125rem;
}

.advice-title {
  font-size: 15px;
  font-weight: 700;
  color: #2d7a3a;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  margin: 0 0 8px;
}

.advice-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.advice-item {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}

.advice-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 5px;
}

.advice-text {
  font-size: 14px;
  line-height: 1.55;
  color: #1a1714;
}

/* Status messages */
.status-msg {
  text-align: center;
  padding: 3rem 0;
  color: #6b6560;
  font-size: 1rem;
}

.status-msg--error {
  color: #c0392b;
}

/* Responsive */
@media (max-width: 600px) {
  .main-grid {
    grid-template-columns: 1fr;
  }

  .left-col {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .mannequin-col {
    flex: 1;
    min-width: 140px;
    flex-direction: row;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .guide-card {
    flex: 1;
    min-width: 140px;
  }

  .mannequin-svg {
    max-width: 100px;
  }

  .score-area {
    flex: 1;
    border-top: none;
    border-left: 1px solid #d8eae6;
    padding-top: 0;
    padding-left: 1rem;
    margin-top: 0;
  }
}
</style>
