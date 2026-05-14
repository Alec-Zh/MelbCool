<script setup>
// Static explainer — no props needed
</script>

<template>
  <div class="card methodology">
    <p class="guide-title">How the score is calculated</p>
    <ul class="method-list">
      <li>
        <strong>How hot it feels</strong>
        We use "feels like" temperature, which accounts for humidity and wind.
      </li>
      <li>
        <strong>Tree shade in the area</strong>
        Suburbs with fewer trees offer less shade, making outdoor time more dangerous.
      </li>
      <li>
        <strong>How you're travelling</strong>
        Walking means 100% of your trip is outdoors. Public transport reduces this to around 25%.
        Driving reduces it to around 10%.
      </li>
      <li>
        <strong>What time you leave</strong>
        Heat peaks in the early afternoon. Leaving earlier or after 5 pm is usually safer.
      </li>
    </ul>
  </div>
</template>

<style scoped>
.methodology {
  padding: 1rem 1.25rem;
}
.guide-title {
  font-size: 0.72rem;
  font-weight: 700;
  color: #2d7a3a;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0 0 0.65rem;
}
.method-list {
  list-style: disc;
  padding-left: 1.1rem;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.method-list li {
  font-size: 0.82rem;
  color: #5a6e6a;
  line-height: 1.55;
}
.method-list li strong {
  display: block;
  color: #1c2e2a;
  font-weight: 600;
  margin-bottom: 0.1rem;
}
</style>
