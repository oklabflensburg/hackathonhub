<template>
  <div class="flex flex-col items-center justify-center py-12 text-center">
    <div class="mb-4">
      <Icon :name="icon" :size="size === 'lg' ? 48 : size === 'md' ? 32 : 24" class="text-gray-400" />
    </div>
    <h3 v-if="title" class="text-lg font-medium text-gray-900 mb-2">{{ title }}</h3>
    <p v-if="message" class="text-gray-600 max-w-md mb-6">{{ message }}</p>
    <div v-if="showAction" class="flex gap-2">
      <Button v-if="actionLabel" :variant="actionVariant" @click="action">
        {{ actionLabel }}
      </Button>
      <Button v-if="secondaryActionLabel" variant="ghost" @click="secondaryAction">
        {{ secondaryActionLabel }}
      </Button>
    </div>
    <slot />
  </div>
</template>

<script setup lang="ts">
import Icon from '~/components/atoms/Icon.vue'
import Button from '~/components/atoms/Button.vue'

interface Props {
  title?: string
  message?: string
  icon?: string
  showAction?: boolean
  actionLabel?: string
  actionVariant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  secondaryActionLabel?: string
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  icon: 'inbox',
  showAction: false,
  actionVariant: 'primary',
  size: 'md'
})

const emit = defineEmits<{
  action: []
  secondaryAction: []
}>()

const action = () => {
  emit('action')
}

const secondaryAction = () => {
  emit('secondaryAction')
}
</script>