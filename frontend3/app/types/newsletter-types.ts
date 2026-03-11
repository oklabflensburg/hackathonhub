/**
 * Newsletter TypeScript Types for Atomic Design Components
 * 
 * This file defines all TypeScript interfaces and enums for newsletter components
 * Used across atoms, molecules, organisms, templates, and composables
 */

// ==================== ENUMS ====================

/**
 * Newsletter status enum
 */
export enum NewsletterStatus {
  DRAFT = 'draft',
  SCHEDULED = 'scheduled',
  SENDING = 'sending',
  SENT = 'sent',
  CANCELLED = 'cancelled',
  FAILED = 'failed'
}

/**
 * Newsletter frequency enum
 */
export enum NewsletterFrequency {
  DAILY = 'daily',
  WEEKLY = 'weekly',
  BIWEEKLY = 'biweekly',
  MONTHLY = 'monthly',
  QUARTERLY = 'quarterly',
  YEARLY = 'yearly',
  ON_DEMAND = 'on_demand'
}

/**
 * Newsletter category enum
 */
export enum NewsletterCategory {
  GENERAL = 'general',
  TECHNICAL = 'technical',
  COMMUNITY = 'community',
  EVENTS = 'events',
  PRODUCT_UPDATES = 'product_updates',
  TUTORIALS = 'tutorials',
  ANNOUNCEMENTS = 'announcements',
  PROMOTIONAL = 'promotional'
}

/**
 * Newsletter subscription status enum
 */
export enum NewsletterSubscriptionStatus {
  SUBSCRIBED = 'subscribed',
  UNSUBSCRIBED = 'unsubscribed',
  PENDING = 'pending',
  BOUNCED = 'bounced',
  COMPLAINED = 'complained'
}

// ==================== INTERFACES ====================

/**
 * Newsletter issue interface
 */
export interface NewsletterIssue {
  id: string
  title: string
  subject: string
  content: string
  excerpt?: string | null
  status: NewsletterStatus
  category: NewsletterCategory
  sentAt: string | null
  scheduledFor: string | null
  sentCount: number
  openedCount: number
  clickedCount: number
  bounceCount: number
  unsubscribeCount: number
  complaintCount: number
  createdAt: string
  updatedAt: string
  createdBy: string
  tags: string[]
  metadata?: Record<string, any>
  previewUrl?: string | null
}

/**
 * Newsletter subscription interface
 */
export interface NewsletterSubscription {
  id: string
  userId: string
  email: string
  status: NewsletterSubscriptionStatus
  categories: NewsletterCategory[]
  frequency: NewsletterFrequency
  subscribedAt: string
  unsubscribedAt: string | null
  lastSentAt: string | null
  openedCount: number
  clickedCount: number
  bounceCount: number
  metadata?: Record<string, any>
  preferences?: NewsletterPreferences
}

/**
 * Newsletter preferences interface
 */
export interface NewsletterPreferences {
  userId: string
  email: string
  categories: NewsletterCategory[]
  frequency: NewsletterFrequency
  receivePromotional: boolean
  receiveCommunityUpdates: boolean
  receiveEventNotifications: boolean
  receiveProductUpdates: boolean
  receiveTutorials: boolean
  language: string
  timezone: string
  createdAt: string
  updatedAt: string
}

/**
 * Newsletter creation data
 */
export interface NewsletterCreateData {
  title: string
  subject: string
  content: string
  excerpt?: string | null
  category: NewsletterCategory
  scheduledFor?: string | null
  tags?: string[]
  metadata?: Record<string, any>
}

/**
 * Newsletter update data
 */
export interface NewsletterUpdateData {
  title?: string
  subject?: string
  content?: string
  excerpt?: string | null
  category?: NewsletterCategory
  status?: NewsletterStatus
  scheduledFor?: string | null
  tags?: string[]
  metadata?: Record<string, any>
}

/**
 * Newsletter subscription data
 */
export interface NewsletterSubscriptionData {
  email: string
  categories?: NewsletterCategory[]
  frequency?: NewsletterFrequency
  preferences?: Partial<NewsletterPreferences>
}

/**
 * Newsletter preferences update data
 */
export interface NewsletterPreferencesUpdateData {
  categories?: NewsletterCategory[]
  frequency?: NewsletterFrequency
  receivePromotional?: boolean
  receiveCommunityUpdates?: boolean
  receiveEventNotifications?: boolean
  receiveProductUpdates?: boolean
  receiveTutorials?: boolean
  language?: string
  timezone?: string
}

/**
 * Newsletter filter options
 */
export interface NewsletterFilterOptions {
  status?: NewsletterStatus[]
  category?: NewsletterCategory[]
  search?: string
  startDate?: string
  endDate?: string
  sent?: boolean
  scheduled?: boolean
  createdBy?: string
  tags?: string[]
  page?: number
  pageSize?: number
  sortBy?: 'newest' | 'oldest' | 'title' | 'sent_at' | 'scheduled_for'
}

