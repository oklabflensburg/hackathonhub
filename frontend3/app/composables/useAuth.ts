/**
 * Authentication Composable
 * Bietet eine konsistente Schnittstelle für alle Authentifizierungs-Operationen
 * Kapselt API-Aufrufe und bietet reaktiven State, Loading-States und Error-Handling
 */

import { ref, computed } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useApiClient, type ApiRequestOptions } from '~/utils/api-client'
import type {
  LoginCredentials,
  RegisterCredentials,
  ForgotPasswordData,
  ResetPasswordData,
  VerifyEmailData,
  TwoFactorVerifyData,
  TwoFactorBackupVerifyData,
  UseAuthOptions
} from '~/types/auth-types'

// Re-export die Types für Abwärtskompatibilität
export type {
  LoginCredentials,
  RegisterCredentials,
  ForgotPasswordData,
  ResetPasswordData,
  VerifyEmailData,
  TwoFactorVerifyData,
  TwoFactorBackupVerifyData,
  UseAuthOptions
}

/**
 * Authentication Composable
 */
export function useAuth(options: UseAuthOptions = {}) {
  const {
    autoRedirect = true,
    defaultRedirectUrl = '/'
  } = options

  // Stores
  const authStore = useAuthStore()
  const apiClient = useApiClient()

  // Local state für Composable-spezifische Daten
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed Properties
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const user = computed(() => authStore.user)
  const userInitials = computed(() => authStore.userInitials)

  /**
   * Login mit Email und Passwort
   */
  async function loginWithEmail(credentials: LoginCredentials): Promise<boolean> {
    try {
      isLoading.value = true
      error.value = null

      // API-Aufruf
      const response = await apiClient.post<{
        requires_2fa: boolean
        temp_token?: string
        user_id?: number
        access_token?: string
        refresh_token?: string
        user?: any
      }>('/api/auth/login', credentials, {
        skipAuth: true,
        skipErrorNotification: true // Wir behandeln Errors selbst
      })

      // 2FA erforderlich
      if (response.requires_2fa && response.temp_token) {
        // Navigiere zur 2FA-Verifizierungsseite
        if (autoRedirect && typeof window !== 'undefined') {
          const router = useRouter()
          await router.push('/verify-2fa')
        }
        return false // 2FA erforderlich
      }

      // Normales Login erfolgreich
      if (response.access_token && response.refresh_token) {
        await authStore.handleAuthResponse({
          access_token: response.access_token,
          refresh_token: response.refresh_token,
          user: response.user
        })

        // Redirect nach erfolgreichem Login
        if (autoRedirect && typeof window !== 'undefined') {
          const router = useRouter()
          await router.push(defaultRedirectUrl)
        }

        return true // Login erfolgreich
      }

      throw new Error('Ungültige Login-Antwort vom Server')
    } catch (err: any) {
      error.value = err.message || 'Login fehlgeschlagen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Registrierung mit Email und Passwort
   */
  async function register(credentials: RegisterCredentials): Promise<any> {
    try {
      isLoading.value = true
      error.value = null

      // API-Aufruf
      const response = await apiClient.post('/api/auth/register', {
        email: credentials.email,
        username: credentials.username,
        password: credentials.password
      }, {
        skipAuth: true,
        skipErrorNotification: true
      })

      // Erfolgreiche Registrierung
      return response
    } catch (err: any) {
      error.value = err.message || 'Registrierung fehlgeschlagen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Passwort vergessen
   */
  async function forgotPassword(data: ForgotPasswordData): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      await apiClient.post('/api/auth/forgot-password', {
        email: data.email
      }, {
        skipAuth: true,
        skipErrorNotification: true
      })
    } catch (err: any) {
      error.value = err.message || 'Anfrage zum Zurücksetzen des Passworts fehlgeschlagen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Passwort zurücksetzen
   */
  async function resetPassword(data: ResetPasswordData): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      await apiClient.post('/api/auth/reset-password', {
        token: data.token,
        new_password: data.newPassword
      }, {
        skipAuth: true,
        skipErrorNotification: true
      })
    } catch (err: any) {
      error.value = err.message || 'Passwort-Reset fehlgeschlagen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * E-Mail verifizieren
   */
  async function verifyEmail(data: VerifyEmailData): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      await apiClient.post('/api/auth/verify-email', {
        token: data.token
      }, {
        skipAuth: true,
        skipErrorNotification: true
      })
    } catch (err: any) {
      error.value = err.message || 'E-Mail-Verifizierung fehlgeschlagen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Verifizierungs-E-Mail erneut senden
   */
  async function resendVerificationEmail(email: string): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      await apiClient.post('/api/auth/resend-verification', {
        email
      }, {
        skipAuth: true,
        skipErrorNotification: true
      })
    } catch (err: any) {
      error.value = err.message || 'Verifizierungs-E-Mail konnte nicht gesendet werden'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 2FA-Verifizierung
   */
  async function verifyTwoFactor(data: TwoFactorVerifyData): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      const response = await apiClient.post('/api/auth/verify-2fa', {
        temp_token: data.tempToken,
        code: data.code
      }, {
        skipAuth: true,
        skipErrorNotification: true
      })

      // Login nach erfolgreicher 2FA-Verifizierung
      if (response.access_token && response.refresh_token) {
        await authStore.handleAuthResponse({
          access_token: response.access_token,
          refresh_token: response.refresh_token,
          user: response.user
        })

        // Redirect nach erfolgreichem Login
        if (autoRedirect && typeof window !== 'undefined') {
          const router = useRouter()
          await router.push(defaultRedirectUrl)
        }
      }
    } catch (err: any) {
      error.value = err.message || '2FA-Verifizierung fehlgeschlagen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 2FA-Backup-Code-Verifizierung
   */
  async function verifyTwoFactorBackup(data: TwoFactorBackupVerifyData): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      const response = await apiClient.post('/api/auth/verify-2fa-backup', {
        temp_token: data.tempToken,
        backup_code: data.backupCode
      }, {
        skipAuth: true,
        skipErrorNotification: true
      })

      // Login nach erfolgreicher 2FA-Verifizierung
      if (response.access_token && response.refresh_token) {
        await authStore.handleAuthResponse({
          access_token: response.access_token,
          refresh_token: response.refresh_token,
          user: response.user
        })

        // Redirect nach erfolgreichem Login
        if (autoRedirect && typeof window !== 'undefined') {
          const router = useRouter()
          await router.push(defaultRedirectUrl)
        }
      }
    } catch (err: any) {
      error.value = err.message || '2FA-Backup-Verifizierung fehlgeschlagen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Logout
   */
  async function logout(): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      // Auth-Store logout aufrufen (kümmert sich um API-Aufruf und State-Clearing)
      await authStore.logout()
    } catch (err: any) {
      // Auch bei Fehlern lokal ausloggen
      console.warn('Logout fehlgeschlagen:', err)
      // State trotzdem zurücksetzen
      authStore.user = null
      authStore.token = null
      authStore.refreshToken = null
    } finally {
      isLoading.value = false

      // Redirect nach Logout
      if (autoRedirect && typeof window !== 'undefined') {
        const router = useRouter()
        await router.push('/login')
      }
    }
  }

  /**
   * Login mit Google OAuth
   */
  async function loginWithGoogle(redirectUrl?: string): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      // Redirect zur Google OAuth URL
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'
      
      const url = new URL(`${backendUrl}/api/auth/google`)
      if (redirectUrl) {
        url.searchParams.append('redirect_url', redirectUrl)
      }

      window.location.href = url.toString()
    } catch (err: any) {
      error.value = err.message || 'Google Login fehlgeschlagen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Login mit GitHub OAuth
   */
  async function loginWithGitHub(redirectUrl?: string): Promise<void> {
    try {
      isLoading.value = true
      error.value = null

      // Redirect zur GitHub OAuth URL
      const config = useRuntimeConfig()
      const backendUrl = config.public.apiUrl || 'http://localhost:8000'
      
      const url = new URL(`${backendUrl}/api/auth/github`)
      if (redirectUrl) {
        url.searchParams.append('redirect_url', redirectUrl)
      }

      window.location.href = url.toString()
    } catch (err: any) {
      error.value = err.message || 'GitHub Login fehlgeschlagen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Token-Refresh
   */
  async function refreshToken(): Promise<boolean> {
    try {
      return await authStore.refreshAccessToken()
    } catch (err: any) {
      error.value = err.message || 'Token-Refresh fehlgeschlagen'
      throw err
    }
  }

  /**
   * Error zurücksetzen
   */
  function clearError(): void {
    error.value = null
  }

  /**
   * Loading-State zurücksetzen
   */
  function clearLoading(): void {
    isLoading.value = false
  }

  /**
   * Composable zurücksetzen
   */
  function reset(): void {
    isLoading.value = false
    error.value = null
  }

  return {
    // State
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    
    // Auth Store State (readonly)
    isAuthenticated,
    user,
    userInitials,
    
    // Methods
    loginWithEmail,
    register,
    forgotPassword,
    resetPassword,
    verifyEmail,
    resendVerificationEmail,
    verifyTwoFactor,
    verifyTwoFactorBackup,
    logout,
    loginWithGoogle,
    loginWithGitHub,
    refreshToken,
    
    // Utilities
    clearError,
    clearLoading,
    reset
  }
}