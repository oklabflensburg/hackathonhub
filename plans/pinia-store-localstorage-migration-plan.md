# Pinia Store LocalStorage Migration Plan

# Pinia Store LocalStorage Migration - Implementation Complete

## Overview
Successfully migrated all direct `localStorage` usage to a centralized Pinia preferences store with proper SSR handling. All localStorage operations are now centralized in a single store with type-safe APIs.

## Implementation Status: ✅ COMPLETED
**Date**: 2026-02-20  
**Files Modified**: 5  
**Lines Changed**: ~150  
**Migration Time**: ~30 minutes

## Summary of Changes

### 1. Created Centralized Preferences Store (`frontend3/app/stores/preferences.ts`)
- **SSR-safe localStorage wrapper** with automatic JSON serialization/deserialization
- **Namespaced modules** for different data types:
  - `auth`: Authentication tokens and user data
  - `theme`: Theme preferences (light/dark mode)
  - `language`: Language preferences
  - `newsletter`: Newsletter email subscriptions
- **Type-safe APIs** with proper TypeScript interfaces
- **Error handling** for storage operations
- **Automatic initialization** on client-side

### 2. Refactored Auth Store (`frontend3/app/stores/auth.ts`)
- **Replaced 12 localStorage calls** with preferences store methods
- **Updated functions**:
  - `handleAuthResponse()`: Now uses `preferences.auth.setTokens()`
  - `refreshAccessToken()`: Now uses `preferences.auth.setTokens()` and `preferences.auth.setUser()`
  - `logout()`: Now uses `preferences.auth.clearAuth()`
  - `initializeAuth()`: Now loads from `preferences.auth.tokens` and `preferences.auth.user`
  - `fetchUserWithToken()`: Now uses `preferences.auth.setUser()`
  - `refreshUser()`: Now uses `preferences.auth.setUser()`

### 3. Refactored Theme Store (`frontend3/app/stores/theme.ts`)
- **Replaced 3 localStorage calls** with preferences store methods
- **Updated functions**:
  - `toggleTheme()`: Now uses `preferences.theme.setTheme()`
  - `setTheme()`: Now uses `preferences.theme.setTheme()`
  - `initializeTheme()`: Now uses `preferences.theme.initialize()`

### 4. Updated LanguageSwitcher Component (`frontend3/app/components/LanguageSwitcher.vue`)
- **Replaced direct localStorage** with `preferences.language.setLanguage()`
- **Removed `process.client` check** (handled by preferences store)
- **Added import** for preferences store

### 5. Updated AppFooter Component (`frontend3/app/components/AppFooter.vue`)
- **Replaced newsletter localStorage** with `preferences.newsletter` methods
- **Updated functions**:
  - `loadSubscribedEmails()`: Now uses `preferences.newsletter.getSubscribedEmails()`
  - `saveSubscribedEmail()`: Now uses `preferences.newsletter.subscribe()`
- **Removed `SUBSCRIBED_EMAILS_KEY` constant** (now managed by preferences store)

## Current State Analysis

### localStorage Usage Locations:

1. **Auth Store** (`frontend3/app/stores/auth.ts`)
   - Tokens: `auth_token`, `refresh_token`
   - User data: `user`
   - Multiple direct localStorage calls with SSR checks

2. **Theme Store** (`frontend3/app/stores/theme.ts`)
   - Theme preference: `theme`
   - Uses `typeof window !== 'undefined'` checks

3. **LanguageSwitcher Component** (`frontend3/app/components/LanguageSwitcher.vue`)
   - Language preference: `preferred-language`
   - Uses `process.client` check

4. **AppFooter Component** (`frontend3/app/components/AppFooter.vue`)
   - Newsletter subscriptions: `subscribed-emails`
   - No SSR checks (potential SSR issue)

## Proposed Architecture

### Centralized Preferences Store
Create `frontend3/app/stores/preferences.ts` with:

