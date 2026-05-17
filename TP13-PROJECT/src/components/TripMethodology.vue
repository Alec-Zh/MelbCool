<script setup>
// No props or emits — reset button is handled in TripCoachPage left column
</script>

<template>
  <div class="methodology">
    <h2 class="section-title">How is the score worked out?</h2>

    <div class="items">
      <div class="item">
        <span class="icon">🌡️</span>
        <div>
          <p class="item-label">How hot it feels outside</p>
          <p class="item-desc">
            We use "feels like" temperature — not just the air temperature. This accounts for
            humidity and wind, which can make heat feel much worse.
          </p>
        </div>
      </div>

      <div class="item">
        <span class="icon">🌳</span>
        <div>
          <p class="item-label">How much shade is in the area</p>
          <p class="item-desc">
            Suburbs with fewer trees have less shade. Less shade means your body heats up faster
            when you're outdoors.
          </p>
        </div>
      </div>

      <div class="item">
        <span class="icon">⏱️</span>
        <div>
          <p class="item-label">How long you'll be outside</p>
          <p class="item-desc">
            The longer you're in the heat, the higher your score. Each stage of your trip — walking,
            waiting, travelling — is counted separately.
          </p>
        </div>
      </div>

      <div class="item">
        <span class="icon">🚌</span>
        <div>
          <p class="item-label">How you're travelling</p>
          <p class="item-desc">
            Walking keeps you in the sun the whole time. Trams and buses reduce this, but you still
            walk to the stop. Driving has the least outdoor exposure.
          </p>
        </div>
      </div>
    </div>

    <p class="note">
      Scores are based on heat stress research. Travel time is entered by you — a future version may
      calculate this automatically from your location.
    </p>
  </div>
</template>

<style scoped>
.methodology {
  background: #fdf8f0;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
}
.section-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 1rem;
}
.items {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}
.item {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}
.icon {
  font-size: 1.25rem;
  flex-shrink: 0;
  margin-top: 0.1rem;
}
.item-label {
  font-weight: 700;
  font-size: 0.9rem;
  color: #1a1a1a;
  margin: 0 0 0.2rem;
}
.item-desc {
  font-size: 0.85rem;
  color: #555;
  line-height: 1.55;
  margin: 0;
}
.note {
  font-size: 0.8rem;
  color: #999;
  border-top: 1px solid #e8dcc8;
  padding-top: 0.75rem;
  margin: 1rem 0 0;
  line-height: 1.5;
}
</style>
