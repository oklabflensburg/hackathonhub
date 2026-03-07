<template>
  <section :class="sectionClasses">
    <Container :size="containerSize" :padding="containerPadding" :centered="containerCentered" :fluid="containerFluid">
      <div v-if="title || subtitle" class="mb-8 text-center">
        <h2 v-if="title" class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          {{ title }}
        </h2>
        <p v-if="subtitle" class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          {{ subtitle }}
        </p>
      </div>
      
      <slot />
    </Container>
  </section>
</template>

<script setup lang="ts">
import Container from '~/components/atoms/Container.vue'

interface Props {
  title?: string
  subtitle?: string
  background?: 'default' | 'muted' | 'primary' | 'secondary'
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl'
  containerSize?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'full'
  containerPadding?: 'none' | 'sm' | 'md' | 'lg' | 'xl'
  containerCentered?: boolean
  containerFluid?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  background: 'default',
  padding: 'lg',
  containerSize: 'lg',
  containerPadding: 'md',
  containerCentered: true,
  containerFluid: false
})

const sectionClasses = computed(() => {
  const classes = []
  
  // Background
  switch (props.background) {
    case 'default': classes.push('bg-white dark:bg-gray-900'); break
    case 'muted': classes.push('bg-gray-50 dark:bg-gray-800'); break
    case 'primary': classes.push('bg-primary-50 dark:bg-primary-900/20'); break
    case 'secondary': classes.push('bg-secondary-50 dark:bg-secondary-900/20'); break
  }
  
  // Padding
  switch (props.padding) {
    case 'none': classes.push('py-0'); break
    case 'sm': classes.push('py-8'); break
    case 'md': classes.push('py-12'); break
    case 'lg': classes.push('py-16'); break
    case 'xl': classes.push('py-24'); break
  }
  
  return classes.join(' ')
})
</script>

<script lang="ts">
import { computed } from 'vue'
</script>