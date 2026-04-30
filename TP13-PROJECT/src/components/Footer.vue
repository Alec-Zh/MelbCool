<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-left">
        <RouterLink to="/" class="brand">
          <img src="/logo.png" alt="MelbCool Melbourne" class="footer-logo" />
          <span class="brand-name">MelbCool</span>
        </RouterLink>
        <p class="footer-source">
          Temperature data:
          <a href="https://open-meteo.com" target="_blank" rel="noopener">Open-Meteo</a> ·
          Population data: ABS 2021 Census · Boundaries: data.gov.au
        </p>
      </div>
      <div class="footer-links">
        <a class="footer-link">Privacy Policy</a>
        <a class="footer-link">Accessibility</a>
        <a class="footer-link">Contact Us</a>
      </div>
      <div class="footer-right">
        <p>© 2026 City of Melbourne. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: #f8fafc;
  padding: 2rem;
  border-top: 1px solid #e2e8f0;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
}

.brand-name {
  color: #0d3a8f;
  font-weight: bold;
  font-size: 17px;
}

.footer-logo {
  height: 48px;
  width: auto;
  object-fit: contain;
}

.footer-left {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-source {
  font-size: 0.78rem;
  color: #94a3b8;
  margin: 0;
  line-height: 1.6;
}

.footer-source a {
  color: #64748b;
  text-decoration: none;
}

.footer-source a:hover {
  color: #1a3a8f;
  text-decoration: underline;
}

.footer-links {
  display: flex;
  gap: 2rem;
}

.footer-link {
  text-decoration: none;
  color: #666;
  font-size: 1rem;
  transition: color 0.3s ease;
  cursor: pointer;
}

.footer-link:hover {
  color: #1a3a8f;
}

.footer-right p {
  font-size: 0.875rem;
  color: #94a3b8;
  margin: 0;
}

@media (max-width: 768px) {
  .footer-container {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }

  .footer-links {
    justify-content: center;
  }

  .footer-left {
    align-items: center;
  }
}
</style>
