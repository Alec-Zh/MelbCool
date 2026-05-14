<template>
 <footer class="mh-footer">
    <div class="mh-footer-inner">
      <div class="mh-footer-brand">
        <a href="index.html" class="mh-brand">
          <img src="/logo-mark-transparent.png" alt="MelbCool" />
          <span>MelbCool</span>
        </a>
        <p>Helping older adults stay safe during Melbourne's heat.</p>
        <p class="mh-footer-source">
          Weather source: <a href="https://open-meteo.com" target="_blank">Open-Meteo</a> ·
          Population: ABS 2021 Census · Boundaries: data.gov.au
        </p>
      </div>
      <div class="mh-footer-nav">
        <p>Navigate</p>
        <RouterLink to="/" class="active">Home</RouterLink>
        <RouterLink to="/heatmap">Heat Map</RouterLink>
        <RouterLink to="/cool-refuges">Cool Refuges</RouterLink>
        <RouterLink to="/trip-coach">Trip Coach</RouterLink>
      </div>
      <div class="mh-footer-emergency">
        <p>Emergency</p>
        <a href="tel:000" class="mh-footer-sos">🚨 Call 000</a>
        <a href="tel:1300606024">Nurse-on-Call: 1300 60 60 24</a>
        <a href="tel:131450">Translation: 131 450</a>
      </div>
    </div>
    <div class="mh-footer-bottom">
      <span>© 2026 City of Melbourne. All rights reserved.</span>
      <span>Guidance only — not medical advice. For emergencies call 000.</span>
    </div>
  </footer>
</template>


