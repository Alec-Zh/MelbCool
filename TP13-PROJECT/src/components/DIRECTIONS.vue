<template>
  <div class="directions-overlay" @click.self="$emit('close')">
    <div class="directions-modal">
      <div class="directions-header">
        <h2>Route Directions</h2>
        <button class="close-btn" @click="$emit('close')">×</button>
      </div>
      
      <div class="directions-content">
        <!-- 温度预警 -->
        <TemperatureAlert
          v-if="props.showTempAlert && currentTemp !== null"
          :temperature="currentTemp"
          :show="props.showTempAlert"
          @close="$emit('close')"
          class="directions-temp-alert"
        />
        <!-- 顶部区域：路线信息、交通方式和路线统计并排 -->
        <div class="top-section">
          <!-- 起点和终点信息 + 路线统计 -->
          <div class="route-info">
            <div class="location-item origin">
              <div class="location-icon">📍</div>
              <div class="location-details">
                <span class="location-label">From</span>
                <span class="location-name">{{ originName }}</span>
              </div>
            </div>
            <div class="route-arrow">→</div>
            <div class="location-item destination">
              <div class="location-icon-img">
                <img :src="mapPhotoObj[refuge?.type || 'library']" alt="destination" />
              </div>
              <div class="location-details">
                <span class="location-label">To</span>
                <span class="location-name">{{ refuge?.name }}</span>
              </div>
            </div>
            <!-- 路线统计 -->
            <div class="route-stats-inline" v-if="routeInfo">
              <div class="stat-divider"></div>
              <div class="stat-item-inline">
                <span class="stat-value-inline">{{ routeInfo.distance }}</span>
                <span class="stat-label-inline">Distance</span>
              </div>
              <div class="stat-item-inline">
                <span class="stat-value-inline">{{ routeInfo.duration }}</span>
                <span class="stat-label-inline">Time</span>
              </div>
            </div>
          </div>
          
          <!-- 交通方式选择 -->
          <div class="transport-modes">
            <button 
              v-for="mode in transportModes" 
              :key="mode.value"
              class="mode-btn"
              :class="{ active: selectedMode === mode.value }"
              @click="switchMode(mode.value)"
            >
              <span class="mode-icon">{{ mode.icon }}</span>
              <span class="mode-label">{{ mode.label }}</span>
            </button>
          </div>
        </div>
        
        <!-- 地图容器 -->
        <div class="map-wrapper">
          <div ref="mapContainer" class="directions-map"></div>
          
          <!-- 终点详情卡片 -->
          <div v-if="showDetailCard" class="map-detail-card">
            <button class="close-btn" @click="showDetailCard = false">×</button>
            <div class="detail-image">
              <img :src="photoObj[refuge?.type]" :alt="refuge?.name" />
              <span class="open-badge" :class="{ closed: !isOpenNow(refuge?.type) }">
                {{ isOpenNow(refuge?.type) ? 'OPEN NOW' : 'CLOSED' }}
              </span>
            </div>
            <div class="detail-content">
              <h3 class="detail-name">{{ refuge?.name }}</h3>
              <p class="detail-address">
                <span v-if="distanceText">{{ distanceText }} • </span>
                {{ refuge?.street }}, {{ refuge?.city }}
              </p>
              
              <div class="detail-hours">
                <div class="hours-icon">🕐</div>
                <div class="hours-text">
                  <span class="hours-label">FULL HOURS</span>
                  <span class="hours-value">Open today: {{ openingHoursObj[refuge?.type] }}</span>
                </div>
              </div>
              
              <div class="detail-facilities">
                <div v-for="(facility, index) in getFacilities(refuge?.type)" :key="index" class="facility-item">
                  <span class="facility-icon">{{ facility.icon }}</span>
                  <span class="facility-name">{{ facility.name }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 路线步骤 -->
        <div class="route-steps" v-if="steps.length > 0">
          <h3>Step by Step</h3>
          <div class="step-list">
            <div v-for="(step, index) in steps" :key="index" class="step-item">
              <span class="step-number">{{ index + 1 }}</span>
              <span class="step-text">{{ step }}</span>
            </div>
          </div>
        </div>
        
       
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import TemperatureAlert from '@/components/TemperatureAlert.vue'

const props = defineProps({
  refuge: {
    type: Object,
    required: true
  },
  userLocation: {
    type: Object,
    default: null
  },
  showTempAlert: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const mapContainer = ref(null)
let map = null

const routeInfo = ref(null)
const steps = ref([])
const selectedMode = ref('driving')
const showDetailCard = ref(false)
const currentTemp = ref(0)

// 封面图片配置
const photoObj = {
  library: '/libraryCover.jpg',
  museum: '/museumCover.jpg',
  park: '/parkCover.jpg',
  community: '/communityCover.jpg',
  shopping: '/shoppingCover.jpg'
}

// 设施配置
const facilitiesObj = {
  library: '❄️  🛜  ☕️',
  museum: '🚻  🛜  ☕️',
  park: '🚻  🅿️ 💧',
  community: '🛜  ☕️  🅿️',
  shopping: '❄️  🛜  🚻'
}

// 营业时间配置
const openingHoursObj = {
  library: '9:00-17:00',
  museum: '11:00-17:00',
  park: 'Open 24 hours',
  community: 'Open 24 hours',
  shopping: '10:00-20:00'
}

// 地图标记图片配置
const mapPhotoObj = {
  library: '/library.png',
  museum: '/museum.png',
  park: '/park.png',
  community: '/community.jpg',
  shopping: '/shopping.png'
}

// 交通方式选项
const transportModes = [
  { value: 'driving', label: 'Drive', icon: '🚗' },
  { value: 'walking', label: 'Walk', icon: '🚶' },
  { value: 'cycling', label: 'Cycle', icon: '🚴' }
]

// 起点名称
const originName = computed(() => {
  if (props.userLocation) {
    return 'Current Location'
  }
  return 'Melbourne CBD'
})

// 计算距离显示文本
const distanceText = computed(() => {
  if (!props.userLocation || !props.refuge?.latitude || !props.refuge?.longitude) {
    return ''
  }
  
  const R = 6371 // 地球半径（公里）
  const dLat = (props.refuge.latitude - props.userLocation.latitude) * Math.PI / 180
  const dLon = (props.refuge.longitude - props.userLocation.longitude) * Math.PI / 180
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(props.userLocation.latitude * Math.PI / 180) *
    Math.cos(props.refuge.latitude * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  const distance = R * c
  
  if (distance < 1) {
    return `${Math.round(distance * 1000)} m`
  } else {
    return `${distance.toFixed(1)} km`
  }
})

// 获取设施列表
const getFacilities = (type) => {
  const facilitiesMap = {
    '❄️': { icon: '❄️', name: 'COOL AIR' },
    '🛜': { icon: '📶', name: 'WIFI' },
    '☕️': { icon: '☕', name: 'CAFE' },
    '🚻': { icon: '🚻', name: 'TOILET' },
    '🅿️': { icon: '🅿️', name: 'PARKING' },
    '💧': { icon: '💧', name: 'WATER' }
  }
  
  const facilityStr = facilitiesObj[type] || ''
  const facilityEmojis = facilityStr.split(/\s+/).filter(e => e)
  
  return facilityEmojis.map(emoji => facilitiesMap[emoji])
}

// 判断是否营业中
const isOpenNow = (type) => {
  const hours = openingHoursObj[type]
  
  // 24小时开放
  if (hours === 'Open 24 hours') {
    return true
  }
  
  // 解析营业时间，如 "9:00-17:00"
  const match = hours.match(/(\d+):(\d+)-(\d+):(\d+)/)
  if (!match) return false
  
  const [, openHour, openMin, closeHour, closeMin] = match.map(Number)
  
  const now = new Date()
  const currentHour = now.getHours()
  const currentMin = now.getMinutes()
  
  // 转换为分钟数便于比较
  const currentTime = currentHour * 60 + currentMin
  const openTime = openHour * 60 + openMin
  const closeTime = closeHour * 60 + closeMin
  
  return currentTime >= openTime && currentTime < closeTime
}

// 初始化 Mapbox token
const initMapboxToken = async () => {
  try {
    const response = await fetch('https://qcbqul6ys2.execute-api.ap-southeast-2.amazonaws.com/mapbox-token')
    const data = await response.json()
    mapboxgl.accessToken = data.token
    return data.token
  } catch (err) {
    console.error('Failed to fetch Mapbox token:', err)
    return ''
  }
}

// 切换交通方式
const switchMode = (mode) => {
  selectedMode.value = mode
  fetchRoute()
}

// 获取路线
const fetchRoute = async () => {
  const origin = props.userLocation 
    ? [props.userLocation.longitude, props.userLocation.latitude]
    : [144.9631, -37.8136] // 墨尔本市中心默认位置
  
  const destination = [props.refuge.longitude, props.refuge.latitude]
  
  try {
    const response = await fetch(
      `https://api.mapbox.com/directions/v5/mapbox/${selectedMode.value}/${origin[0]},${origin[1]};${destination[0]},${destination[1]}?` +
      `geometries=geojson&overview=full&steps=true&access_token=${mapboxgl.accessToken}`
    )
    
    const data = await response.json()
    
    if (data.routes && data.routes.length > 0) {
      const route = data.routes[0]
      
      // 格式化距离和时间
      const distanceKm = (route.distance / 1000).toFixed(1)
      const durationMin = Math.round(route.duration / 60)
      const durationHour = Math.floor(durationMin / 60)
      const durationMinRemain = durationMin % 60
      
      routeInfo.value = {
        distance: `${distanceKm} km`,
        duration: durationHour > 0 
          ? `${durationHour}h ${durationMinRemain}min` 
          : `${durationMin} min`
      }
      
      // 提取步骤
      steps.value = route.legs.flatMap(leg => 
        leg.steps.map(step => step.maneuver.instruction)
      )
      
      // 在地图上绘制路线
      drawRoute(route.geometry)
    }
  } catch (err) {
    console.error('Error fetching route:', err)
  }
}

// 在地图上绘制路线
const drawRoute = (geometry) => {
  if (!map) return
  
  // 添加路线数据源
  if (map.getSource('route')) {
    map.getSource('route').setData({
      type: 'Feature',
      properties: {},
      geometry: geometry
    })
  } else {
    map.addSource('route', {
      type: 'geojson',
      data: {
        type: 'Feature',
        properties: {},
        geometry: geometry
      }
    })
    
    // 添加路线图层
    map.addLayer({
      id: 'route',
      type: 'line',
      source: 'route',
      layout: {
        'line-join': 'round',
        'line-cap': 'round'
      },
      paint: {
        'line-color': '#1a3a8f',
        'line-width': 5,
        'line-opacity': 0.8
      }
    })
  }
  
  // 调整地图视野以包含整个路线
  const coordinates = geometry.coordinates
  const bounds = new mapboxgl.LngLatBounds()
  coordinates.forEach(coord => bounds.extend(coord))
  map.fitBounds(bounds, { padding: 50 })
}

// 初始化地图
const initMap = async () => {
  await initMapboxToken()
  
  const origin = props.userLocation 
    ? [props.userLocation.longitude, props.userLocation.latitude]
    : [144.9631, -37.8136]
  
  map = new mapboxgl.Map({
    container: mapContainer.value,
    style: 'mapbox://styles/mapbox/streets-v12',
    center: origin,
    zoom: 12
  })
  
  map.on('load', () => {
    // 添加起点标记
    new mapboxgl.Marker({ color: '#22c55e' })
      .setLngLat(origin)
      .setPopup(new mapboxgl.Popup().setText('Start'))
      .addTo(map)
    
    // 添加终点标记 - 使用自定义图片
    const refugeType = props.refuge?.type || 'library'
    const markerImage = mapPhotoObj[refugeType] || '/library.png'
    
    // 创建自定义标记元素
    const el = document.createElement('div')
    el.className = 'custom-marker'
    el.style.width = '40px'
    el.style.height = '40px'
    el.style.backgroundImage = `url(${markerImage})`
    el.style.backgroundSize = 'cover'
    el.style.backgroundPosition = 'center'
    el.style.borderRadius = '50%'
    el.style.border = '3px solid white'
    el.style.boxShadow = '0 2px 6px rgba(0,0,0,0.3)'
    el.style.cursor = 'pointer'
    
    // 点击标记显示详情卡片
    el.addEventListener('click', () => {
      showDetailCard.value = true
    })
    
    new mapboxgl.Marker(el)
      .setLngLat([props.refuge.longitude, props.refuge.latitude])
      .addTo(map)
    
    // 获取并显示路线
    fetchRoute()
  })
}

// 获取指定位置的温度
const fetchTemperature = async (latitude, longitude) => {
  try {
    const response = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m`)
    const data = await response.json()
    if (data.current && data.current.temperature_2m !== undefined) {
      return data.current.temperature_2m
    }
    return null
  } catch (err) {
    console.error('Error fetching temperature:', err)
    return null
  }
}

// 获取温度数据
const fetchTemperatureData = async () => {
  const temp = await fetchTemperature(props.refuge.latitude, props.refuge.longitude)
  if (temp !== null) {
    currentTemp.value = temp
  }
}

// 打开 Google Maps
const openGoogleMaps = () => {
  const origin = props.userLocation 
    ? `${props.userLocation.latitude},${props.userLocation.longitude}`
    : '-37.8136,144.9631'
  
  // Google Maps 交通方式映射
  // const googleModeMap = {
  //   driving: 'd',
  //   walking: 'w',
  //   cycling: 'b'
  // }
  
  // const travelmode = googleModeMap[selectedMode.value] || 'd'
  const url = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${props.refuge.latitude},${props.refuge.longitude}`
  window.open(url, '_blank')
}

onMounted(async () => {
  // 获取温度数据（用于路线颜色）
  await fetchTemperatureData()
  // 初始化地图
  initMap()
})
</script>

<style scoped>
.directions-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.directions-modal {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 70%;
  max-height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.directions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.directions-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #1a1a1a;
}

.close-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #f3f4f6;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #e5e7eb;
}

.directions-content {
  overflow-y: auto;
  padding: 24px;
}

/* 温度预警样式 */
.directions-temp-alert {
  margin-bottom: 16px;
}

/* 顶部区域 - 路线信息和交通方式并排 */
.top-section {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  align-items: stretch;
}

.route-info {
  background: #f8fafc;
  border-radius: 12px;
  padding: 12px 16px;
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}

.location-item {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.location-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.location-icon-img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 2px solid white;
}

.location-icon-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.location-item.origin .location-icon {
  background: #dcfce7;
}

.location-details {
  display: flex;
  flex-direction: column;
}

.location-label {
  font-size: 10px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.location-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
}

.route-arrow {
  font-size: 20px;
  color: #9ca3af;
}

/* 交通方式选择 */
.transport-modes {
  display: flex;
  gap: 8px;
}

.mode-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 8px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 60px;
}

.mode-btn:hover {
  border-color: #1a3a8f;
  background: #f8fafc;
}

.mode-btn.active {
  border-color: #1a3a8f;
  background: #1a3a8f;
  color: white;
}

.mode-icon {
  font-size: 20px;
}

.mode-label {
  font-size: 11px;
  font-weight: 500;
}

/* 行内路线统计 */
.route-stats-inline {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: 8px;
  padding-left: 12px;
  border-left: 1px solid #e5e7eb;
}

.stat-divider {
  width: 1px;
  height: 30px;
  background: #e5e7eb;
}

.stat-item-inline {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 50px;
}

.stat-value-inline {
  font-size: 14px;
  font-weight: 700;
  color: #1a3a8f;
}

.stat-label-inline {
  font-size: 10px;
  color: #6b7280;
}

.map-wrapper {
  position: relative;
  margin-bottom: 20px;
}

.directions-map {
  width: 100%;
  height: 60vh;
  border-radius: 12px;
  overflow: hidden;
}

/* 地图详情卡片 */
.map-detail-card {
  position: absolute;
  bottom: 16px;
  right: 16px;
  width: 280px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  z-index: 10;
}

.map-detail-card .close-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 11;
  transition: background 0.2s;
}

.map-detail-card .close-btn:hover {
  background: rgba(0, 0, 0, 0.7);
}

.detail-image {
  position: relative;
  width: 100%;
  height: 120px;
  overflow: hidden;
}

.detail-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.open-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: #22c55e;
  color: white;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
}

.open-badge.closed {
  background: #ef4444;
}

.detail-content {
  padding: 12px;
}

.detail-name {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 6px 0;
}

.detail-address {
  font-size: 12px;
  color: #6b7280;
  margin: 0 0 10px 0;
  line-height: 1.4;
}

.detail-hours {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: 10px;
}

.hours-icon {
  font-size: 16px;
}

.hours-text {
  display: flex;
  flex-direction: column;
}

.hours-label {
  font-size: 10px;
  color: #6b7280;
  text-transform: uppercase;
}

.hours-value {
  font-size: 12px;
  color: #1a1a1a;
  font-weight: 500;
}

.detail-facilities {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.facility-item {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: #f3f4f6;
  border-radius: 12px;
  font-size: 11px;
}

.facility-icon {
  font-size: 12px;
}

.facility-name {
  color: #374151;
  font-weight: 500;
}

.route-steps {
  display: none;
  margin-bottom: 20px;
}

.route-steps h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: #1a1a1a;
}

.step-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.step-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #1a3a8f;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.step-text {
  font-size: 14px;
  color: #374151;
  line-height: 1.5;
}

.directions-actions {
  display: flex;
  gap: 12px;
}

.btn-open-google {
  flex: 1;
  padding: 10px 16px;
  background: #1a3a8f;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: background 0.2s;
}

.btn-open-google:hover {
  background: #142d73;
}

.btn-open-google span {
  font-size: 16px;
}
</style>
