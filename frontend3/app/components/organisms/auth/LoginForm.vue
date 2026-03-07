<template>
  <AuthCard
    :title="title"
    :subtitle="subtitle"
    :padding="padding"
    :width="width"
    :class="className"
  >
    <AuthForm
      :error="error"
      :success="success"
      :loading="loading"
      :disabled="disabled"
      :submit-button-text="submitButtonText"
      :submit-button-loading-text="submitButtonLoadingText"
      @submit="$emit('submit', $event)"
    >
      <!-- Email Field -->
      <FormField
        :label="emailLabel"
        :error="emailError"
        :hint="emailHint"
        :required="true"
      >
        <Input
          v-model="email"
          type="email"
          :placeholder="emailPlaceholder"
          :disabled="loading || disabled"
          :clearable="true"
          @input="$emit('email-change', ($event.target as HTMLInputElement).value)"
        />
      </FormField>

      <!-- Password Field -->
      <FormField
        :label="passwordLabel"
        :error="passwordError"
        :hint="passwordHint"
        :required="true"
      >
        <Input
          v-model="password"
          type="password"
          :placeholder="passwordPlaceholder"
          :disabled="loading || disabled"
          @input="$emit('password-change', ($event.target as HTMLInputElement).value)"
        />
      </FormField>

      <!-- Remember Me & Forgot Password -->
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <Checkbox
            v-model="rememberMe"
            :disabled="loading || disabled"
            :label="rememberMeLabel"
          />
        </div>
        <div class="text-sm">
          <NuxtLink
            :to="forgotPasswordLink"
            class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400"
          >
            {{ forgotPasswordText }}
          </NuxtLink>
        </div>
      </div>

      <!-- OAuth Buttons (optional) -->
      <OAuthButtons
        v-if="showOAuth"
        :providers="oauthProviders"
        :loading="loading"
        :disabled="disabled"
        :show-divider="showOAuthDivider"
        :divider-text="oauthDividerText"
        @provider-click="$emit('oauth-click', $event)"
      />

      <!-- Footer Slot -->
      <template #footer>
        <div class="text-center text-sm text-gray-600 dark:text-gray-400">
          {{ footerText }}
          <NuxtLink
            :to="footerLink"
            class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400"
          >
            {{ footerLinkText }}
          </NuxtLink>
        </div>
      </template>
    </AuthForm>
  </AuthCard>
</template>

<script setup lang="ts">
import AuthCard from '~/components/atoms/AuthCard.vue'
import AuthForm from '~/components/molecules/AuthForm.vue'
import FormField from '~/components/molecules/FormField.vue'
import Input from '~/components/atoms/Input.vue'
import Checkbox from '~/components/atoms/Checkbox.vue'
import OAuthButtons from '~/components/molecules/OAuthButtons.vue'

type OAuthProvider = 'github' | 'google' | 'custom'

interface Props {
  // Data
  email?: string
  password?: string
  rememberMe?: boolean
  
  // Labels & Texts
  title?: string
  subtitle?: string
  emailLabel?: string
  emailPlaceholder?: string
  emailError?: string
  emailHint?: string
  passwordLabel?: string
  passwordPlaceholder?: string
  passwordError?: string
  passwordHint?: string
  rememberMeLabel?: string
  forgotPasswordText?: string
  forgotPasswordLink?: string
  submitButtonText?: string
  submitButtonLoadingText?: string
  footerText?: string
  footerLinkText?: string
  footerLink?: string
  
  // OAuth
  showOAuth?: boolean
  oauthProviders?: OAuthProvider[]
  showOAuthDivider?: boolean
  oauthDividerText?: string
  
  // State
  error?: string
  success?: string
  loading?: boolean
  disabled?: boolean
  
  // Styling
  padding?: 'none' | 'sm' | 'md' | 'lg'
  width?: 'full' | 'md' | 'lg' | 'xl'
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  email: '',
  password: '',
  rememberMe: false,
  title: 'Sign in to your account',
  subtitle: 'Enter your credentials to access your account',
  emailLabel: 'Email address',
  emailPlaceholder: 'you@example.com',
  passwordLabel: 'Password',
  passwordPlaceholder: '••••••••',
  rememberMeLabel: 'Remember me',
  forgotPasswordText: 'Forgot your password?',
  forgotPasswordLink: '/forgot-password',
  submitButtonText: 'Sign in',
  submitButtonLoadingText: 'Signing in...',
  footerText: "Don't have an account?",
  footerLinkText: 'Sign up',
  footerLink: '/register',
  showOAuth: true,
  oauthProviders: () => ['github', 'google'],
  showOAuthDivider: true,
  oauthDividerText: 'Or continue with',
  padding: 'lg',
  width: 'md',
  className: ''
})

const emit = defineEmits<{
  'submit': [event: Event]
  'email-change': [email: string]
  'password-change': [password: string]
  'remember-me-change': [rememberMe: boolean]
  'oauth-click': [provider: OAuthProvider]
}>()

const email = ref(props.email)
const password = ref(props.password)
const rememberMe = ref(props.rememberMe)

watch(email, (newVal) => emit('email-change', newVal))
watch(password, (newVal) => emit('password-change', newVal))
watch(rememberMe, (newVal) => emit('remember-me-change', newVal))
</script>