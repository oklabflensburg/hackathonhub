/**
 * Layout Navigation Composable für Atomic Design Layout-Komponenten
 * Verwaltet Navigation-Zustand, aktive Routes und responsive Navigation
 */

import type { NavigationItem } from '~/types/layout-types'
import { DEFAULT_NAVIGATION_ITEMS, filterNavigationItems, findActiveNavigationItem } from '~/types/layout-types'

/**
 * Navigation State
 */
export interface NavigationState {
  /** Alle Navigationselemente */
  items: NavigationItem[]
  /** Gefilterte Navigationselemente (basierend auf Auth/Rolle) */
  filteredItems: NavigationItem[]
  /** Aktives Navigationselement */
  activeItem: NavigationItem | null
  /** Sidebar zusammengeklappt */
  sidebarCollapsed: boolean
  /** Mobile Navigation sichtbar */
  mobileNavVisible: boolean
  /** Aktuelle Route */
  currentRoute: string
  /** Breakpoint für mobile Navigation */
  mobileBreakpoint: number
  /** Ist mobile Ansicht */
  isMobile: boolean
}

/**
 * Navigation Composable Rückgabetyp
 */
export interface UseLayoutNavigationReturn {
  /** Navigation State */
  state: Ref<NavigationState>
  /** Navigationselemente setzen */
  setNavigationItems: (items: NavigationItem[]) => void
  /** Aktive Route setzen */
  setActiveRoute: (route: string) => void
  /** Sidebar toggle */
  toggleSidebar: () => void
  /** Mobile Navigation toggle */
  toggleMobileNav: () => void
  /** Sidebar öffnen */
  openSidebar: () => void
  /** Sidebar schließen */
  closeSidebar: () => void
  /** Mobile Navigation öffnen */
  openMobileNav: () => void
  /** Mobile Navigation schließen */
  closeMobileNav: () => void
  /** Navigationselemente filtern */
  filterItems: (isAuthenticated: boolean, userRole?: string) => void
  /** Aktives Element finden */
  findActiveItem: (route: string) => NavigationItem | null
  /** Ist Route aktiv */
  isRouteActive: (route: string) => boolean
  /** Responsive Breakpoint prüfen */
  checkMobileBreakpoint: () => void
}

/**
 * Navigation Composable
 */
