# Mobile-First Design System

## Spacing Scale (Mobile First)
```
--space-xs: 0.25rem;  /* 4px - gap-1 */
--space-sm: 0.5rem;   /* 8px - gap-2 */
--space-md: 0.75rem;  /* 12px - gap-3 */
--space-lg: 1rem;     /* 16px - gap-4 */
--space-xl: 1.5rem;   /* 24px - gap-6 */
--space-2xl: 2rem;    /* 32px - gap-8 */
```

## Typography Scale (Mobile First)
```
--text-xs: 0.75rem;   /* 12px - text-xs */
--text-sm: 0.875rem;  /* 14px - text-sm */
--text-base: 1rem;    /* 16px - text-base */
--text-lg: 1.125rem;  /* 18px - text-lg */
--text-xl: 1.25rem;   /* 20px - text-xl */
--text-2xl: 1.5rem;   /* 24px - text-2xl */
--text-3xl: 1.875rem; /* 30px - text-3xl */
--text-4xl: 2.25rem;  /* 36px - text-4xl */
```

## Component Specifications

### 1. Cards
**Mobile (`sm` and below)**:
```css
.card-mobile {
  padding: var(--space-lg); /* 1rem = 16px */
  border-radius: 0.75rem; /* rounded-lg */
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); /* shadow-md */
  margin-bottom: var(--space-xl); /* 1.5rem = 24px */
}
```

**Tablet (`md`)**:
```css
.card-tablet {
  padding: 1.25rem; /* p-5 */
  border-radius: 1rem; /* rounded-xl */
}
```

**Desktop (`lg` and above)**:
```css
.card-desktop {
  padding: var(--space-xl); /* 1.5rem = 24px */
  border-radius: 1rem; /* rounded-xl */
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1); /* shadow-lg */
}
```

### 2. Stats Cards (Profile Page)
**Current Structure**:
```html
<div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
  <div class="flex items-center justify-between">
    <div>
      <p class="text-sm text-gray-500">Hackathons Created</p>
      <p class="text-3xl font-bold text-gray-900 mt-2">5</p>
    </div>
    <div class="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center">
      <!-- Icon -->
    </div>
  </div>
  <div class="mt-4 flex items-center text-sm text-blue-600">
    <span>View your hackathons</span>
    <!-- Arrow icon -->
  </div>
</div>
```

**Improved Mobile Structure**:
```html
<div class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm 
            rounded-lg shadow-md p-4 
            border border-gray-100 dark:border-gray-700
            hover:border-primary-200 dark:hover:border-primary-800
            transition-all duration-200">
  
  <!-- Stack vertically on mobile -->
  <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
    
    <!-- Icon above text on mobile, left on tablet+ -->
    <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 
                flex items-center justify-center mb-3 sm:mb-0 sm:mr-4">
      <svg class="w-5 h-5 text-white">...</svg>
    </div>
    
    <div class="text-center sm:text-left">
      <p class="text-xs font-medium text-gray-500 dark:text-gray-400 
                uppercase tracking-wide mb-1">
        Hackathons
      </p>
      <p class="text-2xl font-bold text-gray-900 dark:text-white">5</p>
    </div>
    
  </div>
  
  <!-- Simplified link - text only, no arrow on mobile -->
  <div class="mt-3 text-center sm:text-left">
    <span class="text-xs font-medium text-blue-600 dark:text-blue-400 
                 hover:text-blue-700 dark:hover:text-blue-300 transition-colors">
      View details
    </span>
  </div>
  
</div>
```

### 3. Project Cards
**Mobile Improvements**:
1. Reduce image height: `h-48` → `h-40`
2. Collapse tech tags: Show 2 tags + " +X more"
3. Simplify stats: Icons only, no text labels
4. Stack action buttons vertically

### 4. Form Elements
**Mobile Optimized**:
```html
<!-- Input Field -->
<div class="relative">
  <input 
    type="text"
    class="w-full px-3 py-2.5 text-sm
           bg-white/50 dark:bg-gray-800/50
           border border-gray-200 dark:border-gray-700
           rounded-lg focus:ring-2 focus:ring-primary-500
           focus:border-transparent backdrop-blur-sm
           placeholder:text-gray-400 dark:placeholder:text-gray-500"
    placeholder="Search projects..."
  />
</div>

<!-- Button -->
<button class="px-4 py-2.5 text-sm font-medium
               bg-gradient-to-r from-primary-500 to-primary-600
               text-white rounded-lg hover:from-primary-600 hover:to-primary-700
               transition-all duration-200 active:scale-95
               focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
  Submit
</button>
```

### 5. Modern Design Elements

#### Gradient Borders
```css
.gradient-border {
  position: relative;
  background: linear-gradient(white, white) padding-box,
              linear-gradient(135deg, #667eea, #764ba2) border-box;
  border: 2px solid transparent;
}
```

#### Glassmorphism
```css
.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
```

#### Subtle Gradients
```css
.subtle-gradient {
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.1) 0%,
    rgba(118, 75, 162, 0.05) 100%);
}
```

### 6. Navigation Improvements

#### Bottom Navigation (Mobile)
```html
<nav class="fixed bottom-0 left-0 right-0 
            bg-white/90 dark:bg-gray-900/90 
            backdrop-blur-lg border-t border-gray-200 dark:border-gray-800
            z-50 lg:hidden">
  <div class="flex justify-around items-center h-16">
    <a href="/" class="flex flex-col items-center p-2">
      <svg class="w-5 h-5">...</svg>
      <span class="text-xs mt-1">Home</span>
    </a>
    <!-- More nav items -->
  </div>
</nav>
```

#### Simplified Sidebar (Tablet+)
```html
<aside class="hidden lg:block w-64">
  <!-- Simplified content with fewer icons -->
</aside>
```

## Implementation Steps

### Step 1: Update Tailwind Config
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      backdropBlur: {
        xs: '2px',
      },
    }
  }
}
```

### Step 2: Create Utility Classes
Add to main.css:
```css
@layer utilities {
  .glass-effect {
    @apply bg-white/70 dark:bg-gray-900/70 backdrop-blur-md;
  }
  
  .gradient-text {
    @apply bg-gradient-to-r from-primary-500 to-purple-600 bg-clip-text text-transparent;
  }
  
  .hover-lift {
    @apply transition-transform duration-200 hover:-translate-y-1;
  }
}
```

### Step 3: Component Refactoring Order
1. Update all card components with responsive padding
2. Implement stats card redesign
3. Update project cards with collapsed tags
4. Optimize form elements
5. Add modern design elements (gradients, glass effects)
6. Implement bottom navigation

### Step 4: Testing
- Test on mobile viewports (320px, 375px, 425px)
- Verify touch targets are at least 44x44px
- Check contrast ratios for accessibility
- Test dark mode compatibility