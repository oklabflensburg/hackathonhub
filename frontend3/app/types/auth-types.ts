/**
 * Authentication TypeScript Types
 * Zentrale Definition aller Authentifizierungs-Interfaces
 */

export interface LoginCredentials {
  email: string
  password: string
  rememberMe?: boolean
}

export interface RegisterCredentials {
  email: string
  username: string
  password: string
  confirmPassword: string
}

export interface ForgotPasswordData {
  email: string
}

export interface ResetPasswordData {
  token: string
  newPassword: string
}

export interface VerifyEmailData {
  token: string
}

export interface TwoFactorVerifyData {
  tempToken: string
  code: string
}

export interface TwoFactorBackupVerifyData {
  tempToken: string
  backupCode: string
}

export interface UseAuthOptions {
  /** Automatisches Redirect nach Login/Logout */
  autoRedirect?: boolean
  /** Standard-Redirect-URL */
  defaultRedirectUrl?: string
}
