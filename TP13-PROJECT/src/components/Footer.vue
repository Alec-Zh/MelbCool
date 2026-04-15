<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-left">
        <div
          style="
            display: flex;
            align-items: center;
            color: #0d3a8f;
            font-weight: bold;
            font-size: 20px;
          "
        >
          <div>CoolPath</div>
          <img src="/logo.png" alt="CoolPath Melbourne" class="footer-logo" />
        </div>
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
}

.footer-logo {
  height: 32px;
  width: auto;
  object-fit: contain;
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
}
</style>
