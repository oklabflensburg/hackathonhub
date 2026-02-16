// Click outside directive plugin for Vue 3
import type { DirectiveBinding } from 'vue'

const clickOutside = {
  beforeMount(el: HTMLElement, binding: DirectiveBinding) {
    el._clickOutsideHandler = (event: Event) => {
      if (!(el === event.target || el.contains(event.target as Node))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el._clickOutsideHandler)
  },
  unmounted(el: HTMLElement) {
    if (el._clickOutsideHandler) {
      document.removeEventListener('click', el._clickOutsideHandler)
    }
  }
}

// Extend HTMLElement type to include our handler
declare global {
  interface HTMLElement {
    _clickOutsideHandler?: (event: Event) => void
  }
}

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.directive('click-outside', clickOutside)
})