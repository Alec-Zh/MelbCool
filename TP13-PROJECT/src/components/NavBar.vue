<script setup>
import { ref } from 'vue'
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
    <div class="header-container">
      <RouterLink to="/" class="brand" @click="closeMenu">
        <img src="/logo.png" alt="MelbCool Melbourne" class="logo" />
        <span class="brand-name">MelbCool</span>
      </RouterLink>

      <nav class="nav">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/heatmap" class="nav-link">Heat Map</RouterLink>
        <RouterLink to="/trip-coach" class="nav-link">Trip Coach</RouterLink>
      </nav>

      <button class="hamburger" @click="toggleMenu" aria-label="Toggle menu">
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
      </button>
    </div>

    <div class="mobile-menu" :class="{ active: menuOpen }">
      <RouterLink to="/" class="mobile-link" @click="closeMenu">Home</RouterLink>
      <RouterLink to="/heatmap" class="mobile-link" @click="closeMenu">Heat Map</RouterLink>
      <RouterLink to="/trip-coach" class="mobile-link" @click="closeMenu">Trip Coach</RouterLink>
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
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  height: 72px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  flex-shrink: 0;
}
.brand-name {
  color: var(--color-primary);
  font-weight: bold;
  font-size: 17px;
}
.logo {
  height: 48px;
  width: auto;
  object-fit: contain;
}
.nav {
  display: flex;
  gap: 2rem;
  align-items: center;
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
@media (max-width: 768px) {
  .nav {
    display: none;
  }
  .hamburger {
    display: flex;
  }
}
</style>
