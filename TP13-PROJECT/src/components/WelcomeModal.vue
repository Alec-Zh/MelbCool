<script setup>
import { ref, onMounted } from 'vue'

const showModal = ref(false)

onMounted(() => {
  // 每次进入页面都显示弹窗
  showModal.value = true
})

const closeModal = () => {
  showModal.value = false
}
</script>

<template>
  <div v-if="showModal" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <button class="close-btn" @click="closeModal">×</button>
      
      <div class="modal-header">
        <span class="welcome-icon">❄️</span>
        <h2 class="modal-title">Welcome to Cool Refuges</h2>
      </div>
      
      <div class="modal-body">
        <p class="description">
          Find safe, air-conditioned public spaces near you to escape the summer heat. 
          This page helps you locate:
        </p>
        
        <!-- <ul class="feature-list">
          <li>
            <span class="feature-icon">📚</span>
            <span class="feature-text"><strong>Libraries</strong> - Quiet spaces with free WiFi and books</span>
          </li>
          <li>
            <span class="feature-icon">🏛️</span>
            <span class="feature-text"><strong>Museums</strong> - Cool cultural spaces to explore</span>
          </li>
          <li>
            <span class="feature-icon">🌳</span>
            <span class="feature-text"><strong>Parks</strong> - Shaded outdoor areas with water facilities</span>
          </li>
          <li>
            <span class="feature-icon">🏘️</span>
            <span class="feature-text"><strong>Community Centers</strong> - Local gathering spaces with AC</span>
          </li>
          <li>
            <span class="feature-icon">🛍️</span>
            <span class="feature-text"><strong>Shopping Centers</strong> - Accessible cooling spaces</span>
          </li>
        </ul> -->
        
        <div class="tips-section">
          <h3 class="tips-title">💡 Quick Tips:</h3>
          <ul class="tips-list">
            <li>Use the search bar to find refuges by suburb or landmark</li>
            <li>Filter by type to find the perfect spot for you</li>
            <li>Switch to Map view to see nearby locations</li>
            <li>Click "Get Directions" for turn-by-turn navigation</li>
          </ul>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn-got-it" @click="closeModal">Got it!</button>
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
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background-color: #ffffff;
  border-radius: 20px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: #f0f0f0;
  color: #333;
}

.modal-header {
  text-align: center;
  padding: 2rem 2rem 1rem;
  background: linear-gradient(135deg, #0d3a8f 0%, #1e4a9e 100%);
  color: white;
  border-radius: 20px 20px 0 0;
}

.welcome-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 0.5rem;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.modal-body {
  padding: 1.5rem 2rem;
}

.description {
  font-size: 1rem;
  color: #333;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem 0;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background-color: #f8f9ff;
  border-radius: 12px;
  margin-bottom: 0.5rem;
  transition: background-color 0.2s ease;
}

.feature-list li:hover {
  background-color: #eef1ff;
}

.feature-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.feature-text {
  font-size: 0.95rem;
  color: #333;
}

.tips-section {
  background-color: #f0fdf4;
  border-radius: 12px;
  padding: 1rem;
  border-left: 4px solid #22c55e;
}

.tips-title {
  font-size: 1rem;
  font-weight: 700;
  color: #166534;
  margin: 0 0 0.75rem 0;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tips-list li {
  font-size: 0.9rem;
  color: #333;
  padding: 0.25rem 0;
  padding-left: 1.2rem;
  position: relative;
}

.tips-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #22c55e;
  font-weight: bold;
}

.modal-footer {
  padding: 1rem 2rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.btn-got-it {
  background-color: #0d3a8f;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-got-it:hover {
  background-color: #1a4bb8;
  transform: translateY(-2px);
}

.btn-dont-show {
  background: none;
  border: none;
  color: #666;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.2s ease;
}

.btn-dont-show:hover {
  color: #333;
  text-decoration: underline;
}

@media (max-width: 480px) {
  .modal-content {
    margin: 0.5rem;
  }
  
  .modal-header {
    padding: 1.5rem 1.5rem 1rem;
  }
  
  .modal-body {
    padding: 1rem 1.5rem;
  }
  
  .modal-footer {
    padding: 1rem 1.5rem 1.5rem;
  }
}
</style>