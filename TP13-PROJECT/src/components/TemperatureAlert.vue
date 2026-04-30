<script setup>
import { computed } from 'vue'

const props = defineProps({
  temperature: {
    type: Number,
    required: true
  },
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

// 根据温度获取状态信息
const tempStatus = computed(() => {
  const temp = props.temperature
  if (temp < 25) {
    return {
      level: 'Low Risk',
      color: '#16a34a',
      bgColor: '#f0fdf4',
      borderColor: '#86efac',
      icon: '✓',
      description: 'Low heat risk. Conditions are suitable for travel—enjoy your day with standard precautions.'
    }
  } else if (temp < 35) {
    return {
      level: 'Moderate Risk',
      color: '#ca8a04',
      bgColor: '#fefce8',
      borderColor: '#fde047',
      icon: '⚠',
      description: 'Moderate heat risk. Travel is possible, but limit time outdoors. Stay hydrated and use shaded paths or nearby cool places to rest.'
    }
  } else {
    return {
      level: 'High Risk',
      color: '#dc2626',
      bgColor: '#fef2f2',
      borderColor: '#fca5a5',
      icon: '!',
      description: 'High heat risk. Avoid going outdoors. Stay in cool environments, keep hydrated, and seek nearby Cool Refuges if needed.'
    }
  }
})

const closeAlert = () => {
  emit('close')
}
</script>

<template>
  <Transition name="slide-up">
    <div v-if="show" class="temperature-alert" :style="{
      backgroundColor: tempStatus.bgColor,
      borderColor: tempStatus.borderColor
    }">
      <button class="close-btn" @click="closeAlert">×</button>
      
      <div class="alert-header">
        <span class="status-icon" :style="{ color: tempStatus.color }">
          {{ tempStatus.icon }}
        </span>
        <span class="status-level" :style="{ color: tempStatus.color }">
          {{ tempStatus.level }}
        </span>
        <span class="temp-icon">🌡️</span>
      </div>
      
      <div class="temperature-value" :style="{ color: tempStatus.color }">
        {{ temperature.toFixed(1) }}°C
      </div>
      
      <p class="description">
        {{ tempStatus.description }}
      </p>
    </div>
  </Transition>
</template>

<style scoped>
.temperature-alert {
  position: absolute;
  bottom: 20px;
  left: 20px;
  width: 320px;
  padding: 20px;
  border-radius: 12px;
  border: 2px solid;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.close-btn {
  position: absolute;
  top: 8px;
  right: 12px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #666;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.alert-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.status-icon {
  font-size: 16px;
  font-weight: bold;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  border: 2px solid currentColor;
}

.status-level {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
  flex: 1;
}

.temp-icon {
  font-size: 20px;
  opacity: 0.6;
}

.temperature-value {
  font-size: 48px;
  font-weight: 300;
  line-height: 1;
  margin-bottom: 12px;
}

.description {
  font-size: 13px;
  line-height: 1.5;
  color: #374151;
  margin: 0;
}

/* 动画效果 */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 响应式 */
@media (max-width: 480px) {
  .temperature-alert {
    width: calc(100% - 40px);
    left: 20px;
    right: 20px;
    bottom: 20px;
  }
}
</style>