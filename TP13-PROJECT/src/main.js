import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import './assets/main.css'
import { hoverScale } from './directives/hoverScale.js'

const app = createApp(App)
app.use(router)
app.directive('hover-scale', hoverScale)
app.mount('#app')
