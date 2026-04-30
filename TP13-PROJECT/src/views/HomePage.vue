<script setup>
import { ref } from 'vue'
import NavBar from '../components/NavBar.vue'
import EmergencyAlertModal from '../components/AlertModal.vue'
import Footer from '../components/Footer.vue'

const showAlertModal = ref(false)
</script>

<template>
  <div class="app">
    <NavBar @alertClick="showAlertModal = true" />

    <main class="main-content">
      <div class="heroWrip">
         <div class="hero">
        <div class="hero-left">
          <h1 class="hero-title" v-hover-scale="1.05">
            Stay Safe and<br />
            <span class="highlight">Cool in Melbourne</span>
          </h1>
          <p class="hero-description" v-hover-scale="1.05">
           CoolPath enables older adults (60+) to make safer decisions during extreme heat. Through intelligent heat mapping and route guidance, it identifies high-risk zones, prioritises shaded paths, and directs users to nearby cooling spaces—supporting independence, safety, and everyday mobility.
          </p>
          <div class="hero-buttons">
            <button class="btn-primary" @click="$router.push('/cool-refuges')">
              <span class="icon" v-hover-scale="1.2">❄️ Find Cool Refuges</span>
            </button>
             <button class="btn-secondary" @click="$router.push('/heatmap')">
              <span class="icon" v-hover-scale="1.2">📃 View Heat Map</span></button>
          </div>
        </div>
      </div>
      </div>
     

      <!-- <section class="heat-impact-section">
        <h2 class="heat-impact-title" v-hover-scale="1.5">Heat Impact in Numbers</h2>
        <div class="heat-impact-grid">
          <div class="impact-card blue" >
            <div class="impact-icon">👴</div>
            <div class="impact-number" v-hover-scale="1.2">120k+</div>
            <div class="impact-label" v-hover-scale="1.2">residents live in high-risk zones</div>
          </div>
          <div class="impact-card red" >
            <div class="impact-icon">🔥</div>
            <div class="impact-number" v-hover-scale="1.2">40%</div>
            <div class="impact-label" v-hover-scale="1.2">of heat-related deaths are older adults</div>
          </div>
          <div class="impact-card orange" >
            <div class="impact-icon">🌡️</div>
            <div class="impact-number" v-hover-scale="1.2">38°C</div>
            <div class="impact-label" v-hover-scale="1.2">during peak heatwaves in urban areas</div>
          </div>
          <div class="impact-card green" >
            <div class="impact-icon">🌳</div>
            <div class="impact-number" v-hover-scale="1.2">+7°C</div>
            <div class="impact-label" v-hover-scale="1.2">hotter in areas without sufficient shade</div>
          </div>
        </div>
      </section> -->

      <section class="why-matters-section">
        <h2 class="why-matters-title" v-hover-scale="1.2">Why Heat Protection Matters</h2>
        <p class="why-matters-subtitle" v-hover-scale="1.2">
          Older adults (60+) are more sensitive to heat and at higher risk during hot weather. Staying cool and hydrated is important.
        </p>
        <div class="why-matters-grid">
          <div class="matter-card" >
            <div class="matter-number blue" v-hover-scale="1.2">80%</div>
            <div class="matter-content">
              <h3 v-hover-scale="1.2">of heat-related hospital stays are for adults over 65.</h3>
              <p v-hover-scale="1.2">
                Older bodies hold heat longer, making it harder to recover from a hot afternoon
                without help.
              </p>
              <div class="matter-visual people">
                <span class="person filled">👤</span>
                <span class="person filled">👤</span>
                <span class="person filled">👤</span>
                <span class="person filled">👤</span>
                <span class="person filled">👤</span>
                <span class="person filled">👤</span>
                <span class="person filled">👤</span>
                <span class="person filled">👤</span>
                <span class="person empty">👤</span>
                <span class="person empty">👤</span>
              </div>
            </div>
          </div>

          <div class="matter-card" >
            <div class="matter-number red" v-hover-scale="1.2">30%</div>
            <div class="matter-content">
              <h3 v-hover-scale="1.2">reduction in the body's natural ability to cool down.</h3>
              <p v-hover-scale="1.2">
                As we age, our sweat glands are less active. This means we feel the heat more
                intensely than we used to.
              </p>
              <div class="matter-visual bar-chart">
                <div class="bar-labels">
                  <span class="bar-label" v-hover-scale="1.2">Cooling Power</span>
                  <span class="bar-value" v-hover-scale="1.2">30% Decrease</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 70%"></div>
                </div>
              </div>
            </div>
          </div>

          <div class="matter-card">
            <div class="matter-number blue" v-hover-scale="1.2">+10°F</div>
            <div class="matter-content">
              <h3 v-hover-scale="1.2">Night temperatures in cities can be significantly higher.</h3>
              <p v-hover-scale="1.2">
                Urban heat islands give senior bodies less time to recover from daytime stress,
                leading to cumulative fatigue.
              </p>
              <div class="matter-visual temp-slider">
                <div class="temp-labels">
                  <span class="temp-icon" v-hover-scale="1.2">🌙</span>
                  <span class="temp-label" v-hover-scale="1.2">CITY</span>
                </div>
                <div class="slider-bar">
                  <div class="slider-fill" style="width: 80%"></div>
                </div>
                <span class="temp-high" v-hover-scale="1.2">+10°F Higher Risk</span>
              </div>
            </div>
          </div>

          <div class="matter-card" >
            <div class="matter-number green" v-hover-scale="1.2">2X</div>
            <div class="matter-content">
              <h3 v-hover-scale="1.2">Faster hydration loss during dangerous heatwaves.</h3>
              <p v-hover-scale="1.2">
                Seniors lose hydration twice as fast as younger adults, often without even feeling
                thirsty until it's critical.
              </p>
              <div class="matter-visual hydration">
                <div class="hydration-box normal">
                  <span class="drop-icon" v-hover-scale="1.2">💧</span>
                  <span class="hydration-label" v-hover-scale="1.2">NORMAL</span>
                </div>
                <div class="hydration-box senior">
                  <span class="drop-icon" v-hover-scale="1.2">💧💧</span>
                  <span class="hydration-label" v-hover-scale="1.2">SENIOR (2X RATE)</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="info-section">
        <div class="info-grid">
          <div class="info-left">
            <span class="tag vulnerability" v-hover-scale="1.2">VULNERABILITY AWARENESS</span>
            <h2 class="section-title" v-hover-scale="1.05">Heat Vulnerability Map</h2>
            <p class="section-description" v-hover-scale="1.05">
              The Heat Vulnerability Map shows heat risk levels across Melbourne based on temperature, tree coverage, and elderly population density, highlighting areas where older adults may be more vulnerable.
            </p>
            <div class="map-image">
              <img src="/reli2.png" alt="Heat Vulnerability Map of Melbourne" />
            </div>
             <RouterLink class="explore-link" to="/heatmap"  v-hover-scale="1.05">Explore Heat Map →</RouterLink>
          </div>

          <div class="info-right">
            <div class="risk-level-card">
              <h3 class="risk-level-title" v-hover-scale="1.2">Risk Level</h3>
              <div class="risk-levels">
                <div>
                  <div class="risk-level-item">
                    <span class="risk-dot green"></span>
                    <span class="risk-label" v-hover-scale="1.2">Low</span>
                  </div>
                  <span class="risk-desc" v-hover-scale="1.1">Lower temperatures and greater tree cover; older adults are less affected by heat.</span>
                </div>
                <div >
                  <div class="risk-level-item">
                    <span class="risk-dot yellow"></span>
                    <span class="risk-label" v-hover-scale="1.2">Moderate</span>
                  </div>
                
                  <span class="risk-desc" v-hover-scale="1.1">Higher temperatures or limited shade; older adults should take precautions against heat.</span>
                </div>
                <div>
                  <div  class="risk-level-item">
                    <span class="risk-dot red"></span>
                    <span class="risk-label" v-hover-scale="1.2">High</span>
                  </div>
                 
                  <span class="risk-desc" v-hover-scale="1.1">High temperatures, low tree cover, and a larger older population; older adults are more vulnerable to heat.</span>
                </div>
                <!-- <div class="risk-level-item">
                  <span class="risk-dot red"></span>
                  <span class="risk-label" v-hover-scale="1.2">Very High</span>
                  <span class="risk-desc" v-hover-scale="1.1">Extremely high temperatures, low tree cover, and a large population density.</span>
                </div> -->
              </div>
            </div>

            <!-- <div class="high-risk-stats">
              <h3 class="stats-title" v-hover-scale="1.2">Risk Areas:</h3>
              <div class="stat-item">
                <span class="stat-icon" v-hover-scale="1.2">👤</span>
                <div class="stat-content">
                  <span class="stat-number" v-hover-scale="1.2">29%</span>
                  <span class="stat-label" v-hover-scale="1.2">average elderly<br />population</span>
                </div>
              </div>
              <div class="stat-item">
                <span class="stat-icon" v-hover-scale="1.2">🌡️</span>
                <div class="stat-content">
                  <span class="stat-number" v-hover-scale="1.2">36°C</span>
                  <span class="stat-label" v-hover-scale="1.2">avg surface<br />temperature</span>
                </div>
              </div>
            </div> -->
          </div>
        </div>
      </section>

      <!-- <section class="cool-refuges-section">
        <div class="cool-refuges-container">
          <span class="tag safe" v-hover-scale="1.2">SAFE SPACES</span>
          <h2 class="cool-refuges-title" v-hover-scale="1.2">Find Your Local Cool Refuges</h2>
          <p class="cool-refuges-description" v-hover-scale="1.2">
            Looking for a cool place to go? Cool spaces like libraries, community centers, and
            shopping malls are free, close by, and air-conditioned.
          </p>

          <div class="cool-refuges-content">
            <div class="refuges-left">
              <div class="refuge-stats">
                <div class="refuge-stat-card blue">
                  <span class="stat-icon-large" v-hover-scale="1.2">🌡️</span>
                  <div class="stat-text">
                    <span class="stat-value" v-hover-scale="1.2">20°F</span>
                    <span class="stat-desc" v-hover-scale="1.2">Cooler<br />than outside</span>
                  </div>
                </div>
                <div class="refuge-stat-card green">
                  <span class="stat-icon-large" v-hover-scale="1.2">📍</span>
                  <div class="stat-text">
                    <span class="stat-value" v-hover-scale="1.2">Nearby</span>
                    <span class="stat-desc" v-hover-scale="1.2">Many easy-<br />to-reach places</span>
                  </div>
                </div>
              </div>

              <div class="refuge-types">
                <div class="refuge-type-item">
                  <span class="type-icon" v-hover-scale="1.2">📚</span>
                  <div class="type-info">
                    <h4 v-hover-scale="1.2">Public Libraries</h4>
                    <p v-hover-scale="1.2">Quiet, air-conditioned spaces and free books.</p>
                  </div>
                </div>
                <div class="refuge-type-item">
                  <span class="type-icon" v-hover-scale="1.2">🏘️</span>
                  <div class="type-info">
                    <h4 v-hover-scale="1.2">Community Hubs</h4>
                    <p v-hover-scale="1.2">Meet others in an air-conditioned place.</p>
                  </div>
                </div>
                <div class="refuge-type-item">
                  <span class="type-icon" v-hover-scale="1.2">🛍️</span>
                  <div class="type-info">
                    <h4 v-hover-scale="1.2">Shopping Malls</h4>
                    <p v-hover-scale="1.2">Large, air-conditioned places to walk around.</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="refuges-right">
              <div class="refuge-image">
                <img src="/pic1.jpg" alt="Senior reading in library" />
              </div>
            </div>
          </div>

          <div class="refuge-action">
            <p class="action-hint" v-hover-scale="1.2">👉 Tap to quickly find a nearby cool refuge</p>
            <button class="btn-find-refuge">
              <span class="btn-icon" v-hover-scale="1.2">❄️  Find Cool Refuges Near Me</span>
            </button>
          </div>
        </div>
      </section> -->

      <section class="risk-section">
        <h2 class="risk-title" v-hover-scale="1.2">How We Calculate Risk</h2>
        <p class="risk-description" v-hover-scale="1.2">
          Three key factors determine the heat safety level for each suburb of Melbourne.
        </p>
        <div class="risk-calculate-cards">
          <div class="risk-calc-card temp">
            <div class="card-image">
              <img src="/temperature.png" alt="Temperature" />
            </div>
            <div class="calc-header">
              <div class="calc-title-group">
                <span class="calc-label" v-hover-scale="1.2">Temperature</span>
                <span class="calc-value orange" v-hover-scale="1.2">36-40°C</span>
              </div>
            </div>
            <ul class="calc-list">
              <li v-hover-scale="1.1"><span class="dot red"></span> 10-15 extreme heat days/year</li>
              <li v-hover-scale="1.1"><span class="dot red"></span> Higher night temperatures increase health risk</li>
            </ul>
          </div>
          <div class="risk-calc-card tree">
            <div class="card-image">
              <img src="/tree.jpg" alt="Tree Coverage" />
            </div>
            <div class="calc-header">
              <div class="calc-title-group">
                <span class="calc-label" v-hover-scale="1.2">Tree Coverage</span>
                <span class="calc-value green" v-hover-scale="1.2">&lt; 15%</span>
              </div>
            </div>
            <ul class="calc-list">
              <li v-hover-scale="1.1"><span class="dot green"></span> Low canopy = 5-7°C hotter</li>
              <li v-hover-scale="1.1"><span class="dot green"></span> Less shade means higher body heat and dehydration risk</li>
              <li v-hover-scale="1.1"><span class="dot green"></span> Less shade means higher body heat and dehydration risk
              </li>
            </ul>
          </div>
          <div class="risk-calc-card elderly">
            <div class="card-image">
              <img src="/Elderly.png" alt="Elderly Population" />
            </div>
            <div class="calc-header">
              <div class="calc-title-group">
                <span class="calc-label" v-hover-scale="1.2">Elderly Population</span>
                <span class="calc-value purple" v-hover-scale="1.2">Up to 30%</span>
              </div>
            </div>
            <ul class="calc-list">
              <li v-hover-scale="1.1"><span class="dot purple"></span> More sensitive to heat</li>
              <li v-hover-scale="1.1"><span class="dot purple"></span> May need extra support to stay safe and cool</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="stay-healthy-section">
        <h2 class="stay-healthy-title" v-hover-scale="1.2">Stay Cool, Stay Healthy</h2>
        <p class="stay-healthy-subtitle" v-hover-scale="1.2">
          Simple actions can make a big difference. Protect yourself and check on others.
        </p>
        <div class="healthy-cards">
          <div class="healthy-card">
            <div class="healthy-card-header">
              <span class="healthy-icon blue" v-hover-scale="1.2">🏠</span>
              <h3 v-hover-scale="1.2">Stay Indoors</h3>
            </div>
            <ul class="healthy-list">
              <li v-hover-scale="1.2"><span class="check" >✓</span> Close curtains or blinds</li>
              <li v-hover-scale="1.2"><span class="check" >✓</span> Stay inside between 12-4 PM</li>
              <li v-hover-scale="1.2"><span class="check" >✓</span> Use fans or air conditioning</li>
            </ul>
          </div>

          <div class="healthy-card">
            <div class="healthy-card-header">
              <span class="healthy-icon cyan" v-hover-scale="1.2">💧</span>
              <h3 v-hover-scale="1.2">Drink Water</h3>
            </div>
            <ul class="healthy-list">
              <li v-hover-scale="1.2"><span class="check" >✓</span> Drink a glass every hour</li>
              <li v-hover-scale="1.2"><span class="check" >✓</span> Avoid alcohol and caffeine</li>
              <li v-hover-scale="1.2"><span class="check" >✓</span> Eat light meals, fruits and vegetables</li>
            </ul>
          </div>

          <div class="healthy-card">
            <div class="healthy-card-header">
              <span class="healthy-icon green" v-hover-scale="1.2">🌳</span>
              <h3 v-hover-scale="1.2">Find Cool Places</h3>
            </div>
            <ul class="healthy-list">
              <li v-hover-scale="1.2"><span class="check" >✓</span> Visit a cool refuge nearby</li>
              <li v-hover-scale="1.2"><span class="check" >✓</span> Spend time in shaded areas</li>
              <li v-hover-scale="1.2"><span class="check" >✓</span> Check on family, friends and neighbours</li>
            </ul>
          </div>

          <div class="healthy-card help-card">
            <div class="healthy-card-header">
              <span class="healthy-icon red" v-hover-scale="1.2">📞</span>
              <h3 v-hover-scale="1.2">Need Help?</h3>
            </div>
            <ul class="help-list">
              <li v-hover-scale="1.2"><span class="help-icon" v-hover-scale="1.2">🚨</span> Call 000 in an emergency</li>
              <li v-hover-scale="1.2"><span class="help-icon" v-hover-scale="1.2">👨‍⚕️</span> Nurse-on-Call: 1300 60 60 24</li>
              <li v-hover-scale="1.2"><span class="help-icon" v-hover-scale="1.2">🌐</span> Translation: 131 450</li>
            </ul>
          </div>
        </div>
      </section>

      <Footer />
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
 
  /* background-size: cover; */
  /* background-position: center; */
  /* background-attachment: fixed; */
}
.heroWrip{
   background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url('/bg.jpg');
  background-size: 100% 100%;
  background-repeat: no-repeat;
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
  background-color: #ffffff;
  /* border-radius: 16px; */
  padding: 2rem;
  text-align: left;
  display: flex;
  gap: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.info-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 4rem;
}

