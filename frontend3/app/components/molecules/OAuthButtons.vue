<template>
  <div :class="['space-y-3', className]">
    <!-- Divider with "or" text -->
    <div v-if="showDivider" class="relative">
      <div class="absolute inset-0 flex items-center">
        <div class="w-full border-t border-gray-300 dark:border-gray-700"></div>
      </div>
      <div class="relative flex justify-center text-sm">
        <span class="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">
          {{ dividerText }}
        </span>
      </div>
    </div>

    <!-- OAuth Buttons -->
    <div class="space-y-3">
      <OAuthButton
        v-for="provider in enabledProviders"
        :key="provider"
        :provider="provider"
        :disabled="loading || disabled"
        :text="getButtonText(provider)"
        @click="$emit('provider-click', provider)"
      />
    </div>

    <!-- Custom Slot for additional buttons -->
    <slot />
  </div>
</template>

<script setup lang="ts">
import OAuthButton from '~/components/atoms/OAuthButton.vue'

type OAuthProvider = 'github' | 'google' | 'custom'

interface Props {
  providers?: OAuthProvider[]
  loading?: boolean
  disabled?: boolean
  showDivider?: boolean
  dividerText?: string
  className?: string
  buttonTexts?: Partial<Record<OAuthProvider, string>>
}

const props = withDefaults(defineProps<Props>(), {
  providers: () => ['github', 'google'],
  loading: false,
  disabled: false,
  showDivider: true,
  dividerText: 'Or continue with',
  className: '',
  buttonTexts: () => ({})
})

const emit = defineEmits<{
  'provider-click': [provider: OAuthProvider]
}>()

const enabledProviders = computed(() => {
  return props.providers.filter(p => p !== 'custom')
})

const getButtonText = (provider: OAuthProvider) => {
  if (props.buttonTexts[provider]) {
    return props.buttonTexts[provider]!
  }
  return undefined // Fallback to default text in OAuthButton
}
</script>