<script setup>
import { ref } from 'vue'
import BackToTop from './components/BackToTop.vue'
import PasswordGate from './components/PasswordGate.vue'

const unlocked = ref(sessionStorage.getItem('melbcool_access') === 'true')
</script>

<template>
  <PasswordGate v-if="!unlocked" @unlocked="unlocked = true" />
  <template v-else>
    <RouterView />
    <BackToTop />
  </template>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans',
    'Helvetica Neue', sans-serif;
}
</style>
