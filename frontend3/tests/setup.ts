import { config } from '@vue/test-utils'
import { vi } from 'vitest'
import { ref } from 'vue'

// Mock Nuxt composables
vi.mock('~/composables/useUserProfile', () => ({
  useUserProfile: () => ({
    user: ref(null),
    loading: ref(false),
    error: ref(null),
    fetchUser: vi.fn(),
    updateUser: vi.fn()
  }),
  useCurrentUser: () => ({
    user: ref(null),
    loading: ref(false),
    error: ref(null),
    isAuthenticated: ref(false)
  })
}))

vi.mock('~/composables/useNotifications', () => ({
  useNotifications: () => ({
    notifications: ref([]),
    loading: ref(false),
    error: ref(null),
    fetchNotifications: vi.fn(),
    markAsRead: vi.fn()
  }),
  useNotificationPreferences: () => ({
    preferences: ref({}),
    loading: ref(false),
    error: ref(null),
    fetchPreferences: vi.fn(),
    updatePreference: vi.fn()
  })
}))

vi.mock('~/composables/useHackathonData', () => ({
  useHackathonData: () => ({
    hackathon: ref(null),
    loading: ref(false),
    error: ref(null),
    fetchHackathon: vi.fn()
  }),
  useHackathonsList: () => ({
    hackathons: ref([]),
    loading: ref(false),
    error: ref(null),
    fetchHackathons: vi.fn()
  })
}))

// Mock Nuxt $fetch
global.$fetch = vi.fn()

// Mock Nuxt useRuntimeConfig
vi.mock('#imports', () => ({
  useRuntimeConfig: () => ({
    public: {
      apiBase: 'http://localhost:3000/api'
    }
  })
}))

// Configure Vue Test Utils
config.global.stubs = {
  NuxtLink: true,
  NuxtImg: true,
  ClientOnly: true
}

config.global.mocks = {
  $t: (key: string) => key,
  $i18n: {
    locale: 'de'
  }
}