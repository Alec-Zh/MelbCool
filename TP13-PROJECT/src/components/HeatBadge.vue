<script setup>
defineProps({
  level: {
    type: String,
    required: true,
    validator: (v) => ['higher', 'moderate', 'lower'].includes(v),
  },
})

const config = {
  higher: { label: 'Hot', bg: '#FEE2E2', color: '#991B1B', border: '#FECACA' },
  moderate: { label: 'Warm', bg: '#FEF3C7', color: '#92400E', border: '#FDE68A' },
  lower: { label: 'Mild', bg: '#DCFCE7', color: '#166534', border: '#BBF7D0' },
}
</script>

<template>
  <span
    class="badge"
    :style="{
      backgroundColor: config[level].bg,
      color: config[level].color,
      border: `1px solid ${config[level].border}`,
    }"
  >
    {{ config[level].label }}
  </span>
</template>

<style scoped>
.badge {
  display: inline-block;
  padding: 0.3rem 0.85rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 0.2px;
  white-space: nowrap;
}
</style>
