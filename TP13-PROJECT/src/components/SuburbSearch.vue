<script setup>
defineProps({
  modelValue: {
    type: String,
    default: '',
  },
})

defineEmits(['update:modelValue'])
</script>

<template>
  <div class="search-wrap">
    <span class="search-icon">🔍</span>
    <input
      type="text"
      class="search-input"
      placeholder="Search suburbs..."
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      aria-label="Search suburbs"
    />
  </div>
</template>

<style scoped>
.search-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.9rem;
  font-size: 1rem;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.85rem 1rem 0.85rem 2.5rem;
  border-radius: var(--radius-card);
  border: 1.5px solid var(--color-border);
  background-color: var(--color-white);
  font-size: 1rem;
  color: var(--color-text);
  outline: none;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(13, 58, 143, 0.1);
}

.search-input::placeholder {
  color: var(--color-text-muted);
}
</style>