```typescript
// Key features:
1. SSR-safe localStorage operations
2. Type-safe getters/setters
3. Namespaced storage keys
4. Automatic JSON serialization/deserialization
5. Change observers/event system
```

### Store Structure:
```typescript
interface PreferencesStore {
  // Core storage methods
  getItem<T>(key: string, defaultValue?: T): T | null
  setItem<T>(key: string, value: T): void
  removeItem(key: string): void
  clear(): void
  
  // Namespaced modules
  auth: {
    tokens: { access: string | null; refresh: string | null }
    user: User | null
    setTokens(access: string, refresh: string): void
    clearAuth(): void
  }
  
  theme: {
    current: 'light' | 'dark'
    setTheme(theme: 'light' | 'dark'): void
    toggleTheme(): void
  }
  
  language: {
    preferred: string
    setLanguage(lang: string): void
  }
  
  newsletter: {
    subscribedEmails: Set<string>
    isSubscribed(email: string): boolean
    subscribe(email: string): void
  }
}
```

## Migration Steps

### Phase 1: Create Preferences Store
1. Create `preferences.ts` store with SSR-safe localStorage wrapper
2. Implement core storage methods with error handling
3. Add namespaced modules for each data type

### Phase 2: Refactor Existing Stores
1. **Auth Store**: Replace direct localStorage calls with `preferences.auth` methods
2. **Theme Store**: Replace localStorage calls with `preferences.theme` methods
3. Update initialization logic to use store methods

### Phase 3: Update Components
1. **LanguageSwitcher**: Use `preferences.language.setLanguage()` instead of direct localStorage
2. **AppFooter**: Use `preferences.newsletter` methods for email subscriptions
3. Remove all direct localStorage references from components

### Phase 4: Testing & Cleanup
1. Test all functionality (auth, theme switching, language switching, newsletter)
2. Verify SSR compatibility
3. Remove any remaining localStorage imports/references
4. Update documentation

## Benefits

1. **SSR Compatibility**: Centralized SSR handling eliminates duplicate checks
2. **Type Safety**: TypeScript interfaces for all stored data
3. **Consistency**: Uniform API for all storage operations
4. **Maintainability**: Single source of truth for storage logic
5. **Testability**: Mockable store interface for testing
6. **Extensibility**: Easy to add new storage types or migrate to different backends

## Key Decisions

1. **SSR Strategy**: Use `process.client` check at store level, not component level
2. **Error Handling**: Centralized error handling for storage operations
3. **Data Structure**: Use native types (Set for emails) with automatic serialization
4. **Migration Path**: Gradual migration with backward compatibility

## Implementation Details

### SSR-Safe Storage Wrapper
```typescript
class SSRStorage {
  getItem<T>(key: string): T | null {
    if (typeof window === 'undefined') return null
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : null
    } catch (error) {
      console.error(`Failed to get item ${key}:`, error)
      return null
    }
  }
  
  setItem<T>(key: string, value: T): void {
    if (typeof window === 'undefined') return
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error(`Failed to set item ${key}:`, error)
    }
  }
}
```

### Backward Compatibility
- Keep existing localStorage keys during migration
- Add migration logic if key format changes
- Provide fallback to direct localStorage during transition

## Testing Strategy

1. **Unit Tests**: Test store methods in isolation
2. **Integration Tests**: Test store interactions with components
3. **SSR Tests**: Verify server-side rendering doesn't break
4. **Browser Tests**: Test actual localStorage persistence
5. **Error Handling**: Test storage failures (quota exceeded, etc.)

## Timeline & Dependencies

### Dependencies:
- Pinia already installed and configured
- Existing stores need minimal modifications
- No external dependencies required

### Risk Assessment:
- **Low Risk**: Gradual migration with fallbacks
- **Medium Impact**: Changes multiple files but logic remains similar
- **High Value**: Improved architecture and maintainability

## Success Criteria

1. All localStorage operations go through preferences store
2. No direct `localStorage` references in components
3. SSR works correctly for all pages
4. All existing functionality preserved
5. TypeScript compilation passes without errors
6. No console errors during normal operation