/**
 * Newsletter pagination response
 */
export interface NewsletterPaginationResponse {
  newsletters: NewsletterIssue[]
  totalCount: number
  page: number
  pageSize: number
  totalPages: number
  hasMore: boolean
}

/**
 * Newsletter statistics
 */
export interface NewsletterStatistics {
  totalSubscribers: number
  activeSubscribers: number
  totalNewsletters: number
  sentNewsletters: number
  scheduledNewsletters: number
  averageOpenRate: number
  averageClickRate: number
  averageBounceRate: number
  averageUnsubscribeRate: number
  topCategories: Array<{
    category: NewsletterCategory
    count: number
    openRate: number
  }>
  recentActivity: Array<{
    date: string
    sent: number
    opened: number
    clicked: number
  }>
}

// ==================== COMPONENT PROPS ====================

/**
 * Newsletter subscription form props
 */
export interface NewsletterSubscriptionFormProps {
  initialEmail?: string
  initialCategories?: NewsletterCategory[]
  initialFrequency?: NewsletterFrequency
  showCategories?: boolean
  showFrequency?: boolean
  compact?: boolean
  loading?: boolean
  disabled?: boolean
  onSubmit: (data: NewsletterSubscriptionData) => Promise<void> | void
  onCancel?: () => void
}

/**
 * Newsletter preferences form props
 */
export interface NewsletterPreferencesFormProps {
  preferences: NewsletterPreferences
  loading?: boolean
  saving?: boolean
  disabled?: boolean
  onSubmit: (data: NewsletterPreferencesUpdateData) => Promise<void> | void
  onReset?: () => void
  onUnsubscribe?: () => void
}

/**
 * Newsletter issue card props
 */
export interface NewsletterIssueCardProps {
  newsletter: NewsletterIssue
  showStatus?: boolean
  showStats?: boolean
  showActions?: boolean
  compact?: boolean
  onView?: (newsletterId: string) => void
  onEdit?: (newsletterId: string) => void
  onDelete?: (newsletterId: string) => void
  onSend?: (newsletterId: string) => void
  onSchedule?: (newsletterId: string, date: string) => void
}

/**
 * Newsletter statistics card props
 */
export interface NewsletterStatisticsCardProps {
  statistics: NewsletterStatistics
  loading?: boolean
  showDetails?: boolean
  period?: 'day' | 'week' | 'month' | 'year' | 'all'
  onPeriodChange?: (period: 'day' | 'week' | 'month' | 'year' | 'all') => void
}

/**
 * Newsletter preview props
 */
export interface NewsletterPreviewProps {
  newsletter: NewsletterIssue
  showHeader?: boolean
  showFooter?: boolean
  showActions?: boolean
  onClose?: () => void
  onSendTest?: () => void
  onSchedule?: () => void
  onSendNow?: () => void
}

// ==================== COMPOSABLE RETURN TYPES ====================

/**
 * UseNewsletter composable return type
 */
export interface UseNewsletterReturn {
  newsletters: Ref<NewsletterIssue[]>
  loading: Ref<boolean>
  error: Ref<string | null>
  totalCount: Ref<number>
  page: Ref<number>
  pageSize: Ref<number>
  filters: Ref<Partial<NewsletterFilterOptions>>
  
  fetchNewsletters: (options?: NewsletterFilterOptions) => Promise<void>
  fetchNewsletter: (newsletterId: string) => Promise<NewsletterIssue | null>
  createNewsletter: (data: NewsletterCreateData) => Promise<NewsletterIssue | null>
  updateNewsletter: (newsletterId: string, data: NewsletterUpdateData) => Promise<NewsletterIssue | null>
  deleteNewsletter: (newsletterId: string) => Promise<boolean>
  sendNewsletter: (newsletterId: string) => Promise<boolean>
  scheduleNewsletter: (newsletterId: string, scheduledFor: string) => Promise<boolean>
  cancelNewsletter: (newsletterId: string) => Promise<boolean>
  getStatistics: () => Promise<NewsletterStatistics | null>
  resetNewsletters: () => void
}

/**
 * UseNewsletterSubscription composable return type
 */
export interface UseNewsletterSubscriptionReturn {
  subscription: Ref<NewsletterSubscription | null>
  preferences: Ref<NewsletterPreferences | null>
  loading: Ref<boolean>
  error: Ref<string | null>
  saving: Ref<boolean>
  
  fetchSubscription: (email?: string) => Promise<void>
  subscribe: (data: NewsletterSubscriptionData) => Promise<boolean>
  unsubscribe: (email?: string) => Promise<boolean>
  updatePreferences: (data: NewsletterPreferencesUpdateData) => Promise<boolean>
  isSubscribed: () => boolean
  getSubscriptionStatus: () => NewsletterSubscriptionStatus | null
  resetSubscription: () => void
}

// ==================== UTILITY TYPES ====================

/**
 * Newsletter category filter props
 */
