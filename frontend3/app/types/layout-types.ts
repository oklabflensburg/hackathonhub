/**
 * TypeScript-Typen für Layout-Komponenten (Atomic Design Phase 1)
 */

/**
 * Navigation Item für Sidebar und Navigation
 */
export interface NavigationItem {
  /** Eindeutige ID des Navigationselements */
  id: string
  /** Angezeigter Text (wird übersetzt) */
  label: string
  /** Route oder URL */
  to: string
  /** Optionales Icon (Tailwind CSS Klasse oder SVG Name) */
  icon?: string
  /** Badge-Anzahl für Benachrichtigungen */
  badgeCount?: number
  /** Erfordert Authentifizierung */
  requiresAuth?: boolean
  /** Nur für bestimmte Rollen sichtbar */
  roles?: string[]
  /** Externer Link (öffnet in neuem Tab) */
  external?: boolean
  /** Children für verschachtelte Navigation */
  children?: NavigationItem[]
}

/**
 * Benutzer-Menü-Option
 */
export interface UserMenuOption {
  /** Eindeutige ID der Option */
  id: string
  /** Angezeigter Text */
  label: string
  /** Icon (Tailwind CSS Klasse) */
  icon: string
  /** Aktion bei Klick */
  action: () => void
  /** Gefährliche Aktion (rote Farbe) */
  dangerous?: boolean
  /** Separator vor dieser Option */
  separatorBefore?: boolean
}

/**
 * Theme-Zustand
 */
export interface ThemeState {
  /** Aktuelles Theme */
  current: 'light' | 'dark' | 'system'
  /** System-Präferenz */
  systemPreference: 'light' | 'dark'
  /** Theme wurde manuell gesetzt und persistiert */
  persisted: boolean
}

/**
 * Logo Props
 */
export interface LogoProps {
  /** Größe des Logos */
  size?: 'sm' | 'md' | 'lg' | 'xl'
  /** Dark Mode Variante */
  darkMode?: boolean
  /** Als Link behandeln */
  asLink?: boolean
  /** Link-Ziel (falls asLink true) */
  to?: string
}

/**
 * Navigation Link Props
 */
export interface NavigationLinkProps {
  /** Route oder URL */
  to: string
  /** Aktiver Zustand */
  active?: boolean
  /** Icon (optional) */
  icon?: string
  /** Externer Link */
  external?: boolean
  /** Deaktivierter Zustand */
  disabled?: boolean
}

/**
 * Navigation Item Props (Molecule)
 */
export interface NavigationItemProps extends NavigationLinkProps {
  /** Badge-Anzahl */
  badgeCount?: number
  /** Zeige Badge nur wenn > 0 */
  showBadgeOnlyWhenPositive?: boolean
}

/**
 * Theme Toggle Props
 */
export interface ThemeToggleProps {
  /** Initiales Theme */
  initialTheme?: 'light' | 'dark' | 'system'
  /** Zeige Label */
  showLabel?: boolean
  /** Größe */
  size?: 'sm' | 'md' | 'lg'
}

/**
 * User Menu Props
 */
export interface UserMenuProps {
  /** Benutzer-Objekt */
  user?: {
    id: number | string
    username: string
    email?: string
    avatarUrl?: string
    avatar_url?: string
    role?: string
  }
  /** Avatar URL (falls nicht in user enthalten) */
  avatarUrl?: string
  /** Menü-Optionen */
  menuOptions?: UserMenuOption[]
  /** Zeige Email */
  showEmail?: boolean
  /** Ausrichtung des Dropdowns */
  placement?: 'bottom-start' | 'bottom-end' | 'top-start' | 'top-end'
}

/**
 * Sidebar Props
 */
export interface SidebarProps {
  /** Navigationselemente */
  navigationItems: NavigationItem[]
  /** Aktuelle Route */
  currentRoute: string
  /** Benutzer-Objekt */
  user?: UserMenuProps['user']
  /** Zusammengeklappter Zustand */
  collapsed?: boolean
  /** Responsive Breakpoint */
  mobileBreakpoint?: number
  /** Zeige Theme Toggle */
  showThemeToggle?: boolean
  /** Zeige User Menu */
  showUserMenu?: boolean
}

/**
 * Mobile Navigation Props
 */
export interface MobileNavigationProps {
  /** Navigationselemente */
  navigationItems: NavigationItem[]
  /** Aktuelle Route */
  currentRoute: string
  /** Sichtbarer Zustand */
  visible?: boolean
  /** Position (bottom oder top) */
  position?: 'bottom' | 'top'
}

/**
 * Header Props
 */
export interface HeaderProps {
  /** Logo Props */
  logo?: LogoProps
  /** Navigationselemente */
  navigationItems?: NavigationItem[]
  /** Aktuelle Route */
  currentRoute?: string
  /** Benutzer-Objekt */
  user?: UserMenuProps['user']
  /** Zeige Suchleiste */
  showSearch?: boolean
  /** Zeige Theme Toggle */
  showThemeToggle?: boolean
  /** Sticky Header */
  sticky?: boolean
  /** Transparenter Hintergrund */
  transparent?: boolean
}

/**
 * Footer Props
 */
export interface FooterProps {
  /** Footer-Links gruppiert */
  linkGroups?: Array<{
    title: string
    links: NavigationItem[]
  }>
  /** Copyright Text */
  copyright?: string
  /** Social Media Links */
  socialLinks?: Array<{
    platform: string
    url: string
    icon: string
  }>
  /** Zeige Newsletter-Formular */
  showNewsletter?: boolean
}

/**
 * Layout Config
 */
