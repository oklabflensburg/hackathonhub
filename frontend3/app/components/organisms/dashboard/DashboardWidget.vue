<template>
  <div class="dashboard-widget" :class="widgetClasses">
    <!-- Widget header -->
    <div class="widget-header" :class="headerClasses">
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <div v-if="icon" class="widget-icon" :class="iconClasses">
            <Icon
              :name="icon"
              :size="iconSize"
              :is-svg="isSvgIcon"
            />
          </div>
          
          <div class="ml-3">
            <h3 class="widget-title" :class="titleClasses">
              {{ title }}
            </h3>
            <p v-if="subtitle" class="widget-subtitle" :class="subtitleClasses">
              {{ subtitle }}
            </p>
          </div>
        </div>
        
        <div class="flex items-center space-x-2">
          <!-- Actions slot -->
          <slot name="actions">
            <button
              v-if="showRefresh"
              type="button"
              class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              @click="$emit('refresh')"
              aria-label="Refresh"
            >
              <Icon
                name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15' /></svg>"
                :size="16"
                is-svg
              />
            </button>
            
            <button
              v-if="showSettings"
              type="button"
              class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              @click="$emit('settings')"
              aria-label="Settings"
            >
              <Icon
                name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' /><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 12a3 3 0 11-6 0 3 3 0 016 0z' /></svg>"
                :size="16"
                is-svg
              />
            </button>
            
            <button
              v-if="showExpand"
              type="button"
              class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              @click="$emit('expand')"
              aria-label="Expand"
            >
              <Icon
                name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5v-4m0 4h-4m4 0l-5-5' /></svg>"
                :size="16"
                is-svg
              />
            </button>
          </slot>
        </div>
      </div>
    </div>

    <!-- Widget content -->
    <div class="widget-content" :class="contentClasses">
      <!-- Loading state -->
      <div v-if="loading" class="widget-loading">
        <div class="flex flex-col items-center justify-center py-12">
          <div class="w-12 h-12 mb-4">
            <Skeleton variant="circle" size="lg" />
          </div>
          <Skeleton class="w-32 h-4 mb-2" />
          <Skeleton class="w-24 h-3" />
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="widget-error">
        <div class="flex flex-col items-center justify-center py-12 text-center">
          <Icon
            name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' /></svg>"
            :size="48"
            is-svg
            class="text-red-400 mb-4"
          />
          <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
            {{ errorTitle || 'Error loading data' }}
          </h4>
          <p class="text-gray-600 dark:text-gray-400 mb-4">
            {{ errorMessage || 'There was a problem loading this widget.' }}
          </p>
          <button
            v-if="showRetry"
            type="button"
            class="px-4 py-2 text-sm font-medium rounded-md bg-primary-600 text-white hover:bg-primary-700"
            @click="$emit('retry')"
          >
            Try Again
          </button>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else-if="isEmpty" class="widget-empty">
        <div class="flex flex-col items-center justify-center py-12 text-center">
          <Icon
            name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4' /></svg>"
            :size="48"
            is-svg
            class="text-gray-400 mb-4"
          />
          <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
            {{ emptyTitle || 'No data available' }}
          </h4>
          <p class="text-gray-600 dark:text-gray-400 mb-4">
            {{ emptyMessage || 'There is no data to display at the moment.' }}
          </p>
          <slot name="empty-action">
            <button
              v-if="showEmptyAction"
              type="button"
              class="px-4 py-2 text-sm font-medium rounded-md border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
              @click="$emit('empty-action')"
            >
              {{ emptyActionText || 'Add Data' }}
            </button>
          </slot>
        </div>
      </div>

      <!-- Main content -->
      <div v-else class="widget-main">
        <slot>
          <!-- Default slot content -->
          <div class="p-6 text-center text-gray-500 dark:text-gray-400">
            Widget content goes here
          </div>
        </slot>
      </div>
    </div>

    <!-- Widget footer -->
    <div v-if="showFooter" class="widget-footer" :class="footerClasses">
      <slot name="footer">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-500 dark:text-gray-400">
            <slot name="footer-left">
              {{ footerText }}
            </slot>
          </div>
          
          <div class="flex items-center space-x-2">
            <slot name="footer-right">
              <button
                v-if="showViewAll"
                type="button"
                class="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
                @click="$emit('view-all')"
              >
                View All
              </button>
            </slot>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Icon from '../../atoms/Icon.vue'
