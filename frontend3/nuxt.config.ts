// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  srcDir: './app',
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt', '@nuxtjs/i18n'],
  css: ['~/assets/css/main.css'],
  typescript: {
    strict: true,
    typeCheck: false
  },
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/scss/variables" as *;'
        }
      }
    }
  },
  runtimeConfig: {
    public: {
      apiUrl: process.env.NUXT_PUBLIC_API_URL || 'http://localhost:8000',
      githubClientId: process.env.NUXT_PUBLIC_GITHUB_CLIENT_ID || '',
      appName: 'Hackathon Dashboard'
    }
  },
  devServer: {
    port: process.env.PORT ? parseInt(process.env.PORT) : 3001
  },

  i18n: {
    vueI18n: "../i18n/i18n.config.ts",
    locales: [
      { code: "de", iso: "de-DE", file: "de.json", name: "Deutsch" },
      { code: "en", iso: "en-US", file: "en.json", name: "English" },
    ],
    defaultLocale: "de",
    strategy: "prefix_except_default",
    lazy: true,
    langDir: "../i18n/locales",
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: "i18n_redirected",
      redirectOn: "root",
    },
    bundle: {
      optimizeTranslationDirective: false
    }
  },
})