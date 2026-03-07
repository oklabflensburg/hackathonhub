<template>
  <div :class="gridClasses">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  cols?: 1 | 2 | 3 | 4 | 5 | 6 | 12 | string
  gap?: 'none' | 'sm' | 'md' | 'lg' | 'xl'
  responsive?: boolean
  alignItems?: 'start' | 'center' | 'end' | 'stretch'
  justify?: 'start' | 'center' | 'end' | 'between' | 'around'
}

const props = withDefaults(defineProps<Props>(), {
  cols: 1,
  gap: 'md',
  responsive: true,
  alignItems: 'stretch',
  justify: 'start'
})

const normalizedCols = computed(() => {
  const cols = props.cols
  if (typeof cols === 'string') {
    const num = parseInt(cols, 10)
    return (num === 1 || num === 2 || num === 3 || num === 4 || num === 5 || num === 6 || num === 12) ? num : 1
  }
  return cols ?? 1
})

const gridClasses = computed(() => {
  const classes = ['grid']
  
  // Columns
  if (props.responsive) {
    switch (normalizedCols.value) {
      case 1: classes.push('grid-cols-1'); break
      case 2: classes.push('grid-cols-1 sm:grid-cols-2'); break
      case 3: classes.push('grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'); break
      case 4: classes.push('grid-cols-1 sm:grid-cols-2 lg:grid-cols-4'); break
      case 5: classes.push('grid-cols-1 sm:grid-cols-2 lg:grid-cols-5'); break
      case 6: classes.push('grid-cols-1 sm:grid-cols-2 lg:grid-cols-6'); break
      case 12: classes.push('grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6'); break
    }
  } else {
    classes.push(`grid-cols-${normalizedCols.value}`)
  }
  
  // Gap
  switch (props.gap) {
    case 'none': classes.push('gap-0'); break
    case 'sm': classes.push('gap-2 sm:gap-3'); break
    case 'md': classes.push('gap-4 sm:gap-6'); break
    case 'lg': classes.push('gap-6 sm:gap-8'); break
    case 'xl': classes.push('gap-8 sm:gap-12'); break
  }
  
  // Alignment
  switch (props.alignItems) {
    case 'start': classes.push('items-start'); break
    case 'center': classes.push('items-center'); break
    case 'end': classes.push('items-end'); break
    case 'stretch': classes.push('items-stretch'); break
  }
  
  // Justify
  switch (props.justify) {
    case 'start': classes.push('justify-start'); break
    case 'center': classes.push('justify-center'); break
    case 'end': classes.push('justify-end'); break
    case 'between': classes.push('justify-between'); break
    case 'around': classes.push('justify-around'); break
  }
  
  return classes.join(' ')
})
</script>