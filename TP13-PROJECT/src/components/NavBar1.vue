
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
<header class="mh-nav" id="mhNav">
    <div class="mh-nav-inner">
      <a class="mh-brand" href="/">
        <img src="/logo-mark-transparent.png" alt="MelbCool" />
        <span>MelbCool</span>
      </a>
      <nav class="mh-links" aria-label="Main navigation">
        <RouterLink to="/" exact-active-class="active">Home</RouterLink>
        <RouterLink to="/heatmap" exact-active-class="active">Heat Map</RouterLink>
        <RouterLink to="/cool-refuges" exact-active-class="active">Cool Refuges</RouterLink>
        <RouterLink to="/trip-coach" exact-active-class="active">Trip Coach</RouterLink>
        <!-- <RouterLink to="/clothing-recommendations">Clothing</RouterLink> -->
        <RouterLink to="/safety-plan" exact-active-class="active">Safety Plan</RouterLink>
      </nav>
      <a class="mh-nav-cta" href="/safety-plan">Plan Today ↗</a>
    </div>
  </header>
</template>


