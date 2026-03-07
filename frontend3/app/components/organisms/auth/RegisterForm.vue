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
      <!-- Name Field -->
      <FormField
        v-if="showNameField"
        :label="nameLabel"
        :error="nameError"
        :hint="nameHint"
        :required="true"
      >
        <Input
          :value="name"
          type="text"
          :placeholder="namePlaceholder"
          :disabled="loading || disabled"
          :clearable="true"
          @input="$emit('name-change', ($event.target as HTMLInputElement).value)"
        />
      </FormField>

      <!-- Email Field -->
      <FormField
        :label="emailLabel"
        :error="emailError"
        :hint="emailHint"
        :required="true"
      >
        <Input
          :value="email"
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
          :value="password"
          type="password"
          :placeholder="passwordPlaceholder"
          :disabled="loading || disabled"
          @input="$emit('password-change', ($event.target as HTMLInputElement).value)"
        />
      </FormField>

      <!-- Confirm Password Field -->
      <FormField
        v-if="showConfirmPassword"
        :label="confirmPasswordLabel"
        :error="confirmPasswordError"
        :hint="confirmPasswordHint"
        :required="true"
      >
        <Input
          :value="confirmPassword"
          type="password"
          :placeholder="confirmPasswordPlaceholder"
          :disabled="loading || disabled"
          @input="$emit('confirm-password-change', ($event.target as HTMLInputElement).value)"
        />
      </FormField>

      <!-- Terms & Conditions -->
      <div v-if="showTerms" class="flex items-center">
        <Checkbox
          :model-value="termsAccepted"
          :label="termsLabel"
          :disabled="loading || disabled"
          :required="true"
          :error="termsError"
          @update:model-value="$emit('terms-change', $event)"
        >
          <span class="text-sm text-gray-700 dark:text-gray-300">
            {{ termsText }}
            <NuxtLink
              v-if="termsLink"
              :to="termsLink"
              class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400"
              target="_blank"
            >
              {{ termsLinkText }}
            </NuxtLink>
          </span>
        </Checkbox>
      </div>

      <!-- Newsletter Opt-in -->
      <div v-if="showNewsletter" class="flex items-center">
        <Checkbox
          :model-value="newsletterOptIn"
          :label="newsletterLabel"
          :disabled="loading || disabled"
          @update:model-value="$emit('newsletter-change', $event)"
        >
          <span class="text-sm text-gray-700 dark:text-gray-300">
            {{ newsletterText }}
          </span>
        </Checkbox>
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
  name?: string
  email?: string
  password?: string
  confirmPassword?: string
  termsAccepted?: boolean
  newsletterOptIn?: boolean
  
  // Labels & Texts
  title?: string
  subtitle?: string
  nameLabel?: string
  namePlaceholder?: string
  nameError?: string
  nameHint?: string
  emailLabel?: string
  emailPlaceholder?: string
  emailError?: string
  emailHint?: string
  passwordLabel?: string
  passwordPlaceholder?: string
  passwordError?: string
  passwordHint?: string
  confirmPasswordLabel?: string
  confirmPasswordPlaceholder?: string
  confirmPasswordError?: string
  confirmPasswordHint?: string
  termsLabel?: string
  termsText?: string
  termsLink?: string
  termsLinkText?: string
  termsError?: string
  newsletterLabel?: string
  newsletterText?: string
  footerText?: string
  footerLink?: string
  footerLinkText?: string
  submitButtonText?: string
  submitButtonLoadingText?: string
  
  // Configuration
  showNameField?: boolean
  showConfirmPassword?: boolean
  showTerms?: boolean
  showNewsletter?: boolean
  showOAuth?: boolean
  showOAuthDivider?: boolean
  oauthProviders?: OAuthProvider[]
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
  // Data defaults
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  termsAccepted: false,
  newsletterOptIn: false,
  
  // Labels & Texts defaults
  title: 'Create Account',
  subtitle: 'Join our community and start building amazing projects',
  nameLabel: 'Full Name',
  namePlaceholder: 'Enter your full name',
  emailLabel: 'Email Address',
  emailPlaceholder: 'Enter your email',
  passwordLabel: 'Password',
  passwordPlaceholder: 'Create a strong password',
  confirmPasswordLabel: 'Confirm Password',
  confirmPasswordPlaceholder: 'Re-enter your password',
  termsLabel: 'Terms & Conditions',
  termsText: 'I agree to the',
  termsLink: '/terms',
  termsLinkText: 'Terms & Conditions',
  newsletterLabel: 'Newsletter Subscription',
  newsletterText: 'Subscribe to our newsletter for updates and announcements',
  footerText: 'Already have an account?',
  footerLink: '/login',
  footerLinkText: 'Sign in',
  submitButtonText: 'Create Account',
  submitButtonLoadingText: 'Creating account...',
  
  // Configuration defaults
  showNameField: true,
  showConfirmPassword: true,
  showTerms: true,
  showNewsletter: true,
  showOAuth: true,
  showOAuthDivider: true,
  oauthProviders: () => ['github', 'google'],
  oauthDividerText: 'Or sign up with',
  
  // State defaults
  error: '',
  success: '',
  loading: false,
  disabled: false,
  
  // Styling defaults
  padding: 'md',
  width: 'md',
  className: ''
})

const emit = defineEmits<{
  submit: [event: Event]
  'name-change': [value: string]
  'email-change': [value: string]
  'password-change': [value: string]
  'confirm-password-change': [value: string]
  'terms-change': [value: boolean]
  'newsletter-change': [value: boolean]
  'oauth-click': [provider: OAuthProvider]
}>()
</script>