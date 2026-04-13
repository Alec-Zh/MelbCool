<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const showBackToTop = ref(false)

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  })
}

const handleScroll = () => {
  showBackToTop.value = window.scrollY > 300
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <button
    v-if="showBackToTop"
    class="back-to-top"
    @click="scrollToTop"
    aria-label="Back to top"
  >
    ↑
  </button>
</template>

<style scoped>
.back-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background-color: #0d3a8f;
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(13, 58, 143, 0.3);
  transition: all 0.3s ease;
  z-index: 99;
  border: none;
}

.back-to-top:hover {
  background-color: #1a4bb8;
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(13, 58, 143, 0.4);
}

.back-to-top:active {
  transform: translateY(0);
}
</style>
