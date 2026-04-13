export const hoverScale = {
  mounted(el, binding) {

    const scale = binding.value || 1.1
  
    const duration = binding.arg || '0.3s'

    el.style.transition = `transform ${duration} ease`
    
    const computedStyle = window.getComputedStyle(el)
    if (computedStyle.display === 'inline') {
      el.style.display = 'inline-block'
    }
    el.style.cursor = 'pointer'

    el._mouseenterHandler = () => {
      el.style.transform = `scale(${scale})`
    }

    el._mouseleaveHandler = () => {
      el.style.transform = 'scale(1)'
    }

    el.addEventListener('mouseenter', el._mouseenterHandler)
    el.addEventListener('mouseleave', el._mouseleaveHandler)
  },

  unmounted(el) {
    el.removeEventListener('mouseenter', el._mouseenterHandler)
    el.removeEventListener('mouseleave', el._mouseleaveHandler)
  },
}

export default hoverScale
