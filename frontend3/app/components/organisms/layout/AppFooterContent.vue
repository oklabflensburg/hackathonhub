<template>
  <footer class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 mt-8">
    <Container class="py-10" :size="'2xl'">
      <Grid cols="4" gap="lg">
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
          :button-label="isLoading ? t('footer.subscribing') : t('footer.subscribe')"
          :disabled="!canSubscribe"
          :validation-message="validationMessage"
          :validation-class="validationClass"
          @update:email="newsletterEmail = $event"
          @submit="subscribeToNewsletter"
        />
      </Grid>

      <div class="border-t border-gray-200 dark:border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
        <p class="text-gray-600 dark:text-gray-400 text-sm">{{ t('footer.copyright', { year: currentYear }) }}</p>
        <div class="flex space-x-6 mt-4 md:mt-0">
          <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm transition-colors">{{ t('footer.privacyPolicy') }}</a>
          <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm transition-colors">{{ t('footer.termsOfService') }}</a>
          <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm transition-colors">{{ t('footer.cookiePolicy') }}</a>
        </div>
      </div>
    </Container>
  </footer>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUIStore } from '~/stores/ui'
import { usePreferencesStore } from '~/stores/preferences'
import FooterLinkGroup from '~/components/molecules/FooterLinkGroup.vue'
import NewsletterForm from '~/components/molecules/NewsletterForm.vue'
import Container from '~/components/atoms/Container.vue'
import Grid from '~/components/molecules/Grid.vue'

const { t } = useI18n()
const uiStore = useUIStore()
const preferences = usePreferencesStore()
const { subscribe, isLoading, error } = useNewsletter({
  autoErrorHandling: false, // Wir behandeln Errors selbst
  autoSuccessHandling: false // Wir behandeln Success selbst
})

const currentYear = new Date().getFullYear()
const newsletterEmail = ref('')
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
const canSubscribe = computed(() => !!newsletterEmail.value && isValidEmail.value && !isLoading.value && !isAlreadySubscribed.value)

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

  try {
    await subscribe(newsletterEmail.value, 'website_footer')
    
    // Erfolg - lokalen State aktualisieren
    preferences.newsletter.subscribe(newsletterEmail.value)
    subscribedEmails.value = new Set(preferences.newsletter.getSubscribedEmails())
    uiStore.showSuccess(t('footer.successfullySubscribed'))
    newsletterEmail.value = ''
  } catch (err: any) {
    // Error wird bereits vom Composable gesetzt, aber wir zeigen eine benutzerdefinierte Nachricht
    uiStore.showError(err.message || t('footer.failedToSubscribe'))
  }
}
</script>
