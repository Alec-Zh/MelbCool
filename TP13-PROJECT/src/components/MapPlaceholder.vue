<template>
  <div class="map-wrap">
    <div class="map-placeholder">
      <div class="map-inner">
        <span class="map-icon">🗺</span>
        <p class="map-title">Heat Vulnerability Map</p>
        <p class="map-sub">
          Interactive map coming soon.<br />Leaflet + GeoJSON integration pending.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.map-wrap {
  width: 100%;
  border-radius: var(--radius-card);
  overflow: hidden;
  border: 1.5px solid var(--color-border);
}

.map-placeholder {
  width: 100%;
  height: 420px;
  background: linear-gradient(135deg, #e8f0fe 0%, #c7d7fc 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-inner {
  text-align: center;
}

.map-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 0.75rem;
}

.map-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 0.4rem;
}

.map-sub {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  line-height: 1.6;
}
</style>
