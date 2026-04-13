<script setup>
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
</script>

<template>
  <div class="page">
    <NavBar :show-alert-button="false" />
    
    <div class="refuges-header">
      <div class="refuges-header-content">
        <div class="header-top">
          <div class="header-text">
            <h1 class="refuges-title">Stay Safe and Cool Today</h1>
            <p class="refuges-description">Find public spaces with air conditioning nearby to escape the summer heat safely.</p>
          </div>
          <div class="current-location">
            <span class="location-icon">📍</span>
            <span class="location-text">CURRENT LOCATION</span>
            <span class="location-result">8 Refuges found near Carlton</span>
          </div>
        </div>
        
        <div class="search-container">
          <input type="text" class="search-input" placeholder="Search by suburb or landmark..." />
          <button class="search-button">FIND</button>
        </div>
        
        <div class="controls-container">
          <div class="view-toggle">
            <button class="view-button active">📋 List</button>
            <button class="view-button">🗺️ Map</button>
          </div>
          <div class="category-filters">
            <button class="filter-button active">All</button>
            <button class="filter-button">📚 Library</button>
            <button class="filter-button">🏛️ Museum</button>
            <button class="filter-button">🌳 Park</button>
            <button class="filter-button">🏘️ Community</button>
            <button class="filter-button">🛍️ Shopping</button>
          </div>
        </div>
        
        <div class="content-container">
          <div class="refuges-list">
            <!-- Carlton Public Library -->
            <div class="refuge-card library">
              <div class="refuge-image">
                <img src="/pic1.jpg" alt="Carlton Public Library" />
              </div>
              <div class="refuge-info">
                <div class="refuge-header">
                  <h3 class="refuge-name">Carlton Public Library</h3>
                  <span class="refuge-distance">0.5 km</span>
                </div>
                <div class="refuge-tags">
                  <span class="tag">Full Air-Con</span>
                  <span class="tag">9:00 AM - 8:00 PM</span>
                </div>
                <div class="refuge-facilities">
                  <span class="facility-label">AVAILABLE FACILITIES</span>
                  <div class="facility-icons">
                    <span class="facility">💧</span>
                    <span class="facility">🚻</span>
                    <span class="facility">📶</span>
                  </div>
                </div>
                <div class="refuge-buttons">
                  <button class="btn-direction">GET DIRECTIONS</button>
                  <button class="btn-details">DETAILS</button>
                </div>
              </div>
            </div>
            
            <!-- Royal Exhibition Museum -->
            <div class="refuge-card museum">
              <div class="refuge-image">
                <img src="/pic1.jpg" alt="Royal Exhibition Museum" />
              </div>
              <div class="refuge-info">
                <div class="refuge-header">
                  <h3 class="refuge-name">Royal Exhibition Museum</h3>
                  <span class="refuge-distance">1.2 km</span>
                </div>
                <div class="refuge-tags">
                  <span class="tag">Advanced Cooling</span>
                  <span class="tag">10:00 AM - 5:00 PM</span>
                </div>
                <div class="refuge-facilities">
                  <span class="facility-label">AVAILABLE FACILITIES</span>
                  <div class="facility-icons">
                    <span class="facility">💧</span>
                    <span class="facility">🚻</span>
                    <span class="facility">📶</span>
                  </div>
                </div>
                <div class="refuge-buttons">
                  <button class="btn-direction">GET DIRECTIONS</button>
                  <button class="btn-details">DETAILS</button>
                </div>
              </div>
            </div>
            
            <!-- Central Plaza Mall -->
            <div class="refuge-card shopping">
              <div class="refuge-image">
                <img src="/pic1.jpg" alt="Central Plaza Mall" />
              </div>
              <div class="refuge-info">
                <div class="refuge-header">
                  <h3 class="refuge-name">Central Plaza Mall</h3>
                  <span class="refuge-distance">1.8 km</span>
                </div>
                <div class="refuge-tags">
                  <span class="tag">Climate Controlled</span>
                  <span class="tag">8:00 AM - 10:00 PM</span>
                </div>
                <div class="refuge-facilities">
                  <span class="facility-label">AVAILABLE FACILITIES</span>
                  <div class="facility-icons">
                    <span class="facility">💧</span>
                    <span class="facility">🚻</span>
                    <span class="facility">📶</span>
                  </div>
                </div>
                <div class="refuge-buttons">
                  <button class="btn-direction">GET DIRECTIONS</button>
                  <button class="btn-details">DETAILS</button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="sidebar">
            <!-- Health Contacts Card -->
            <div class="sidebar-card health-card">
              <h3 class="card-title">* HEALTH CONTACTS</h3>
              <div class="contact-item">
                <span class="contact-label">HEALTH DIRECT ENQ/TS</span>
                <span class="contact-number">1800 022 222</span>
                <span class="contact-note">Professional medical advice for non-emergencies</span>
              </div>
              <div class="contact-item emergency">
                <span class="contact-label">EMERGENCY ONLY</span>
                <span class="contact-number emergency">000</span>
                <span class="contact-note">Call immediately for heatstroke signs</span>
              </div>
            </div>
            
            <!-- Neighborhood Map Card -->
            <div class="sidebar-card map-card">
              <div class="map-header">
                <h3 class="card-title">NEIGHBORHOOD MAP</h3>
                <a href="#" class="view-full">VIEW FULL</a>
              </div>
              <div class="map-image">
                <img src="/pic1.jpg" alt="Neighborhood Map" />
                <div class="map-info">
                  <span class="refuge-count">3 refuges currently open in this view</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Using Cool Refuges Effectively Section -->
        <div class="using-refuges-section">
          <h2 class="section-title">Using Cool Refuges Effectively</h2>
          <div class="tips-container">
            <!-- Drink Water Tip -->
            <div class="tip-item">
              <div class="tip-icon">
                <span class="icon">💧</span>
              </div>
              <h3 class="tip-title">Drink Water</h3>
              <p class="tip-description">Drink plenty of water before you feel thirsty.</p>
            </div>
            
            <!-- Light Clothing Tip -->
            <div class="tip-item">
              <div class="tip-icon">
                <span class="icon">👕</span>
              </div>
              <h3 class="tip-title">Light Clothing</h3>
              <p class="tip-description">Wear loose, lightweight, and light-colored clothes.</p>
            </div>
            
            <!-- Stay Longer Tip -->
            <div class="tip-item">
              <div class="tip-icon">
                <span class="icon">⏰</span>
              </div>
              <h3 class="tip-title">Stay Longer</h3>
              <p class="tip-description">Stay at least 2 hours in a cool refuge to lower body temperature.</p>
            </div>
            
            <!-- Check In Tip -->
            <div class="tip-item">
              <div class="tip-icon">
                <span class="icon">👥</span>
              </div>
              <h3 class="tip-title">Check In</h3>
              <p class="tip-description">Call a friend or family member to let them know where you are.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.refuges-header {
  background-color: #ffffff;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.refuges-header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-text {
  flex: 1;
  min-width: 300px;
}

