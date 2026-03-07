<template>
  <div class="relative overflow-hidden rounded-xl">
    <img
      :src="src"
      :alt="alt"
      :class="[
        'w-full h-full object-cover transition-transform duration-300',
        hoverScale && 'group-hover:scale-105',
        rounded && 'rounded-xl',
        shadow && 'shadow-lg'
      ]"
      :loading="lazy ? 'lazy' : 'eager'"
    />
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  src: string
  alt?: string
  hoverScale?: boolean
  rounded?: boolean
  shadow?: boolean
  lazy?: boolean
}

withDefaults(defineProps<Props>(), {
  alt: 'Hackathon image',
  hoverScale: true,
  rounded: true,
  shadow: true,
  lazy: true
})
</script>