export interface LayoutConfig {
  /** Header Konfiguration */
  header?: HeaderProps
  /** Sidebar Konfiguration */
  sidebar?: SidebarProps
  /** Footer Konfiguration */
  footer?: FooterProps
  /** Mobile Navigation Konfiguration */
  mobileNav?: MobileNavigationProps
  /** Container-Klasse für Hauptinhalt */
  containerClass?: string
  /** Padding für Hauptinhalt */
  contentPadding?: string
}

/**
 * Hilfsfunktionen
 */

/**
 * Prüft ob ein Navigationselement sichtbar sein sollte
 */
export function shouldShowNavigationItem(
  item: NavigationItem,
  isAuthenticated: boolean,
  userRole?: string
): boolean {
  // Prüfe Authentifizierung
  if (item.requiresAuth && !isAuthenticated) {
    return false
  }

  // Prüfe Rollen
  if (item.roles && item.roles.length > 0) {
    if (!userRole || !item.roles.includes(userRole)) {
      return false
    }
  }

  return true
}

/**
 * Filtert Navigationselemente basierend auf Authentifizierung und Rolle
 */
export function filterNavigationItems(
  items: NavigationItem[],
  isAuthenticated: boolean,
  userRole?: string
): NavigationItem[] {
  return items
    .filter(item => shouldShowNavigationItem(item, isAuthenticated, userRole))
    .map(item => ({
      ...item,
      children: item.children
        ? filterNavigationItems(item.children, isAuthenticated, userRole)
        : undefined
    }))
}

/**
 * Findet aktives Navigationselement
 */
export function findActiveNavigationItem(
  items: NavigationItem[],
  currentRoute: string
): NavigationItem | undefined {
  for (const item of items) {
    // Prüfe aktuelles Item
    if (item.to === currentRoute || currentRoute.startsWith(item.to + '/')) {
      return item
    }

    // Prüfe Children rekursiv
    if (item.children) {
      const childActive = findActiveNavigationItem(item.children, currentRoute)
      if (childActive) {
        return childActive
      }
    }
  }

  return undefined
}

/**
 * Theme-Hilfsfunktionen
 */

/**
 * Ermittelt System-Theme-Präferenz
 */
export function getSystemThemePreference(): 'light' | 'dark' {
  if (typeof window === 'undefined') {
    return 'light'
  }

  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

/**
 * Wendet Theme auf Document an
 */
export function applyThemeToDocument(theme: 'light' | 'dark'): void {
  if (typeof document === 'undefined') {
    return
  }

  const root = document.documentElement
  root.classList.remove('light', 'dark')
  root.classList.add(theme)
  root.setAttribute('data-theme', theme)
}

/**
 * Speichert Theme in localStorage
 */
export function persistTheme(theme: 'light' | 'dark' | 'system'): void {
  if (typeof localStorage === 'undefined') {
    return
  }

  localStorage.setItem('theme', theme)
}

/**
 * Lädt Theme aus localStorage
 */
export function loadPersistedTheme(): 'light' | 'dark' | 'system' | null {
  if (typeof localStorage === 'undefined') {
    return null
  }

  const theme = localStorage.getItem('theme')
  if (theme === 'light' || theme === 'dark' || theme === 'system') {
    return theme
  }

  return null
}

/**
 * Standard-Navigationselemente für die Anwendung
 */
export const DEFAULT_NAVIGATION_ITEMS: NavigationItem[] = [
  {
    id: 'home',
    label: 'navigation.home',
    to: '/',
    icon: 'home',
  },
  {
    id: 'hackathons',
    label: 'navigation.hackathons',
    to: '/hackathons',
    icon: 'trophy',
  },
  {
    id: 'projects',
    label: 'navigation.projects',
    to: '/projects',
    icon: 'code',
  },
  {
    id: 'teams',
    label: 'navigation.teams',
    to: '/teams',
    icon: 'users',
    requiresAuth: true,
  },
  {
    id: 'users',
    label: 'navigation.users',
    to: '/users',
    icon: 'user',
  },
  {
    id: 'admin-users',
    label: 'navigation.adminUsers',
    to: '/admin/users',
    icon: 'shield-check',
    requiresAuth: true,
    roles: ['superuser'],
  },
  {
    id: 'my-profile',
    label: 'navigation.myProfile',
    to: '/profile',
    icon: 'user-circle',
    requiresAuth: true,
  },
  {
    id: 'my-projects',
    label: 'navigation.myProjects',
    to: '/my-projects',
    icon: 'folder',
    requiresAuth: true,
  },
  {
    id: 'notifications',
    label: 'navigation.notifications',
    to: '/notifications',
    icon: 'bell',
    requiresAuth: true,
    badgeCount: 0, // Wird dynamisch gesetzt
  },
]

/**
 * Standard-User-Menü-Optionen
 */
export const DEFAULT_USER_MENU_OPTIONS: UserMenuOption[] = [
  {
    id: 'profile',
    label: 'userMenu.profile',
    icon: 'user',
    action: () => {
      // Wird in Komponente überschrieben
      console.log('Profile clicked')
    },
  },
  {
    id: 'settings',
    label: 'userMenu.settings',
    icon: 'cog',
    action: () => {
      console.log('Settings clicked')
    },
  },
  {
    id: 'separator-1',
    label: '',
    icon: '',
    action: () => {},
    separatorBefore: true,
  },
  {
    id: 'logout',
    label: 'userMenu.logout',
    icon: 'logout',
    action: () => {
      console.log('Logout clicked')
    },
    dangerous: true,
  },
]

export type {
  NavigationItem as NavigationItemType,
  UserMenuOption as UserMenuOptionType,
  ThemeState as ThemeStateType,
}
