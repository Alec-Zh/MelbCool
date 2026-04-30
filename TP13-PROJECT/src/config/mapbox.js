export const MAPBOX_CONFIG = {
  accessToken: import.meta.env.VITE_MAPBOX_ACCESS_TOKEN,
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [144.9631, -37.8136], // Melbourne coordinates
  zoom: 12,
  radius: 10000, // 10km in meters
}

export const MELBOURNE_CENTER = {
  lng: 144.9631,
  lat: -37.8136,
}

export const REFUGE_TYPES = {
  library: {
    name: 'Library',
    color: '#3b82f6',
    icon: '📚',
  },
  museum: {
    name: 'Museum',
    color: '#8b5cf6',
    icon: '🏛️',
  },
  park: {
    name: 'Park',
    color: '#16a34a',
    icon: '🌳',
  },
  community: {
    name: 'Community',
    color: '#f59e0b',
    icon: '🏘️',
  },
  shopping: {
    name: 'Shopping',
    color: '#ec4899',
    icon: '🛍️',
  },
}
