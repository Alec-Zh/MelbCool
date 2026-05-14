<script setup>
import { ref } from 'vue'

const emit = defineEmits(['unlocked'])

const PASSWORD = import.meta.env.VITE_PREVIEW_PASSWORD
const input = ref('')
const wrong = ref(false)
const shaking = ref(false)

function submit() {
  if (input.value === PASSWORD) {
    sessionStorage.setItem('melbcool_access', 'true')
    emit('unlocked')
  } else {
    wrong.value = true
    shaking.value = true
    setTimeout(() => (shaking.value = false), 500)
  }
}
</script>

<template>
  <div class="gate-bg">
    <div class="gate-card" :class="{ shake: shaking }">
      <div class="brand">MELBCOOL</div>
      <h1 class="title">Welcome.</h1>
      <p class="subtitle">
        This is a private preview for our team and reviewers.<br />
        Please enter the access password to continue.
      </p>

      <label class="input-label">ACCESS PASSWORD</label>
      <input
        v-model="input"
        type="password"
        class="password-input"
        :class="{ 'input-error': wrong }"
        placeholder=""
        @keyup.enter="submit"
        @input="wrong = false"
        autofocus
      />
      <p v-if="wrong" class="error-msg">Incorrect password. Please try again.</p>

      <button class="continue-btn" @click="submit">Continue</button>

      <p class="footer-note">
        Course preview · FIT5120 Industry Experience Studio Project, Monash University.
      </p>
    </div>
  </div>
</template>

<style scoped>
.gate-bg {
  min-height: 100vh;
  background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url('/bg.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.gate-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 2.5rem 2rem;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.brand {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #2d7a3a;
  margin-bottom: 1rem;
}

.title {
  font-size: 2.25rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.75rem;
  line-height: 1.1;
}

.subtitle {
  font-size: 1rem;
  color: #555;
  line-height: 1.6;
  margin-bottom: 1.75rem;
}

.input-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.password-input {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 2px solid #2d7a3a;
  border-radius: 12px;
  font-size: 1rem;
  outline: none;
  transition:
    border-color 0.2s,
    box-shadow 0.2s;
  box-sizing: border-box;
  background: #fff;
  color: #1a1a1a;
}

.password-input:focus {
  border-color: #1a5c28;
  box-shadow: 0 0 0 3px rgba(45, 122, 58, 0.15);
}

.password-input.input-error {
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.12);
}

.error-msg {
  font-size: 0.85rem;
  color: #dc2626;
  margin-top: 0.4rem;
  margin-bottom: 0;
}

.continue-btn {
  width: 100%;
  margin-top: 1.25rem;
  padding: 0.9rem;
  background-color: #a3f77d;
  color: #1a4a12;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition:
    background-color 0.2s,
    transform 0.15s;
}

.continue-btn:hover {
  background-color: #8fed60;
  transform: translateY(-1px);
}

.continue-btn:active {
  transform: translateY(0);
}

.footer-note {
  margin-top: 1.5rem;
  font-size: 0.8rem;
  color: #888;
  line-height: 1.5;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  20% {
    transform: translateX(-8px);
  }
  40% {
    transform: translateX(8px);
  }
  60% {
    transform: translateX(-6px);
  }
  80% {
    transform: translateX(6px);
  }
}

.shake {
  animation: shake 0.45s ease;
}
</style>
