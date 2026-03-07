// Auth Organisms - High-level authentication components
// These components combine multiple molecules and atoms to create complete authentication forms

export { default as LoginForm } from './LoginForm.vue'
export { default as RegisterForm } from './RegisterForm.vue'
export { default as ForgotPasswordForm } from './ForgotPasswordForm.vue'
export { default as ResetPasswordForm } from './ResetPasswordForm.vue'
export { default as EmailVerificationStatus } from './EmailVerificationStatus.vue'
// Additional auth organisms can be added here:
// export { default as ProfileSettingsForm } from './ProfileSettingsForm.vue'

// Re-export types for consistency
// Note: OAuthProvider type is defined within each component file
// For type consistency, import directly from the component that uses it