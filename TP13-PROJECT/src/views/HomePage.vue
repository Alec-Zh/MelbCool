<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import NavBar from '../components/NavBar.vue';
import EmergencyAlertModal from '../components/EmergencyAlertModal.vue';
import Footer from '../components/Footer.vue';

const showBackToTop = ref(false);
const showAlertModal = ref(false);

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
};

const handleScroll = () => {
  showBackToTop.value = window.scrollY > 300;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<template>
  <div class="app">
    <NavBar @alertClick="showAlertModal = true" />

    <main class="main-content">
      <div class="hero">
        <div class="hero-left">
          <h1 class="hero-title">
            Stay Safe and<br />
            <span class="highlight">Cool in Melbourne</span>
          </h1>
          <p class="hero-description">
            Comprehensive resources and real-time guidance to navigate Melbourne's rising
            temperatures with confidence and care.
          </p>
          <div class="hero-buttons">
            <button class="btn-primary"><span class="icon">❄️</span> Find Cool Refuges</button>
            <button class="btn-secondary"><span class="icon">🧾</span> View Heat Map</button>
          </div>
        </div>
      </div>

      <section class="info-section">
        <div class="info-grid">
          <div class="info-left">
            <span class="tag vulnerability">VULNERABILITY AWARENESS</span>
            <h2 class="section-title">Heat Vulnerability Map</h2>
            <p class="section-description">
              This map highlights heat levels across Melbourne suburbs. We specifically track areas
              with high elderly population density to ensure our guardians have the support they
              need where it's needed most.
            </p>
            <div class="map-image">
              <img src="/reli.jpg" alt="Heat Vulnerability Map of Melbourne" />
            </div>
            <a class="explore-link">Explore Heat Map →</a>
          </div>

          <div class="info-right">
            <span class="tag safe">SAFE SPACES</span>
            <h2 class="section-title">Find Your Local Cool Refuge</h2>
            <p class="section-description">
              Looking for a place to rest? We list all accessible libraries, community centers, and
              shopping malls with high-quality air conditioning and comfortable seating.
            </p>
            <div class="refuge-options">
              <div class="refuge-item">
                <span class="refuge-icon">📚</span>
                <div class="refuge-info">
                  <h4>Public Libraries</h4>
                  <p>Quiet, air-conditioned, and free books.</p>
                </div>
              </div>
              <div class="refuge-item">
                <span class="refuge-icon">🏘️</span>
                <div class="refuge-info">
                  <h4>Community Hubs</h4>
                  <p>Meet others while staying safe from the heat.</p>
                </div>
              </div>
            </div>
            <button class="btn-primary" style="justify-content: center">
              <span class="icon">❄️</span> Find Cool Refuges
            </button>
          </div>
        </div>
      </section>

      <section class="risk-section">
        <h2 class="risk-title">How We Calculate Risk</h2>
        <p class="risk-description">
          We combine three simple factors to determine the heat safety level for every suburb in
          Melbourne.
        </p>
        <div class="risk-cards">
          <div class="risk-card temperature">
            <span class="risk-icon">🌡️</span>
            <h3>Temperature Data</h3>
            <p>
              We use live weather station data to track exact ground temperatures throughout the day
              and night.
            </p>
          </div>
          <div class="risk-card tree">
            <span class="risk-icon">🌳</span>
            <h3>Tree Coverage</h3>
            <p>
              Areas with more trees and green spaces stay significantly cooler than concrete urban
              centers.
            </p>
          </div>
          <div class="risk-card elderly">
            <span class="risk-icon">👴</span>
            <h3>Elderly Population</h3>
            <p>
              We prioritize neighborhoods where many older residents live to ensure resources are
              properly allocated.
            </p>
          </div>
        </div>
      </section>

      <section class="health-section">
        <div class="health-container">
          <div class="health-left">
            <h2 class="health-title">Stay Cool, Stay Healthy</h2>
            <p class="health-description">
              Simple, effective actions to manage extreme heat conditions safely.
            </p>
          </div>

          <div class="health-cards">
            <div class="health-card">
              <span class="card-icon">🏠</span>
              <h3>Stay Cool Indoors</h3>
              <ul class="tips-list">
                <li>
                  <span class="check">✓</span>
                  Close blinds and curtains during the peak of the day.
                </li>
                <li>
                  <span class="check">✓</span>
                  Use fans to circulate air, but avoid pointing them directly at the body if over
                  35°C.
                </li>
                <li>
                  <span class="check">✓</span>
                  Open windows for cross-ventilation only once the sun has set.
                </li>
              </ul>
            </div>

            <div class="health-card">
              <span class="card-icon">💧</span>
              <h3>Stay Hydrated & Alert</h3>
              <ul class="tips-list">
                <li>
                  <span class="check">✓</span>
                  Drink water regularly, even if you do not feel thirsty.
                </li>
                <li>
                  <span class="check">✓</span>
                  Opt for light meals like salads or fruit to avoid generating internal heat.
                </li>
                <li>
                  <span class="check">✓</span>
                  Limit alcohol and caffeine which can increase dehydration.
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <Footer />

      <!-- Back to Top Button -->
      <button
        v-if="showBackToTop"
        class="back-to-top"
        @click="scrollToTop"
        aria-label="Back to top"
      >
        ↑
      </button>
    </main>

    <!-- Emergency Alert Modal -->
    <EmergencyAlertModal :show="showAlertModal" @close="showAlertModal = false" />
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.main-content {
  min-height: calc(100vh - 80px);
  background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url('/bg.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

.hero {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 4rem;
  min-height: calc(100vh - 160px);
}

.hero-left {
  flex: 1;
  max-width: 600px;
}

.hero-title {
  font-size: 4rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.hero-title .highlight {
  color: #a3f77d;
}

.hero-description {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  margin-bottom: 2rem;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
}

.btn-primary {
  background-color: #0d3a8f;
  color: #ffffff;
  border: none;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary:hover {
  background-color: #1a4bb8;
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 1rem 2rem;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.info-section {
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
  padding: 5rem 2rem;
}

.info-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
}

.info-left,
.info-right {
  display: flex;
  flex-direction: column;
}

.tag {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 1rem;
  align-self: flex-start;
}

.tag.vulnerability {
  background-color: #ffe4cc;
  color: #c2410c;
}

.tag.safe {
  background-color: #bbf7d0;
  color: #15803d;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 1rem;
}

.section-description {
  font-size: 1rem;
  color: #666;
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

.map-image {
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 1rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.map-image img {
  width: 100%;
  height: 300px;
  object-fit: cover;
  display: block;
}

.explore-link {
  color: #1a3a8f;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
}

.explore-link:hover {
  color: #0d3a8f;
}

.refuge-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.refuge-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background-color: #f8f9ff;
  border-radius: 12px;
  transition: background-color 0.3s ease;
}

.refuge-item:hover {
  background-color: #eef1ff;
}

.refuge-icon {
  font-size: 1.5rem;
}

.refuge-info h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.25rem;
}

.refuge-info p {
  font-size: 0.875rem;
  color: #666;
  margin: 0;
}

.risk-section {
  background-color: #ffffff;
  padding: 5rem 2rem;
  text-align: center;
}

.risk-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.75rem;
}

.risk-description {
  font-size: 1.1rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto 3rem;
}

.risk-cards {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.risk-card {
  background-color: #f8f9ff;
  border-radius: 16px;
  padding: 2rem;
  text-align: left;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
}

.risk-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
}

.risk-card.temperature {
  border-bottom: 4px solid #2563eb;
}

.risk-card.tree {
  border-bottom: 4px solid #16a34a;
}

.risk-card.elderly {
  border-bottom: 4px solid #92400e;
}

.risk-icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 1rem;
}

.risk-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.75rem;
}

.risk-card p {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.health-section {
  background: linear-gradient(135deg, #0c2d6e 0%, #1e4a9e 100%);
  padding: 5rem 2rem;
}

.health-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 4rem;
  align-items: start;
}

.health-left {
  padding-top: 1rem;
}

.health-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 1rem;
}

.health-description {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 2rem;
}

.health-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.health-card {
  background-color: #ffffff;
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.card-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 1rem;
}

.health-card h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0c2d6e;
  margin-bottom: 1.5rem;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tips-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  color: #333;
  line-height: 1.6;
}

.tips-list li:last-child {
  margin-bottom: 0;
}

.check {
  color: #16a34a;
  font-weight: bold;
  flex-shrink: 0;
}



/* Back to Top Button */
.back-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background-color: #0d3a8f;
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(13, 58, 143, 0.3);
  transition: all 0.3s ease;
  z-index: 99;
  border: none;
}

.back-to-top:hover {
  background-color: #1a4bb8;
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(13, 58, 143, 0.4);
}

.back-to-top:active {
  transform: translateY(0);
}
</style>
