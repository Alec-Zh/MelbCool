<script setup>
import { ref } from 'vue'
import AlertModal from './AlertModal.vue';
const showAlertModal = ref(false);
const menuOpen = ref(false)
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}
const closeMenu = () => {
  menuOpen.value = false
}
</script>

<template>
  <header class="header">
    <AlertModal :show="showAlertModal" @close="showAlertModal = false" />
    <div class="header-container">
      <!-- Logo → 主页 -->
      <RouterLink to="/" class="brand" @click="closeMenu">
        <span class="brand-name">CoolPath</span>
        <img src="/logo.png" alt="CoolPath Melbourne" class="logo" />
      </RouterLink>

      <!-- 桌面端导航 -->
      <nav class="nav">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/heatmap" class="nav-link">HeatMap</RouterLink>
        <RouterLink to="/cool-refuges" class="nav-link">Cool Refuges</RouterLink>
      </nav>

      <button class="btn-alerts desktop-only" @click="showAlertModal = true">Get Alerts</button>

      <!-- 汉堡按钮（移动端） -->
      <button class="hamburger" @click="toggleMenu" aria-label="Toggle menu">
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
      </button>
    </div>

    <!-- 移动端下拉菜单 -->
    <div class="mobile-menu" :class="{ active: menuOpen }">
      <RouterLink to="/" class="mobile-link" @click="closeMenu">Home</RouterLink>
      <RouterLink to="/heatmap" class="mobile-link" @click="closeMenu">HeatMap</RouterLink>
      <RouterLink to="/cool-refuges" class="mobile-link" @click="closeMenu"
        >Cool Refuges</RouterLink
      >
      <button class="btn-alerts mobile-btn" @click="showAlertModal = true">Get Alerts</button>
    </div>
  </header>
</template>

<style scoped>
.header {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  max-width: var(--max-width);
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  height: 64px;
}

/* Brand / Logo */
.brand {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  text-decoration: none;
}

.brand-name {
  color: var(--color-primary);
  font-weight: bold;
  font-size: 20px;
}

.logo {
  width: 120px;
  object-fit: contain;
}

/* 桌面端导航 */
.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: var(--color-text-muted);
  font-size: 1rem;
  padding: 0.5rem 0;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: var(--color-primary);
}

.nav-link.router-link-active {
  color: var(--color-primary);
  border-bottom: 2px solid var(--color-primary);
}

/* 汉堡按钮 */
.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.hamburger span {
  display: block;
  width: 24px;
  height: 2px;
  background-color: var(--color-primary);
  transition: all 0.3s ease;
  transform-origin: center;
}

.hamburger span.open:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.hamburger span.open:nth-child(2) {
  opacity: 0;
}

.hamburger span.open:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* 移动端菜单 */
.mobile-menu {
  display: none;
  flex-direction: column;
  padding: 1rem 2rem 1.5rem;
  border-top: 1px solid var(--color-border);
  gap: 0.5rem;
}

.mobile-menu.active {
  display: flex;
}

.mobile-link {
  text-decoration: none;
  color: var(--color-text-muted);
  font-size: 1rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f0f0f0;
  transition: color 0.3s ease;
}

.mobile-link:hover,
.mobile-link.router-link-active {
  color: var(--color-primary);
}

.mobile-btn {
  margin-top: 0.75rem;
  width: 100%;
}

/* 断点：768px 以下切换到移动端 */
@media (max-width: 768px) {
  .nav {
    display: none;
  }

  .desktop-only {
    display: none;
  }

  .hamburger {
    display: flex;
  }
}
</style>
