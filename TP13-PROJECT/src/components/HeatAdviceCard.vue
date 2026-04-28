<script setup>
import { computed } from 'vue'

const props = defineProps({
  riskLevel: { type: String, required: true },
  heatScore: { type: Number, default: 0 },
  shadeScore: { type: Number, default: 0 },
})

const emit = defineEmits(['close'])

// Determine the primary driver of risk
// shade_score raw value: higher = less shade = more dangerous
const riskDriver = computed(() => {
  const heatHigh = props.heatScore >= 65
  const shadeHigh = props.shadeScore >= 65
  if (heatHigh && shadeHigh) return 'both'
  if (heatHigh) return 'heat'
  if (shadeHigh) return 'shade'
  return 'combined'
})

// Dynamic title
const dynamicTitle = computed(() => {
  if (props.riskLevel === 'high') {
    if (riskDriver.value === 'shade') return 'High risk — limited shade'
    if (riskDriver.value === 'heat') return 'High risk — extreme heat'
    if (riskDriver.value === 'both') return 'High risk — heat and shade'
    return 'High risk area'
  }
  if (props.riskLevel === 'moderate') {
    if (riskDriver.value === 'shade') return 'Caution — limited shade'
    if (riskDriver.value === 'heat') return 'Caution — elevated heat'
    return 'Take care outdoors'
  }
  return 'Conditions look safe'
})

// Dynamic summary
const dynamicSummary = computed(() => {
  const level = props.riskLevel
  const driver = riskDriver.value

  if (level === 'low') {
    return 'Overall conditions in this area are currently manageable. Stay hydrated and take basic precautions if spending extended time outdoors.'
  }
  if (level === 'moderate') {
    if (driver === 'heat')
      return 'Temperatures in this area are elevated. Avoid strenuous activity during the hottest part of the day (11am–3pm).'
    if (driver === 'shade')
      return 'This area has limited tree shade, increasing sun exposure risk. Seek shaded spots and protect yourself from direct sunlight.'
    if (driver === 'both')
      return 'This area has elevated temperatures and limited tree shade. Take extra care when spending time outdoors.'
    return 'Combined heat and shade conditions in this area require some caution when spending time outdoors.'
  }
  if (level === 'high') {
    if (driver === 'heat')
      return 'Temperatures in this area are dangerously high. Limit time outdoors and seek cool, air-conditioned shelter immediately if feeling unwell.'
    if (driver === 'shade')
      return 'This area has very little tree shade, posing a serious sun exposure and heat risk. Avoid prolonged outdoor activity, especially during peak UV hours.'
    if (driver === 'both')
      return 'This area has dangerously high temperatures and very limited tree shade. Avoid going outside where possible and seek cool shelter.'
    return 'Combined conditions in this area pose a significant risk. Limit outdoor time and take all available precautions.'
  }
  return 'Take care when spending time outdoors in this area.'
})

// Dynamic tips
const dynamicTips = computed(() => {
  const level = props.riskLevel
  const driver = riskDriver.value

  const tips = {
    water: 'Drink water regularly — do not wait until you feel thirsty.',
    waterFreq: 'Drink cool water frequently — at least every 30 minutes when outdoors.',
    hat: 'Wear a hat and apply sunscreen before going outside.',
    sunscreen: 'Apply SPF 50+ sunscreen and reapply every 2 hours if outdoors.',
    shade: 'Seek shaded areas, trees, or covered walkways when outdoors.',
    lightCloth: 'Wear light, loose-fitting clothing to reduce heat absorption.',
    ac: 'Stay in air-conditioned spaces where possible.',
    avoidPeak: 'Avoid being outdoors between 11am and 3pm.',
    avoidAll: 'Avoid going outside between 11am and 4pm if possible.',
    checkIn: 'Check in on elderly neighbours or family members.',
    heatStroke:
      'Call 000 immediately if someone shows signs of heat stroke: confusion, no sweating, very hot skin.',
    alerts: 'Check the Victorian Government heat health alerts for the latest updates.',
    heatSigns: 'Watch for signs of heat stress: dizziness, nausea, or heavy sweating.',
  }

  if (level === 'low') {
    return [tips.water, tips.hat, tips.checkIn]
  }
  if (level === 'moderate') {
    if (driver === 'shade')
      return [tips.shade, tips.sunscreen, tips.hat, tips.waterFreq, tips.avoidPeak]
    if (driver === 'heat') return [tips.ac, tips.waterFreq, tips.avoidPeak, tips.heatSigns]
    return [tips.shade, tips.ac, tips.waterFreq, tips.avoidPeak, tips.heatSigns]
  }
  if (level === 'high') {
    if (driver === 'shade')
      return [
        tips.shade,
        tips.sunscreen,
        tips.lightCloth,
        tips.waterFreq,
        tips.avoidAll,
        tips.heatStroke,
        tips.alerts,
      ]
    if (driver === 'heat')
      return [tips.ac, tips.waterFreq, tips.avoidAll, tips.heatStroke, tips.alerts]
    return [tips.ac, tips.shade, tips.waterFreq, tips.avoidAll, tips.heatStroke, tips.alerts]
  }
  return [tips.water, tips.hat]
})