.refuges-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a3a8f;
  margin-bottom: 0.5rem;
}

.refuges-description {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.current-location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #e6f0ff;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  width: fit-content;
}

.location-icon {
  font-size: 1rem;
}

.location-text {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1a3a8f;
  letter-spacing: 0.5px;
}

.location-result {
  font-size: 0.875rem;
  color: #333;
  font-weight: 500;
}

.search-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  width: 100%;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 1rem;
}

.search-button {
  background-color: #0d3a8f;
  color: #ffffff;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  white-space: nowrap;
}

.search-button:hover {
  background-color: #1a4bb8;
}

.controls-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.view-button {
  padding: 0.5rem 1.5rem;
  border: 1px solid #e2e8f0;
  background-color: #ffffff;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-button.active {
  background-color: #0056b3;
  color: #ffffff;
  border-color: #0056b3;
}

.view-button:hover:not(.active) {
  background-color: #f8f9fa;
  border-color: #dee2e6;
}

.view-toggle {
  display: flex;
  gap: 0;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.view-toggle .view-button {
  border-radius: 0;
  border: none;
  border-right: 1px solid #e2e8f0;
}

.view-toggle .view-button:last-child {
  border-right: none;
}

.category-filters {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-button {
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  background-color: #f8fafc;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.filter-button.active {
  background-color: #0d3a8f;
  color: #ffffff;
  border-color: #0d3a8f;
}

.filter-button:hover:not(.active) {
  background-color: #e2e8f0;
}

.content-container {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.refuges-list {
  flex: 1;
  min-width: 300px;
}

.sidebar {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.refuge-card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  display: flex;
  gap: 1.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.refuge-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.refuge-card.library {
  border-left: 4px solid #3b82f6;
}

.refuge-card.museum {
  border-left: 4px solid #8b5cf6;
}

.refuge-card.shopping {
  border-left: 4px solid #ec4899;
}

.refuge-image {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.refuge-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.refuge-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.refuge-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.refuge-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a3a8f;
  margin: 0;
}

.refuge-distance {
  font-size: 0.875rem;
  font-weight: 500;
  color: #3b82f6;
}

.refuge-features {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 0.75rem;
}

.feature {
  font-size: 0.75rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.refuge-hours {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.hours-label {
  font-weight: 500;
  color: #333;
}

.hours-value {
  color: #666;
}

.refuge-buttons {
  display: flex;
  gap: 0.75rem;
  margin-top: auto;
}

.btn-direction {
  background-color: #0d3a8f;
  color: #ffffff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-direction:hover {
  background-color: #1a4bb8;
}

.btn-details {
  background-color: #f8fafc;
  color: #333;
  border: 1px solid #e2e8f0;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-details:hover {
  background-color: #e2e8f0;
}

.refuge-tags {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.tag {
  background-color: #e0f2fe;
  color: #0284c7;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.refuge-facilities {
  margin-bottom: 1rem;
}

.facility-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #666;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.facility-icons {
  display: flex;
  gap: 0.75rem;
}

.facility {
  font-size: 1rem;
  color: #333;
}

.sidebar-card {
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.health-card {
  background-color: #fecaca;
  border-top: 4px solid #f87171;
}

.map-card {
  background-color: #ffffff;
  border-top: 4px solid #3b82f6;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.health-card .card-title {
  color: #dc2626;
  font-size: 1.125rem;
  font-weight: 700;
}

.contact-item {
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: #ffffff;
  border-radius: 6px;
  border: 1px solid #fecaca;
}

.contact-item:last-child {
  margin-bottom: 0;
}

.contact-item.emergency {
  background-color: #ffffff;
  padding: 1rem;
  border-radius: 6px;
  margin-top: 0.5rem;
  border: 1px solid #fecaca;
}

.contact-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #dc2626;
  margin-bottom: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.contact-number {
  display: block;
  font-size: 1.25rem;
  font-weight: 700;
  color: #dc2626;
  margin-bottom: 0.25rem;
}

.contact-number.emergency {
  color: #dc2626;
  font-size: 2rem;
  font-weight: 800;
}

.contact-note {
  display: block;
  font-size: 0.75rem;
  color: #dc2626;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.view-full {
  font-size: 0.75rem;
  font-weight: 500;
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.3s ease;
}

.view-full:hover {
  color: #1d4ed8;
}

.map-image {
  position: relative;
  border-radius: 6px;
  overflow: hidden;
}

.map-image img {
  width: 100%;
  height: auto;
  display: block;
}

.map-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #3b82f6;
  color: #ffffff;
  padding: 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.map-info::before {
  content: "📍";
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .content-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
  }
  
  .refuge-card {
    flex-direction: column;
  }
  
  .refuge-image {
    width: 100%;
    height: 200px;
  }
  
  .tips-container {
    flex-direction: column;
  }
  
  .tip-item {
    width: 100%;
  }
}

.using-refuges-section {
  background-color: #ebeff7;
  border-radius: 12px;
  padding: 2rem;
  margin-top: 3rem;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0619ab;
  text-align: center;
  margin-bottom: 2rem;
}

.tips-container {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.tip-item {
  flex: 1;
  min-width: 200px;
  text-align: center;
  padding: 1.5rem;
}

.tip-icon {
  width: 60px;
  height: 60px;
  background-color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #d1e7ff;
}

.tip-icon .icon {
  font-size: 1.5rem;
  color: #0056b3;
}

.tip-title {
  font-size: 1rem;
  font-weight: 600;
  color: #000;
  margin-bottom: 0.5rem;
}

.tip-description {
  font-size: 0.875rem;
  color: #333333;
  line-height: 1.4;
}
</style>