export interface NewsletterCategoryFilterProps {
  selectedCategories: NewsletterCategory[]
  onChange: (categories: NewsletterCategory[]) => void
  disabled?: boolean
}

/**
 * Newsletter frequency selector props
 */
export interface NewsletterFrequencySelectorProps {
  frequency: NewsletterFrequency
  onChange: (frequency: NewsletterFrequency) => void
  disabled?: boolean
}

// ==================== UTILITY CONSTANTS ====================

/**
 * Newsletter status labels
 */
export const NEWSLETTER_STATUS_LABELS: Record<NewsletterStatus, string> = {
  [NewsletterStatus.DRAFT]: 'Entwurf',
  [NewsletterStatus.SCHEDULED]: 'Geplant',
  [NewsletterStatus.SENDING]: 'Wird gesendet',
  [NewsletterStatus.SENT]: 'Gesendet',
  [NewsletterStatus.CANCELLED]: 'Abgebrochen',
  [NewsletterStatus.FAILED]: 'Fehlgeschlagen'
}

/**
 * Newsletter status colors
 */
export const NEWSLETTER_STATUS_COLORS: Record<NewsletterStatus, string> = {
  [NewsletterStatus.DRAFT]: 'gray',
  [NewsletterStatus.SCHEDULED]: 'blue',
  [NewsletterStatus.SENDING]: 'yellow',
  [NewsletterStatus.SENT]: 'green',
  [NewsletterStatus.CANCELLED]: 'orange',
  [NewsletterStatus.FAILED]: 'red'
}

/**
 * Newsletter frequency labels
 */
export const NEWSLETTER_FREQUENCY_LABELS: Record<NewsletterFrequency, string> = {
  [NewsletterFrequency.DAILY]: 'Täglich',
  [NewsletterFrequency.WEEKLY]: 'Wöchentlich',
  [NewsletterFrequency.BIWEEKLY]: 'Zweiwöchentlich',
  [NewsletterFrequency.MONTHLY]: 'Monatlich',
  [NewsletterFrequency.QUARTERLY]: 'Vierteljährlich',
  [NewsletterFrequency.YEARLY]: 'Jährlich',
  [NewsletterFrequency.ON_DEMAND]: 'Bei Bedarf'
}

/**
 * Newsletter category labels
 */
export const NEWSLETTER_CATEGORY_LABELS: Record<NewsletterCategory, string> = {
  [NewsletterCategory.GENERAL]: 'Allgemein',
  [NewsletterCategory.TECHNICAL]: 'Technisch',
  [NewsletterCategory.COMMUNITY]: 'Community',
  [NewsletterCategory.EVENTS]: 'Events',
  [NewsletterCategory.PRODUCT_UPDATES]: 'Produkt-Updates',
  [NewsletterCategory.TUTORIALS]: 'Tutorials',
  [NewsletterCategory.ANNOUNCEMENTS]: 'Ankündigungen',
  [NewsletterCategory.PROMOTIONAL]: 'Promotional'
}

/**
 * Newsletter category colors
 */
export const NEWSLETTER_CATEGORY_COLORS: Record<NewsletterCategory, string> = {
  [NewsletterCategory.GENERAL]: 'gray',
  [NewsletterCategory.TECHNICAL]: 'blue',
  [NewsletterCategory.COMMUNITY]: 'green',
  [NewsletterCategory.EVENTS]: 'purple',
  [NewsletterCategory.PRODUCT_UPDATES]: 'orange',
  [NewsletterCategory.TUTORIALS]: 'yellow',
  [NewsletterCategory.ANNOUNCEMENTS]: 'red',
  [NewsletterCategory.PROMOTIONAL]: 'pink'
}

/**
 * Newsletter subscription status labels
 */
export const NEWSLETTER_SUBSCRIPTION_STATUS_LABELS: Record<NewsletterSubscriptionStatus, string> = {
  [NewsletterSubscriptionStatus.SUBSCRIBED]: 'Abonniert',
  [NewsletterSubscriptionStatus.UNSUBSCRIBED]: 'Nicht abonniert',
  [NewsletterSubscriptionStatus.PENDING]: 'Ausstehend',
  [NewsletterSubscriptionStatus.BOUNCED]: 'Bounced',
  [NewsletterSubscriptionStatus.COMPLAINED]: 'Beschwert'
}

/**
 * Newsletter subscription status colors
 */
export const NEWSLETTER_SUBSCRIPTION_STATUS_COLORS: Record<NewsletterSubscriptionStatus, string> = {
  [NewsletterSubscriptionStatus.SUBSCRIBED]: 'green',
  [NewsletterSubscriptionStatus.UNSUBSCRIBED]: 'gray',
  [NewsletterSubscriptionStatus.PENDING]: 'yellow',
  [NewsletterSubscriptionStatus.BOUNCED]: 'orange',
  [NewsletterSubscriptionStatus.COMPLAINED]: 'red'
}