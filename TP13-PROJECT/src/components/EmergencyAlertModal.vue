<script setup>
defineProps({
  show: {
    type: Boolean,
    required: true
  }
});

defineEmits(['close']);
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <div class="emergency-title">
          <span class="warning-icon">⚠️</span>
          EMERGENCY BROADCAST
        </div>
        <button class="modal-close" @click="$emit('close')">×</button>
      </div>
      
      <div class="modal-body">
        <h2 class="alert-title">Severe Heat Alert: Melbourne Metropolitan Area</h2>
        
        <div class="risk-level">
          <span class="risk-icon">!</span>
          Level 4: Extreme Risk
        </div>
        
        <p class="alert-description">
          Avoid outdoor activities between 11 AM and 6 PM. Stay hydrated and check on vulnerable neighbors. Use cooling centers if your home temperature exceeds 30°C.
        </p>
        
        <div class="modal-buttons">
          <button class="btn-guidelines" @click="$emit('close')">
            View Safety Guidelines
          </button>
          <button class="btn-dismiss" @click="$emit('close')">
            Dismiss
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background-color: white;
  border-radius: 16px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  animation: slideUp 0.3s ease;
}

.modal-header {
  background-color: #dc2626;
  color: white;
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.emergency-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
  font-size: 1.1rem;
  letter-spacing: 0.5px;
}

.warning-icon {
  font-size: 1.25rem;
}

.modal-close {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  font-size: 1.5rem;
  font-weight: 300;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
}

.modal-close:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.modal-body {
  padding: 2rem;
}

.alert-title {
  color: #1e40af;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
  text-align: center;
  line-height: 1.3;
}

.risk-level {
  background-color: #fecdd3;
  color: #be123c;
  padding: 0.75rem 1.25rem;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  justify-content: center;
}

.risk-icon {
  background-color: #be123c;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 0.9rem;
}

.alert-description {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 2rem;
  font-size: 1rem;
}

.modal-buttons {
  display: flex;
  gap: 1rem;
}

.btn-guidelines {
  flex: 1;
  background-color: #1e40af;
  color: white;
  border: 2px dashed #3b82f6;
  padding: 1rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-guidelines:hover {
  background-color: #1e3a8a;
  transform: translateY(-2px);
}

.btn-dismiss {
  flex: 1;
  background-color: #f3f4f6;
  color: #4b5563;
  border: none;
  padding: 1rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-dismiss:hover {
  background-color: #e5e7eb;
  transform: translateY(-2px);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
