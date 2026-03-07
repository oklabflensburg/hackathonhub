<template>
  <div :class="containerClasses">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full'
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl'
  centered?: boolean
  fluid?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'lg',
  padding: 'md',
  centered: true,
  fluid: false
})

const containerClasses = computed(() => {
  const classes = []
  
  // Size classes
  if (props.fluid) {
    classes.push('w-full')
  } else {
    switch (props.size) {
      case 'xs': classes.push('max-w-screen-xs'); break
      case 'sm': classes.push('max-w-screen-sm'); break
      case 'md': classes.push('max-w-screen-md'); break
      case 'lg': classes.push('max-w-screen-lg'); break
      case 'xl': classes.push('max-w-screen-xl'); break
      case '2xl': classes.push('max-w-screen-2xl'); break
      case 'full': classes.push('max-w-full'); break
    }
  }
  
  // Padding classes
  switch (props.padding) {
    case 'none': classes.push('px-0'); break
    case 'sm': classes.push('px-4 sm:px-6'); break
    case 'md': classes.push('px-4 sm:px-6 lg:px-8'); break
    case 'lg': classes.push('px-6 sm:px-8 lg:px-12'); break
    case 'xl': classes.push('px-8 sm:px-12 lg:px-16'); break
  }
  
  // Centering
  if (props.centered && !props.fluid) {
    classes.push('mx-auto')
  }
  
  return classes.join(' ')
})
</script>