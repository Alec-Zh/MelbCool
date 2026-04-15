<script setup>
import { ref } from 'vue'
// import AlertModal from './AlertModal.vue'  // Iteration 2
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
    <!-- <AlertModal :show="showAlertModal" @close="showAlertModal = false" /> -->
    <div class="header-container">
      <!-- Logo → home -->
      <RouterLink to="/" class="brand" @click="closeMenu">
        <span class="brand-name">CoolPath</span>
        <img src="/logo.png" alt="CoolPath Melbourne" class="logo" />
      </RouterLink>

      <!-- Desktop nav — centred -->
      <nav class="nav">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/heatmap" class="nav-link">HeatMap</RouterLink>
        <!-- <RouterLink to="/cool-refuges" class="nav-link">Cool Refuges</RouterLink> -->
        <!-- Iteration 2 -->
      </nav>

      <!-- Right slot kept for layout balance; Get Alerts is Iteration 2 -->
      <div class="nav-right">
        <!-- <button class="btn-alerts" @click="showAlertModal = true">Get Alerts</button> -->
      </div>

      <!-- Hamburger (mobile) -->
      <button class="hamburger" @click="toggleMenu" aria-label="Toggle menu">
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
      </button>
    </div>

    <!-- Mobile dropdown -->
    <div class="mobile-menu" :class="{ active: menuOpen }">
      <RouterLink to="/" class="mobile-link" @click="closeMenu">Home</RouterLink>
      <RouterLink to="/heatmap" class="mobile-link" @click="closeMenu">HeatMap</RouterLink>
      <!-- <RouterLink to="/cool-refuges" class="mobile-link" @click="closeMenu">Cool Refuges</RouterLink> -->
      <!-- Iteration 2 -->
      <!-- <button class="btn-alerts mobile-btn" @click="showAlertModal = true">Get Alerts</button> -->
      <!-- Iteration 2 -->
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
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 0 2rem;
  height: 64px;
}

/* Brand / Logo — left */
.brand {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  text-decoration: none;
  justify-self: start;
  min-width: 0;
}

.brand-name {
  color: var(--color-primary);
  font-weight: bold;
  font-size: 20px;
}

.logo {
  height: 32px;
  width: auto;
  object-fit: contain;
}

/* Desktop nav — centre */
.nav {
  display: flex;
  gap: 2rem;
  justify-self: center;
}

.nav-link {
  text-decoration: none;
  color: var(--color-text-muted);
  font-size: 1rem;
  padding: 0.5rem 0;
  transition: color 0.3s ease;
  white-space: nowrap;
}

.nav-link:hover {
  color: var(--color-primary);
}

.nav-link.router-link-active {
  color: var(--color-primary);
  border-bottom: 2px solid var(--color-primary);
}

/* Right slot — keeps grid balanced */
.nav-right {
  justify-self: end;
  display: flex;
  align-items: center;
}

/* Hamburger button */
.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  grid-column: 3;
  justify-self: end;
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

/* Mobile menu */
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

/* ≤ 768px: switch to mobile layout */
@media (max-width: 768px) {
  .header-container {
    grid-template-columns: 1fr auto;
  }

  .nav {
    display: none;
  }

  .nav-right {
    display: none;
  }

  .hamburger {
    display: flex;
    grid-column: 2;
  }
}
</style>