// Static style config per risk level
const styleMap = {
  low: {
    icon: '✅',
    decision: 'Safe to go outside',
    decisionBg: '#dcfce7',
    decisionColour: '#166534',
    colour: '#166534',
    bg: '#f0fdf4',
    border: '#bbf7d0',
  },
  moderate: {
    icon: '⚠️',
    decision: 'Go outside with caution',
    decisionBg: '#fef3c7',
    decisionColour: '#92400E',
    colour: '#92400E',
    bg: '#fffbeb',
    border: '#fde68a',
  },
  high: {
    icon: '🚨',
    decision: 'Avoid going outside',
    decisionBg: '#fee2e2',
    decisionColour: '#991B1B',
    colour: '#991B1B',
    bg: '#fff5f5',
    border: '#fecaca',
  },
}

const style = computed(() => styleMap[props.riskLevel] ?? styleMap['low'])
</script>

<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div class="modal-backdrop" @click.self="emit('close')">
        <div
          class="modal"
          :style="{ borderColor: style.border, backgroundColor: style.bg }"
          role="dialog"
          aria-modal="true"
          :aria-label="`Safety advice: ${dynamicTitle}`"
        >
          <!-- Close -->
          <button class="modal-close" @click="emit('close')" aria-label="Close advice">
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

          <!-- Header -->
          <div class="modal-header">
            <span class="modal-icon">{{ style.icon }}</span>
            <h3 class="modal-title" :style="{ color: style.colour }">{{ dynamicTitle }}</h3>
          </div>

          <!-- Summary -->
          <p class="modal-summary">{{ dynamicSummary }}</p>

          <!-- AC3.2.2 — Decision label -->
          <div
            class="decision-label"
            :style="{ backgroundColor: style.decisionBg, color: style.decisionColour }"
          >
            <span class="decision-dot" :style="{ backgroundColor: style.decisionColour }"></span>
            {{ style.decision }}
          </div>

          <!-- Tips -->
          <div class="modal-tips">
            <div class="tips-heading">What should you do?</div>
            <ul class="tips-list">
              <li v-for="tip in dynamicTips" :key="tip">{{ tip }}</li>
            </ul>
          </div>

          <!-- Source -->
          <a
            href="https://www.betterhealth.vic.gov.au/health/healthyliving/how-to-cope-and-stay-safe-in-extreme-heat"
            target="_blank"
            rel="noopener noreferrer"
            class="modal-source"
          >
            Source: Victorian Government Better Health Channel ↗
          </a>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1.5rem;
}

.modal {
  position: relative;
  width: 100%;
  max-width: 440px;
  border: 1.5px solid;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.18);
  max-height: 90vh;
  overflow-y: auto;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid rgba(0, 0, 0, 0.12);
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #555;
  transition: background 0.15s;
}
.modal-close:hover {
  background: #fff;
  color: #111;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding-right: 2rem;
}

.modal-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.modal-title {
  font-size: 1.1rem;
  font-weight: 700;
  line-height: 1.3;
  margin: 0;
}

.modal-summary {
  font-size: 0.92rem;
  color: #374151;
  line-height: 1.6;
  margin: 0;
}

.decision-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.55rem 0.9rem;
  border-radius: 8px;
  font-size: 0.92rem;
  font-weight: 700;
}

.decision-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.modal-tips {
  background: rgba(255, 255, 255, 0.65);
  border-radius: 10px;
  padding: 0.9rem 1rem;
}

.tips-heading {
  font-size: 0.82rem;
  font-weight: 700;
  color: #111;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.6rem;
}

.tips-list {
  margin: 0;
  padding-left: 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.tips-list li {
  font-size: 0.9rem;
  color: #374151;
  line-height: 1.55;
}

.modal-source {
  font-size: 0.78rem;
  color: #1d4ed8;
  text-decoration: none;
  padding-top: 0.25rem;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}
.modal-source:hover {
  text-decoration: underline;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-active .modal,
.modal-fade-leave-active .modal {
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}
.modal-fade-enter-from {
  opacity: 0;
}
.modal-fade-enter-from .modal {
  transform: translateY(12px);
  opacity: 0;
}
.modal-fade-leave-to {
  opacity: 0;
}
</style>
