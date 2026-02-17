<template>
  <footer class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 mt-16">
    <div class="container mx-auto px-4 sm:px-6 py-8 sm:py-12">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
        <!-- Brand -->
        <div class="space-y-4">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center">
              <span class="text-white font-bold text-xl">H</span>
            </div>
            <div>
              <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ t('app.name') }}</h2>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ t('app.tagline') }}</p>
            </div>
          </div>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            {{ t('app.description') }}
          </p>
          <div class="flex space-x-4">
            <a href="#" class="text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
              </svg>
            </a>
            <a href="#" class="text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z" />
              </svg>
            </a>
            <a href="#" class="text-gray-500 dark:text-gray-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
              </svg>
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ t('footer.quickLinks') }}</h3>
          <ul class="space-y-2">
            <li>
              <NuxtLink to="/" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                {{ t('navigation.dashboard') }}
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/hackathons" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                {{ t('navigation.hackathons') }}
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/projects" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                {{ t('navigation.projects') }}
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/create" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                {{ t('navigation.create') }}
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/about" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                {{ t('navigation.about') }}
              </NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Resources -->
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ t('footer.resources') }}</h3>
          <ul class="space-y-2">
            <li>
              <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                {{ t('footer.documentation') }}
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                {{ t('footer.apiReference') }}
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                {{ t('footer.tutorials') }}
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                {{ t('footer.blog') }}
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                {{ t('footer.community') }}
              </a>
            </li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ t('footer.contactUs') }}</h3>
          <ul class="space-y-2">
            <li class="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span>{{ t('footer.email') }}</span>
            </li>
            <li class="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span>{{ t('footer.location') }}</span>
            </li>
          </ul>
          <div class="mt-6">
            <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">{{ t('footer.newsletter') }}</h4>
             <div class="flex flex-col sm:flex-row max-w-full">
                 <input
                  v-model="newsletterEmail"
                  type="email"
                  :placeholder="t('footer.emailPlaceholder')"
                  :disabled="newsletterLoading"
                  class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-t-lg sm:rounded-l-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed w-full"
                  @keyup.enter="subscribeToNewsletter"
                />
                <button 
                  @click="subscribeToNewsletter"
                  :disabled="newsletterLoading || !newsletterEmail"
                  class="inline-flex items-center justify-center px-4 py-2 bg-primary-600 text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed rounded-t-none sm:rounded-tl-none sm:rounded-r-lg mt-0 sm:mt-0 w-full sm:w-auto font-medium"
                >
                <svg 
                  v-if="newsletterLoading" 
                  class="w-5 h-5 animate-spin" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                <span v-else>{{ t('footer.subscribe') }}</span>
              </button>
            </div>
            <div v-if="newsletterMessage" class="mt-2 text-sm" :class="newsletterSuccess ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
              {{ newsletterMessage }}
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="border-t border-gray-200 dark:border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
        <p class="text-gray-600 dark:text-gray-400 text-sm">
          {{ t('footer.copyright') }}
        </p>
        <div class="flex space-x-6 mt-4 md:mt-0">
          <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm transition-colors">
            {{ t('footer.privacyPolicy') }}
          </a>
          <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm transition-colors">
            {{ t('footer.termsOfService') }}
          </a>
          <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm transition-colors">
            {{ t('footer.cookiePolicy') }}
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const { t } = useI18n()

const newsletterEmail = ref('')
const newsletterLoading = ref(false)
const newsletterMessage = ref('')
const newsletterSuccess = ref(false)

const config = useRuntimeConfig()
const apiUrl = config.public.apiUrl

const subscribeToNewsletter = async () => {
  if (!newsletterEmail.value || newsletterLoading.value) {
    return
  }

  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(newsletterEmail.value)) {
    newsletterMessage.value = t('validation.emailInvalid')
    newsletterSuccess.value = false
    return
  }

  newsletterLoading.value = true
  newsletterMessage.value = ''

  try {
    const response = await fetch(`${apiUrl}/api/newsletter/subscribe`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: newsletterEmail.value,
        source: 'website_footer'
      })
    })

    const data = await response.json()

    if (response.ok) {
      newsletterMessage.value = data.message
      newsletterSuccess.value = true
      
      // Clear email field on success
      if (!data.already_subscribed) {
        newsletterEmail.value = ''
      }
      
      // Clear success message after 5 seconds
      setTimeout(() => {
        newsletterMessage.value = ''
      }, 5000)
    } else {
      newsletterMessage.value = data.detail || t('errors.subscriptionFailed')
      newsletterSuccess.value = false
    }
  } catch (error: any) {
    console.error('Newsletter subscription error:', error)
    newsletterMessage.value = t('errors.networkError')
    newsletterSuccess.value = false
  } finally {
    newsletterLoading.value = false
  }
}
</script>