export function useLayoutNavigation(
  initialItems: NavigationItem[] = DEFAULT_NAVIGATION_ITEMS,
  options: {
    mobileBreakpoint?: number
    initialSidebarCollapsed?: boolean
    initialRoute?: string
  } = {}
): UseLayoutNavigationReturn {
  const {
    mobileBreakpoint = 768,
    initialSidebarCollapsed = false,
    initialRoute = '/',
  } = options

  // SSR-safe Prüfung für Browser-APIs
  const isClient = typeof window !== 'undefined'

  // Zustand
  const state = ref<NavigationState>({
    items: initialItems,
    filteredItems: initialItems,
    activeItem: null,
    sidebarCollapsed: initialSidebarCollapsed,
    mobileNavVisible: false,
    currentRoute: initialRoute,
    mobileBreakpoint,
    isMobile: false,
  })

  // Router für Navigation
  const router = useRouter()
  const route = useRoute()

  // Auth Store (falls verfügbar)
  let authStore: any = null
  
  // Async Funktion zum Laden des Auth Stores
  const loadAuthStore = async () => {
    try {
      // Versuche Auth Store zu importieren
      const { useAuthStore } = await import('~/stores/auth')
      authStore = useAuthStore()
    } catch (error) {
      // Auth Store nicht verfügbar
      console.debug('Auth store not available for navigation filtering')
    }
  }
  
  // Auth Store laden
  if (isClient) {
    loadAuthStore()
  }

  // Initialisiere Navigation
  onMounted(() => {
    initializeNavigation()
    
    // Responsive Breakpoint überwachen
    if (isClient) {
      checkMobileBreakpoint()
      window.addEventListener('resize', checkMobileBreakpoint)
    }
  })

  // Cleanup
  onUnmounted(() => {
    if (isClient) {
      window.removeEventListener('resize', checkMobileBreakpoint)
    }
  })

  // Route-Änderungen überwachen
  watch(
    () => route.path,
    (newPath) => {
      setActiveRoute(newPath)
      // Mobile Navigation schließen bei Route-Änderung (auf mobilen Geräten)
      if (state.value.isMobile) {
        closeMobileNav()
      }
    }
  )

  // Auth-Änderungen überwachen (falls Auth Store verfügbar)
  if (authStore) {
    watch(
      () => authStore.user,
      () => {
        filterNavigationBasedOnAuth()
      },
      { deep: true }
    )
  }

  /**
   * Navigation initialisieren
   */
  function initializeNavigation(): void {
    // Aktuelle Route setzen
    setActiveRoute(route.path)
    
    // Navigation basierend auf Auth filtern
    filterNavigationBasedOnAuth()
    
    // Responsive State prüfen
    checkMobileBreakpoint()
  }

  /**
   * Navigation basierend auf Auth filtern
   */
  function filterNavigationBasedOnAuth(): void {
    if (!authStore) {
      // Kein Auth Store, alle Items anzeigen
      state.value.filteredItems = state.value.items
      return
    }

    const isAuthenticated = !!authStore.user
    const userRole = authStore.user?.role
    
    filterItems(isAuthenticated, userRole)
  }

  /**
   * Navigationselemente setzen
   */
  function setNavigationItems(items: NavigationItem[]): void {
    state.value.items = items
    filterNavigationBasedOnAuth()
    
    // Aktives Item neu berechnen
    if (state.value.currentRoute) {
      state.value.activeItem = findActiveNavigationItem(items, state.value.currentRoute) || null
    }
  }

  /**
   * Aktive Route setzen
   */
  function setActiveRoute(route: string): void {
    state.value.currentRoute = route
    state.value.activeItem = findActiveNavigationItem(state.value.filteredItems, route) || null
  }

  /**
   * Navigationselemente filtern
   */
  function filterItems(isAuthenticated: boolean, userRole?: string): void {
    state.value.filteredItems = filterNavigationItems(
      state.value.items,
      isAuthenticated,
      userRole
    )
    
    // Aktives Item neu berechnen
    if (state.value.currentRoute) {
      state.value.activeItem = findActiveNavigationItem(state.value.filteredItems, state.value.currentRoute) || null
    }
  }

  /**
   * Aktives Element finden
   */
  function findActiveItem(route: string): NavigationItem | null {
    return findActiveNavigationItem(state.value.filteredItems, route) || null
  }

  /**
   * Ist Route aktiv
   */
  function isRouteActive(routeToCheck: string): boolean {
    if (!state.value.currentRoute) return false
    
    // Exakte Übereinstimmung
    if (state.value.currentRoute === routeToCheck) {
      return true
    }
    
    // Child Route (z.B. /projects/123 ist Child von /projects)
    if (state.value.currentRoute.startsWith(routeToCheck + '/')) {
      return true
    }
    
    return false
  }

  /**
   * Responsive Breakpoint prüfen
   */
  function checkMobileBreakpoint(): void {
    if (!isClient) {
      state.value.isMobile = false
      return
    }
    
    const isMobile = window.innerWidth < state.value.mobileBreakpoint
    state.value.isMobile = isMobile
    
    // Sidebar automatisch schließen/öffnen basierend auf Breakpoint
    if (isMobile && !state.value.sidebarCollapsed) {
      state.value.sidebarCollapsed = true
    } else if (!isMobile && state.value.sidebarCollapsed) {
      state.value.sidebarCollapsed = false
    }
  }

  /**
   * Sidebar toggle
   */
  function toggleSidebar(): void {
    state.value.sidebarCollapsed = !state.value.sidebarCollapsed
  }

  /**
   * Mobile Navigation toggle
   */
  function toggleMobileNav(): void {
    state.value.mobileNavVisible = !state.value.mobileNavVisible
  }

  /**
   * Sidebar öffnen
   */
  function openSidebar(): void {
    state.value.sidebarCollapsed = false
  }

  /**
   * Sidebar schließen
   */
  function closeSidebar(): void {
    state.value.sidebarCollapsed = true
  }

  /**
   * Mobile Navigation öffnen
   */
  function openMobileNav(): void {
    state.value.mobileNavVisible = true
  }

  /**
   * Mobile Navigation schließen
   */
  function closeMobileNav(): void {
    state.value.mobileNavVisible = false
  }

  /**
   * Zu Route navigieren
   */
  function navigateTo(route: string): void {
    router.push(route)
  }

  return {
    state,
    setNavigationItems,
    setActiveRoute,
    toggleSidebar,
    toggleMobileNav,
    openSidebar,
    closeSidebar,
    openMobileNav,
    closeMobileNav,
    filterItems,
    findActiveItem,
    isRouteActive,
    checkMobileBreakpoint,
  }
}

/**
 * Vereinfachter Navigation Hook für Komponenten
 */
export function useNavigation() {
  const navigation = useLayoutNavigation()
  
  return {
    navigationItems: computed(() => navigation.state.value.filteredItems),
    activeItem: computed(() => navigation.state.value.activeItem),
    sidebarCollapsed: computed(() => navigation.state.value.sidebarCollapsed),
    mobileNavVisible: computed(() => navigation.state.value.mobileNavVisible),
    isMobile: computed(() => navigation.state.value.isMobile),
    toggleSidebar: navigation.toggleSidebar,
    toggleMobileNav: navigation.toggleMobileNav,
    isRouteActive: navigation.isRouteActive,
    navigateTo: (route: string) => {
      navigation.setActiveRoute(route)
      // In einer echten Implementierung würden wir den Router verwenden
      console.log(`Navigate to: ${route}`)
    },
  }
}