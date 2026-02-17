# Internationalization (i18n) Documentation

## Overview

The Hackathon Hub application has been fully internationalized to support both English (en) and German (de) languages. The i18n implementation uses the `@nuxtjs/i18n` module with `vue-i18n` for Vue 3/Nuxt 3.

## Architecture

### File Structure
```
frontend3/i18n/
├── config.ts          # i18n configuration
├── locales/
│   ├── en.json       # English translations (default)
│   └── de.json       # German translations
└── README.md         # This documentation
```

### Key Features
- **Language Detection**: Automatic detection from browser headers, cookies, and localStorage
- **Routing Strategy**: `prefix_except_default` (German at `/`, English at `/en/`)
- **SSR Support**: Fully compatible with server-side rendering
- **Type Safety**: TypeScript support for translation keys
- **Fallback**: German as default locale with English as fallback

## Usage

### In Vue Templates
Use the `$t()` function in templates:

```vue
<template>
  <h1>{{ $t('app.name') }}</h1>
  <p>{{ $t('app.description') }}</p>
  <button>{{ $t('common.submit') }}</button>
</template>
```

### In Vue Scripts
Use the `useI18n()` composable:

```vue
<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const message = t('errors.somethingWentWrong')
</script>
```

### With Dynamic Parameters
Use curly braces for interpolation:

```json
{
  "validation": {
    "minLength": "Must be at least {min} characters"
  }
}
```

```vue
<template>
  <p>{{ $t('validation.minLength', { min: 8 }) }}</p>
</template>
```

### Pluralization
Use the pipe (`|`) separator for plural forms:

```json
{
  "time": {
    "minutesAgo": "{count} minute ago | {count} minutes ago"
  }
}
```

## Adding New Translations

### 1. Add Translation Keys
Add new keys to both `en.json` and `de.json` files:

```json
// en.json
{
  "newSection": {
    "key": "English translation"
  }
}

// de.json
{
  "newSection": {
    "key": "German translation"
  }
}
```

### 2. Use in Components
Update your component to use the translation key:

```vue
<template>
  <div>{{ $t('newSection.key') }}</div>
</template>
```

### 3. Update Backend Messages (if needed)
For backend error messages, update the corresponding translation in the backend i18n system.

## Translation Keys Structure

The translation keys are organized hierarchically:

- **app**: Application name, tagline, description
- **navigation**: Menu items, navigation labels
- **common**: Common UI elements (buttons, labels, status)
- **auth**: Authentication-related messages
- **errors**: Error messages
- **validation**: Form validation messages
- **dates**: Date-related text
- **time**: Time-related text
- **footer**: Footer content
- **appHeader**: Header navigation
- **languageSwitcher**: Language selection UI
- **home**: Home page content
- **sidebar**: Sidebar navigation
- **profile**: Profile page content
- **hackathons**: Hackathon listing and details
- **projects**: Project listing and details
- **create**: Create project/hackathon forms
- **votes**: Voting interface messages

## Language Switching

Users can switch languages using:
1. The language switcher component in the header
2. URL prefix (`/` for German, `/en/` for English)
3. Browser language detection

The selected language is persisted in cookies and localStorage.

## Testing Translations

### Development
1. Run the development server: `npm run dev`
2. Navigate to `http://localhost:3000` (German)
3. Navigate to `http://localhost:3000/en` (English)
4. Use the language switcher to toggle between languages

### Verifying Coverage
Check for any remaining hardcoded strings by:
1. Searching for English text in Vue components
2. Testing all UI flows in both languages
3. Checking console for missing translation warnings

## Common Issues

### Missing Translations
If a translation key is missing, you'll see:
- Development: The key path in brackets (e.g., `[missing.key]`)
- Production: The fallback language text

### Dynamic Content
For content loaded from APIs (project names, descriptions, etc.), translation happens on the backend. Ensure backend endpoints return localized content based on the `Accept-Language` header.

### Right-to-Left (RTL) Languages
Currently only LTR languages (English, German) are supported. RTL support would require additional CSS and layout adjustments.

## Maintenance

### Adding a New Language
1. Create a new locale file (e.g., `fr.json`)
2. Add the language to the `locales` array in `i18n/config.ts`
3. Update the language switcher component if needed
4. Add translations for all keys

### Updating Translations
1. Update both `en.json` and `de.json` files
2. Keep keys synchronized between files
3. Test both languages after changes

## Backend Integration

The backend also supports i18n for error messages and API responses. Backend translations are managed separately in the `backend/i18n/` directory.

### API Headers
Frontend sends the current locale in the `Accept-Language` header for API requests. Backend uses this to return localized error messages.

## Performance Considerations

- Translation files are loaded on-demand
- Only the current locale is loaded initially
- Other locales are lazy-loaded when needed
- No impact on initial page load performance

## Contributing

When adding new features:
1. Add all UI text to translation files first
2. Use translation keys in components
3. Test in both languages
4. Update this documentation if needed