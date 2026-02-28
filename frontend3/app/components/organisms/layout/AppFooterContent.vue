<template>
  <footer class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 mt-8">
    <div class="container mx-auto px-3 sm:px-4 md:px-6 py-10">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <FooterLinkGroup :title="t('footer.quickLinks')" :links="quickLinks" />
        <FooterLinkGroup :title="t('footer.resources')" :links="resourceLinks" />

        <div>
          <h3 class="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">{{ t('footer.contactUs') }}</h3>
          <ul class="space-y-3 text-gray-600 dark:text-gray-400">
            <li>{{ t('footer.email') }}</li>
            <li>{{ t('footer.location') }}</li>
          </ul>
        </div>

        <NewsletterForm
          :title="t('footer.newsletter')"
          :description="t('footer.subscribeToNewsletter')"
          :placeholder="t('footer.emailPlaceholder')"
          :email="newsletterEmail"
          :button-label="newsletterLoading ? t('footer.subscribing') : t('footer.subscribe')"
          :disabled="!canSubscribe"
          :validation-message="validationMessage"
          :validation-class="validationClass"
          @update:email="newsletterEmail = $event"
          @submit="subscribeToNewsletter"
        />
      </div>

      <div class="border-t border-gray-200 dark:border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
        <p class="text-gray-600 dark:text-gray-400 text-sm">{{ t('footer.copyright', { year: currentYear }) }}</p>
        <div class="flex space-x-6 mt-4 md:mt-0">
          <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm transition-colors">{{ t('footer.privacyPolicy') }}</a>
          <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm transition-colors">{{ t('footer.termsOfService') }}</a>
          <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm transition-colors">{{ t('footer.cookiePolicy') }}</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUIStore } from '~/stores/ui'
import { usePreferencesStore } from '~/stores/preferences'
import FooterLinkGroup from '~/components/molecules/FooterLinkGroup.vue'
import NewsletterForm from '~/components/molecules/NewsletterForm.vue'

const { t } = useI18n()
const uiStore = useUIStore()
const preferences = usePreferencesStore()
const apiUrl = useRuntimeConfig().public.apiUrl

const currentYear = new Date().getFullYear()
const newsletterEmail = ref('')
const newsletterLoading = ref(false)
const subscribedEmails = ref<Set<string>>(new Set())

const quickLinks = computed(() => [
  { label: t('appHeader.hackathons'), to: '/hackathons' },
  { label: t('appHeader.projects'), to: '/projects' },
  { label: t('appHeader.create'), to: '/create' },
  { label: t('appHeader.myProfile'), to: '/profile' },
])

const resourceLinks = computed(() => [
  { label: t('footer.documentation'), to: '/about' },
  { label: t('footer.apiReference'), to: '/about' },
  { label: t('footer.tutorials'), to: '/about' },
  { label: t('footer.community'), to: '/users' },
])

onMounted(() => {
  subscribedEmails.value = new Set(preferences.newsletter.getSubscribedEmails())
})

const isValidEmail = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newsletterEmail.value))
const isAlreadySubscribed = computed(() => subscribedEmails.value.has(newsletterEmail.value.toLowerCase()))
const canSubscribe = computed(() => !!newsletterEmail.value && isValidEmail.value && !newsletterLoading.value && !isAlreadySubscribed.value)

const validationMessage = computed(() => {
  if (newsletterEmail.value && !isValidEmail.value) return t('validation.emailInvalid')
  if (isAlreadySubscribed.value) return t('footer.alreadySubscribed')
  return ''
})

const validationClass = computed(() => {
  if (newsletterEmail.value && !isValidEmail.value) return 'text-red-600 dark:text-red-400'
  if (isAlreadySubscribed.value) return 'text-green-600 dark:text-green-400'
  return ''
})

const subscribeToNewsletter = async () => {
  if (!canSubscribe.value) return

  newsletterLoading.value = true
  try {
    const idempotencyKey = `newsletter-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
    const response = await fetch(`${apiUrl}/api/newsletter/subscribe`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Idempotency-Key': idempotencyKey,
      },
      body: JSON.stringify({ email: newsletterEmail.value, source: 'website_footer' }),
    })

    const data = await response.json()

    if (!response.ok) {
      uiStore.showError(data.detail || t('footer.failedToSubscribe'))
      return
    }

    preferences.newsletter.subscribe(newsletterEmail.value)
    subscribedEmails.value = new Set(preferences.newsletter.getSubscribedEmails())
    uiStore.showSuccess(data.message || t('footer.successfullySubscribed'))
    newsletterEmail.value = ''
  } catch (error) {
    console.error('Newsletter subscription error:', error)
    uiStore.showError(t('footer.failedToSubscribe'))
  } finally {
    newsletterLoading.value = false
  }
}
</script>