import Skeleton from '../../atoms/Skeleton.vue'

export interface DashboardWidgetProps {
  /** Widget title */
  title: string
  /** Widget subtitle */
  subtitle?: string
  /** Widget icon (SVG string) */
  icon?: string
  /** Icon size */
  iconSize?: number
  /** Whether icon is SVG */
  isSvgIcon?: boolean
  /** Widget variant */
  variant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info'
  /** Widget size */
  size?: 'sm' | 'md' | 'lg'
  /** Whether widget is loading */
  loading?: boolean
  /** Whether widget has error */
  error?: boolean
  /** Error title */
  errorTitle?: string
  /** Error message */
  errorMessage?: string
  /** Whether widget is empty */
  isEmpty?: boolean
  /** Empty state title */
  emptyTitle?: string
  /** Empty state message */
  emptyMessage?: string
  /** Whether to show footer */
  showFooter?: boolean
  /** Footer text */
  footerText?: string
  /** Whether to show refresh button */
  showRefresh?: boolean
  /** Whether to show settings button */
  showSettings?: boolean
  /** Whether to show expand button */
  showExpand?: boolean
  /** Whether to show retry button in error state */
  showRetry?: boolean
  /** Whether to show empty action button */
  showEmptyAction?: boolean
  /** Empty action button text */
  emptyActionText?: string
  /** Whether to show view all button in footer */
  showViewAll?: boolean
  /** Whether widget is collapsible */
  collapsible?: boolean
  /** Whether widget is initially collapsed */
  collapsed?: boolean
}

const props = withDefaults(defineProps<DashboardWidgetProps>(), {
  variant: 'default',
  size: 'md',
  iconSize: 24,
  isSvgIcon: true,
  showFooter: false,
  showRefresh: false,
  showSettings: false,
  showExpand: false,
  showRetry: true,
  showEmptyAction: false,
  showViewAll: false,
  collapsible: false,
  collapsed: false,
  footerText: 'Last updated: Just now',
})

const emit = defineEmits<{
  /** Emitted when refresh button is clicked */
  refresh: []
  /** Emitted when settings button is clicked */
  settings: []
  /** Emitted when expand button is clicked */
  expand: []
  /** Emitted when retry button is clicked */
  retry: []
  /** Emitted when empty action button is clicked */
  'empty-action': []
  /** Emitted when view all button is clicked */
  'view-all': []
  /** Emitted when widget is collapsed/expanded */
  'update:collapsed': [collapsed: boolean]
}>()

// Computed properties
const widgetClasses = computed(() => {
  const classes = ['rounded-lg', 'shadow-sm', 'overflow-hidden']
  
  // Size classes
  const sizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
  }
  classes.push(sizeClasses[props.size])
  
  // Variant classes for background
  const variantClasses = {
    default: 'bg-white dark:bg-gray-800',
    primary: 'bg-primary-50 dark:bg-primary-900/20',
    secondary: 'bg-secondary-50 dark:bg-secondary-900/20',
    success: 'bg-green-50 dark:bg-green-900/20',
    warning: 'bg-yellow-50 dark:bg-yellow-900/20',
    danger: 'bg-red-50 dark:bg-red-900/20',
    info: 'bg-blue-50 dark:bg-blue-900/20',
  }
  classes.push(variantClasses[props.variant])
  
  return classes
})

