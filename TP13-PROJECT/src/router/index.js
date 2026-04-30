import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import HeatMapPage from '../views/HeatMapPage.vue'
import CoolRefugePage from '../views/CoolRefugePage.vue'
import TripCoachPage from '../views/TripCoachPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomePage },
    { path: '/heatmap', component: HeatMapPage },
    { path: '/cool-refuges', component: CoolRefugePage },
    { path: '/trip-coach', component: TripCoachPage },
  ],
})

export default router