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
        <RouterLink to="/cool-refuges" class="nav-link">Cool Refuges</RouterLink>
        <RouterLink to="/trip-coach" class="nav-link">Trip Coach</RouterLink>
        <RouterLink to="/outfit-advisor" class="nav-link">Outfit Advisor</RouterLink>
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
      <RouterLink to="/cool-refuges" class="mobile-link" @click="closeMenu"
        >Cool Refuges</RouterLink
      >
      <RouterLink to="/trip-coach" class="mobile-link" @click="closeMenu">Trip Coach</RouterLink>
      <RouterLink to="/outfit-advisor" class="mobile-link" @click="closeMenu"
        >Outfit Advisor</RouterLink
      >
    </div>
  </header>
</template>

<style scoped>
.header {
  background: #ffffff;
  border-bottom: 1px solid #e3ded5;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 0 #e3ded5;
}
.header-container {
  max-width: var(--max-width);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  height: 64px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  flex-shrink: 0;
}
.brand-name {
  color: #1a1714;
  font-weight: 700;
  font-size: 17px;
  letter-spacing: 0.02em;
}
.logo {
  height: 38px;
  width: auto;
  object-fit: contain;
}
.nav {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}
.nav-link {
  text-decoration: none;
  color: #6b6560;
  font-size: 0.9rem;
  font-weight: 500;
  padding: 0.4rem 0.9rem;
  border-radius: 6px;
  transition:
    color 0.2s,
    background 0.2s;
  white-space: nowrap;
  letter-spacing: 0.01em;
}
.nav-link:hover {
  color: #1a1714;
  background: rgba(13, 212, 191, 0.06);
}
.nav-link.router-link-active {
  color: #2d7a3a;
  background: rgba(45, 122, 58, 0.09);
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
  width: 22px;
  height: 2px;
  background-color: #6b6560;
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
  border-top: 1px solid #e3ded5;
  gap: 0.25rem;
  background: #ffffff;
}
.mobile-menu.active {
  display: flex;
}
.mobile-link {
  text-decoration: none;
  color: #6b6560;
  font-size: 1rem;
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #e3ded5;
  transition: color 0.2s;
}
.mobile-link:hover,
.mobile-link.router-link-active {
  color: #2dd4bf;
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