.info-left,
.info-right {
  display: flex;
 
  flex-direction: column;
}
.info-right{
 margin-top: 115px;
}

.risk-level-card {
  background-color: #f8f9ff;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  border: 1px solid #e0e7ff;
}

.risk-level-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 1rem;
}

.risk-levels {
  display: flex;
  flex-direction: column;
  gap: 2.8rem;
}

.risk-level-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  gap: 0.75rem;
}

.risk-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  flex-shrink: 0;
}

.risk-dot.green {
  background-color: #22c55e;
}

.risk-dot.yellow {
  background-color: #eab308;
}

.risk-dot.orange {
  background-color: #f97316;
}

.risk-dot.red {
  background-color: #dc2626;
}

.risk-desc{
  padding-left: 20px;
}
.risk-label {
  font-size: 1rem;
  color: #1a1a1a;
  font-weight: bold;
}

.high-risk-stats {
  background-color: #f8f9ff;
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid #e0e7ff;
}

.stats-title {
  color: #1a1a1a;
  margin-bottom: 1.5rem;
  line-height: 1.3;
  font-size: 1.25rem;
  font-weight: 700;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.stat-item:last-child {
  margin-bottom: 0;
}

.stat-icon {
  font-size: 2rem;
  color: #dc2626;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1a1a1a;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.3;
  margin-top: 0.25rem;
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
  height: 400px;
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

.cool-refuges-section {
  background-color: #f0f7ff;
  padding: 5rem 2rem;
}

.cool-refuges-container {
  max-width: 1200px;
  margin: 0 auto;
}

.cool-refuges-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 1rem 0 1rem;
}

.cool-refuges-description {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 2rem;
  max-width: 700px;
}

.cool-refuges-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.refuges-left {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.refuge-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.refuge-stat-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.refuge-stat-card.blue {
  border: 2px solid #dbeafe;
}

.refuge-stat-card.green {
  border: 2px solid #bbf7d0;
}

.stat-icon-large {
  font-size: 2rem;
}

.stat-text {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a1a1a;
}

.stat-desc {
  font-size: 0.8rem;
  color: #666;
  line-height: 1.3;
}

.refuge-types {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.refuge-type-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.type-icon {
  font-size: 1.75rem;
}

.type-info h4 {
  font-size: 1rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.25rem;
}

.type-info p {
  font-size: 0.875rem;
  color: #666;
  margin: 0;
}

.refuges-right {
  display: flex;
  align-items: stretch;
}

.refuge-image {
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.refuge-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.refuge-action {
  text-align: center;
  padding-top: 1rem;
}

.action-hint {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1rem;
}

.btn-find-refuge {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: white;
  border: none;
  padding: 1rem 3rem;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.3);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.btn-find-refuge:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
}

.btn-icon {
  font-size: 1.25rem;
}

@media (max-width: 768px) {
  .cool-refuges-content {
    grid-template-columns: 1fr;
  }

  .refuges-right {
    order: -1;
  }

  .refuge-image {
    height: 250px;
  }
}

.why-matters-section {
  background-color: #f0f7ff;
  padding: 5rem 2rem;
  text-align: center;
}

.why-matters-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.75rem;
}

.why-matters-subtitle {
  font-size: 1rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto 3rem;
  line-height: 1.5;
}

.why-matters-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.matter-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 2rem;
  text-align: left;
  display: flex;
  gap: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.matter-number {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1;
  flex-shrink: 0;
}

.matter-number.blue {
  color: #1e40af;
}

.matter-number.red {
  color: #dc2626;
}

.matter-number.green {
  color: #16a34a;
}

.matter-content h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.matter-content p {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

.matter-visual {
  margin-top: 1rem;
}

.matter-visual.people {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.person {
  font-size: 1.25rem;
}

.person.filled {
  opacity: 1;
}

.person.empty {
  opacity: 0.3;
}

.bar-chart {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
}

.bar-labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.8rem;
}

.bar-label {
  background-color: #dc2626;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-weight: 600;
}

.bar-value {
  color: #666;
}

.progress-bar {
  height: 8px;
  background-color: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #dc2626;
  border-radius: 4px;
}

.temp-slider {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.temp-labels {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.temp-icon {
  font-size: 1.25rem;
}

.temp-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #666;
}

.slider-bar {
  flex: 1;
  height: 8px;
  background-color: #dbeafe;
  border-radius: 4px;
  position: relative;
}

.slider-fill {
  height: 100%;
  background-color: #1e40af;
  border-radius: 4px;
}

.temp-high {
  font-size: 0.75rem;
  color: #1e40af;
  font-weight: 600;
  white-space: nowrap;
}

.hydration {
  display: flex;
  gap: 1rem;
}

.hydration-box {
  flex: 1;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  /* border: 2px solid #e5e7eb; */
}



/* .hydration-box.senior {
  background-color: #16a34a;
  border-color: #16a34a;
} */

.hydration-box.senior .hydration-label {
  color: #16a34a;
}

.drop-icon {
  font-size: 1.5rem;
  display: block;
  margin-bottom: 0.5rem;
}

.hydration-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #666;
}

@media (max-width: 768px) {
  .why-matters-grid {
    grid-template-columns: 1fr;
  }

  .matter-card {
    flex-direction: column;
  }

  .matter-number {
    font-size: 2.5rem;
  }
}

.heat-impact-section {
  background-color: #ffffff;
  padding: 5rem 2rem;
  text-align: center;
}

.heat-impact-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 2rem;
}

.heat-impact-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.impact-card {
  background-color: #f8f9ff;
  border-radius: 16px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.impact-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
}

.impact-card.blue {
  background-color: #eff6ff;
}

.impact-card.red {
  background-color: #fef2f2;
}

.impact-card.orange {
  background-color: #fff7ed;
}

.impact-card.green {
  background-color: #f0fdf4;
}

.impact-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}

.impact-number {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.impact-card.blue .impact-number {
  color: #2563eb;
}

.impact-card.red .impact-number {
  color: #dc2626;
}

.impact-card.orange .impact-number {
  color: #ea580c;
}

.impact-card.green .impact-number {
  color: #16a34a;
}

.impact-label {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

@media (max-width: 1024px) {
  .heat-impact-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .heat-impact-grid {
    grid-template-columns: 1fr;
  }
}

.risk-section {
  background-color: #f0f7ff;
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

.risk-calculate-cards {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.risk-calc-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 1.5rem;
  text-align: left;
  border: 2px solid #e5e7eb;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  overflow: hidden;
}

.risk-calc-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.risk-calc-card.temp {
  border-color: #fed7aa;
  background-color: #fff7ed;
}

.risk-calc-card.tree {
  border-color: #bbf7d0;
  background-color: #f0fdf4;
}

.risk-calc-card.elderly {
  border-color: #ddd6fe;
  background-color: #faf5ff;
}

.card-image {
  margin: -1.5rem -1.5rem 1.5rem -1.5rem;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.calc-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  /* margin-bottom: 1rem; */
}

.calc-icon {
  font-size: 2rem;
}

.calc-title-group {
  display: flex;
  flex-direction: column;
}

.calc-label {
  font-size: 20px;
  color: #666;
  font-weight: bold;
}

.calc-value {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ea580c;
  margin: 10px 0;
}

.calc-value.green {
  color: #16a34a;
}

.calc-value.purple {
  color: #7c3aed;
}

.calc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.calc-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.calc-list .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 0.375rem;
}

.calc-list .dot.red {
  background-color: #ef4444;
}

.calc-list .dot.green {
  background-color: #16a34a;
}

.calc-list .dot.purple {
  background-color: #7c3aed;
}

.stay-healthy-section {
  background-color: #fff;
  padding: 5rem 2rem;
  text-align: center;
}

.stay-healthy-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.75rem;
}

.stay-healthy-subtitle {
  font-size: 1rem;
  color: #666;
  margin-bottom: 2.5rem;
}

.healthy-cards {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.healthy-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 1.5rem;
  text-align: left;
  border: 2px solid #e5e7eb;
}

.healthy-card.help-card {
  background-color: #fef2f2;
  border-color: #fecaca;
}

.healthy-card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.healthy-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.healthy-icon.blue {
  background-color: #dbeafe;
}

.healthy-icon.cyan {
  background-color: #cffafe;
}

.healthy-icon.green {
  background-color: #bbf7d0;
}

.healthy-icon.red {
  background-color: #fecaca;
}

.healthy-card-header h3 {
  font-size: 1rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.healthy-list,
.help-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.healthy-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.healthy-list .check {
  color: #16a34a;
  font-weight: 700;
  flex-shrink: 0;
}

.help-list li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.help-icon {
  font-size: 1rem;
}

@media (max-width: 1024px) {
  .risk-calculate-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .healthy-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .risk-calculate-cards {
    grid-template-columns: 1fr;
  }

  .healthy-cards {
    grid-template-columns: 1fr;
  }
}

.health-section {
  display: none;
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
</style>