const headerClasses = computed(() => {
  const classes = ['px-6', 'py-4', 'border-b']
  
  // Variant classes for header
  const variantClasses = {
    default: 'border-gray-200 dark:border-gray-700',
    primary: 'border-primary-200 dark:border-primary-800',
    secondary: 'border-secondary-200 dark:border-secondary-800',
    success: 'border-green-200 dark:border-green-800',
    warning: 'border-yellow-200 dark:border-yellow-800',
    danger: 'border-red-200 dark:border-red-800',
    info: 'border-blue-200 dark:border-blue-800',
  }
  classes.push(variantClasses[props.variant])
  
  return classes
})

const iconClasses = computed(() => {
  const classes = ['rounded-lg', 'p-2']
  
  // Variant classes for icon
  const variantClasses = {
    default: 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300',
    primary: 'bg-primary-100 dark:bg-primary-800 text-primary-600 dark:text-primary-300',
    secondary: 'bg-secondary-100 dark:bg-secondary-800 text-secondary-600 dark:text-secondary-300',
    success: 'bg-green-100 dark:bg-green-800 text-green-600 dark:text-green-300',
    warning: 'bg-yellow-100 dark:bg-yellow-800 text-yellow-600 dark:text-yellow-300',
    danger: 'bg-red-100 dark:bg-red-800 text-red-600 dark:text-red-300',
    info: 'bg-blue-100 dark:bg-blue-800 text-blue-600 dark:text-blue-300',
  }
  classes.push(variantClasses[props.variant])
  
  return classes
})

const titleClasses = computed(() => {
  const classes = ['font-semibold']
  
  // Variant classes for title
  const variantClasses = {
    default: 'text-gray-900 dark:text-white',
    primary: 'text-primary-900 dark:text-primary-100',
    secondary: 'text-secondary-900 dark:text-secondary-100',
    success: 'text-green-900 dark:text-green-100',
    warning: 'text-yellow-900 dark:text-yellow-100',
    danger: 'text-red-900 dark:text-red-100',
    info: 'text-blue-900 dark:text-blue-100',
  }
  classes.push(variantClasses[props.variant])
  
  return classes
})

const subtitleClasses = computed(() => {
  return 'text-sm text-gray-500 dark:text-gray-400'
})

const contentClasses = computed(() => {
  return 'p-6'
})

const footerClasses = computed(() => {
  const classes = ['px-6', 'py-3', 'border-t']
  
  // Variant classes for footer
  const variantClasses = {
    default: 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50',
    primary: 'border-primary-200 dark:border-primary-800 bg-primary-50/50 dark:bg-primary-900/10',
    secondary: 'border-secondary-200 dark:border-secondary-800 bg-secondary-50/50 dark:bg-secondary-900/10',
    success: 'border-green-200 dark:border-green-800 bg-green-50/50 dark:bg-green-900/10',
    warning: 'border-yellow-200 dark:border-yellow-800 bg-yellow-50/50 dark:bg-yellow-900/10',
    danger: 'border-red-200 dark:border-red-800 bg-red-50/50 dark:bg-red-900/10',
    info: 'border-blue-200 dark:border-blue-800 bg-blue-50/50 dark:bg-blue-900/10',
  }
  classes.push(variantClasses[props.variant])
  
  return classes
})
</script>

<style scoped>
.dashboard-widget {
  transition: all 0.2s ease-in-out;
}

.dashboard-widget:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.widget-header {
  transition: background-color 0.2s ease;
}

.widget-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.widget-title {
  line-height: 1.25;
}

.widget-subtitle {
  line-height: 1.4;
}

.widget-content {
  min-height: 200px;
}

.widget-loading,
.widget-error,
.widget-empty {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .dashboard-widget {
    margin-bottom: 1rem;
  }
  
  .widget-header {
    padding: 0.75rem 1rem;
  }
  
  .widget-content {
    padding: 1rem;
  }
  
  .widget-footer {
    padding: 0.75rem 1rem;
  }
}
</style>