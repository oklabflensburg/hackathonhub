<template>
  <div class="dashboard-page">
    <!-- Page header -->
    <div class="page-header mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
        Dashboard
      </h1>
      <p class="mt-2 text-gray-600 dark:text-gray-400">
        Welcome back! Here's what's happening with your hackathons and projects.
      </p>
    </div>

    <!-- Stats overview -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Active hackathons -->
      <DashboardWidget
        title="Active Hackathons"
        subtitle="Currently participating"
        icon="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' /></svg>"
        variant="primary"
        show-footer
        footer-text="Updated today"
      >
        <template #default>
          <div class="text-center py-6">
            <div class="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              3
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              +1 from last week
            </div>
          </div>
        </template>
      </DashboardWidget>

      <!-- Projects submitted -->
      <DashboardWidget
        title="Projects Submitted"
        subtitle="Total this month"
        icon="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' /></svg>"
        variant="success"
        show-footer
        footer-text="Last submission: 2 days ago"
      >
        <template #default>
          <div class="text-center py-6">
            <div class="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              12
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              +3 from last month
            </div>
          </div>
        </template>
      </DashboardWidget>

      <!-- Team members -->
      <DashboardWidget
        title="Team Members"
        subtitle="Across all teams"
        icon="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a5.5 5.5 0 11-11 0 5.5 5.5 0 0111 0z' /></svg>"
        variant="info"
        show-footer
        footer-text="Active: 8/12"
      >
        <template #default>
          <div class="text-center py-6">
            <div class="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              12
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              Across 3 teams
            </div>
          </div>
        </template>
      </DashboardWidget>

      <!-- Upcoming deadlines -->
      <DashboardWidget
        title="Upcoming Deadlines"
        subtitle="Next 7 days"
        icon="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' /></svg>"
        variant="warning"
        show-footer
        footer-text="Closest: Tomorrow"
      >
        <template #default>
          <div class="text-center py-6">
            <div class="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              2
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              Project submissions
            </div>
          </div>
        </template>
      </DashboardWidget>
    </div>

    <!-- Main content grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left column -->
      <div class="lg:col-span-2 space-y-8">
        <!-- Recent activity -->
        <DashboardWidget
          title="Recent Activity"
          subtitle="Latest updates from your hackathons"
          variant="default"
          show-footer
          show-view-all
          @view-all="$router.push('/activity')"
        >
          <template #default>
            <div class="space-y-4">
              <div v-for="activity in recentActivities" :key="activity.id" class="flex items-start p-3 hover:bg-gray-50 dark:hover:bg-gray-800/50 rounded-lg">
                <div class="flex-shrink-0">
                  <div class="w-10 h-10 rounded-full flex items-center justify-center" :class="activity.iconClasses">
                    <Icon
                      :name="activity.icon"
                      :size="20"
                      is-svg
                      class="text-white"
                    />
                  </div>
                </div>
                <div class="ml-3 flex-1">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ activity.message }}
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {{ activity.time }}
                  </p>
                </div>
                <Badge :variant="activity.badgeVariant" size="sm">
                  {{ activity.badge }}
                </Badge>
              </div>
            </div>
          </template>
        </DashboardWidget>

        <!-- Active projects -->
        <DashboardWidget
          title="Active Projects"
          subtitle="Projects you're currently working on"
          variant="default"
          show-footer
          show-view-all
          @view-all="$router.push('/projects')"
        >
          <template #default>
            <div class="space-y-4">
              <div v-for="project in activeProjects" :key="project.id" class="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-gray-800/50 rounded-lg">
                <div class="flex items-center">
                  <div class="w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                    <Icon
                      name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' /></svg>"
                      :size="20"
                      is-svg
                      class="text-primary-600 dark:text-primary-400"
                    />
                  </div>
                  <div class="ml-3">
                    <h4 class="text-sm font-medium text-gray-900 dark:text-white">
                      {{ project.name }}
                    </h4>
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      {{ project.hackathon }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <ProgressBar
                    :value="project.progress"
                    size="sm"
                    :show-value="true"
                  />
                  <Badge :variant="project.statusVariant" size="sm">
                    {{ project.status }}
                  </Badge>
                </div>
              </div>
            </div>
          </template>
        </DashboardWidget>
      </div>

      <!-- Right column -->
      <div class="space-y-8">
        <!-- Quick actions -->
        <DashboardWidget
          title="Quick Actions"
          subtitle="Things you can do right now"
          variant="default"
        >
          <template #default>
            <div class="space-y-3">
              <button
                v-for="action in quickActions"
                :key="action.id"
                class="w-full flex items-center justify-between p-3 text-left rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                @click="handleQuickAction(action)"
              >
                <div class="flex items-center">
                  <div class="w-8 h-8 rounded-lg flex items-center justify-center" :class="action.iconClasses">
                    <Icon
                      :name="action.icon"
                      :size="16"
                      is-svg
                      class="text-white"
                    />
                  </div>
                  <div class="ml-3">
                    <h4 class="text-sm font-medium text-gray-900 dark:text-white">
                      {{ action.title }}
                    </h4>
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      {{ action.description }}
                    </p>
                  </div>
                </div>
                <Icon
                  name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 5l7 7-7 7' /></svg>"
                  :size="16"
                  is-svg
                  class="text-gray-400"
                />
              </button>
            </div>
          </template>
        </DashboardWidget>

        <!-- Notifications preview -->
        <DashboardWidget
          title="Notifications"
          :unread-count="3"
          variant="default"
          show-footer
          show-view-all
          @view-all="$router.push('/notifications')"
        >
          <template #default>
            <div class="space-y-3">
              <div v-for="notification in notifications" :key="notification.id" class="flex items-start p-3 hover:bg-gray-50 dark:hover:bg-gray-800/50 rounded-lg">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 rounded-full flex items-center justify-center" :class="notification.iconClasses">
                    <Icon
                      :name="notification.icon"
                      :size="14"
                      is-svg
                      class="text-white"
                    />
                  </div>
                </div>
                <div class="ml-3 flex-1">
                  <p class="text-sm text-gray-900 dark:text-white">
                    {{ notification.message }}
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {{ notification.time }}
                  </p>
                </div>
                <div v-if="!notification.read" class="w-2 h-2 rounded-full bg-primary-500"></div>
              </div>
            </div>
          </template>
        </DashboardWidget>

        <!-- Upcoming events -->
        <DashboardWidget
          title="Upcoming Events"
          subtitle="Hackathons starting soon"
          variant="default"
          show-footer
          show-view-all
          @view-all="$router.push('/hackathons')"
        >
          <template #default>
            <div class="space-y-4">
              <div v-for="event in upcomingEvents" :key="event.id" class="p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="text-sm font-medium text-gray-900 dark:text-white">
                      {{ event.name }}
                    </h4>
                    <div class="flex items-center mt-1 text-xs text-gray-500 dark:text-gray-400">
                      <Icon
                        name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' /></svg>"
                        :size="12"
                        is-svg
                        class="mr-1"
                      />
                      {{ event.date }}
                    </div>
                  </div>
                  <Badge :variant="event.badgeVariant">
                    {{ event.status }}
                  </Badge>
                </div>
                <div class="mt-3 flex items-center justify-between">
                  <div class="flex items-center text-xs text-gray-500 dark:text-gray-400">
                    <Icon
                      name="<svg fill='none' stroke='currentColor' viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z' /><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 11a3 3 0 11-6 0 3 3 0 016 0z' /></svg>"
                      :size="12"
                      is-svg
                      class="mr-1"
                    />
                    {{ event.location }}
                  </div>
                  <button
                    class="text-xs font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
                    @click="viewEvent(event)"
                  >
                    View Details
                  </button>
                </div>
              </div>
            </div>
          </template>
        </DashboardWidget>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import DashboardWidget from '~/components/organisms/dashboard/DashboardWidget.vue'
import Icon from '~/components/atoms/Icon.vue'
import Badge from '~/components/atoms/Badge.vue'
import ProgressBar from '~/components/atoms/ProgressBar.vue'

// Mock data for the dashboard
const recentActivities = [
  {
    id: 1,
    icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    iconClasses: 'bg-green-500',
    message: 'Your project "EcoTracker" won 1st place in GreenTech Hackathon',
    time: '2 hours ago',
    badge: 'Winner',
    badgeVariant: 'success' as const,
  },
  {
    id: 2,
    icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    iconClasses: 'bg-blue-500',
    message: 'Deadline extended for AI Innovation Challenge',
    time: '1 day ago',
    badge: 'Update',
    badgeVariant: 'info' as const,
  },
  {
    id: 3,
    icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" /></svg>',
    iconClasses: 'bg-purple-500',
    message: 'John Doe joined your team "CodeCrafters"',
    time: '2 days ago',
    badge: 'Team',
    badgeVariant: 'secondary' as const,
  },
]

const activeProjects = [
  {
    id: 1,
    name: 'EcoTracker',
    hackathon: 'GreenTech Hackathon',
    progress: 85,
    status: 'In Progress',
    statusVariant: 'primary' as const,
  },
  {
    id: 2,
    name: 'AI Assistant',
    hackathon: 'AI Innovation Challenge',
    progress: 45,
    status: 'Needs Work',
    statusVariant: 'warning' as const,
  },
  {
    id: 3,
    name: 'Health Monitor',
    hackathon: 'HealthTech Summit',
    progress: 100,
    status: 'Completed',
    statusVariant: 'success' as const,
  },
]

const quickActions = [
  {
    id: 1,
    title: 'Create New Project',
    description: 'Start a new hackathon project',
    icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>',
    iconClasses: 'bg-primary-500',
  },
  {
    id: 2,
    title: 'Join Hackathon',
    description: 'Find and join upcoming events',
    icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    iconClasses: 'bg-success-500',
  },
  {
    id: 3,
    title: 'Invite Team Members',
    description: 'Collaborate with others',
    icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" /></svg>',
    iconClasses: 'bg-info-500',
  },
]

const notifications = [
  {
    id: 1,
    icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    iconClasses: 'bg-success-500',
    message: 'Your submission was accepted',
    time: '2 hours ago',
    read: false,
  },
  {
    id: 2,
    icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    iconClasses: 'bg-warning-500',
    message: 'Deadline reminder: 2 days left',
    time: '1 day ago',
    read: true,
  },
  {
    id: 3,
    icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" /></svg>',
    iconClasses: 'bg-info-500',
    message: 'New team member joined',
    time: '3 days ago',
    read: true,
  },
]

const upcomingEvents = [
  {
    id: 1,
    name: 'Blockchain Hackathon',
    date: 'Mar 15-17, 2026',
    location: 'Virtual',
    status: 'Upcoming',
    badgeVariant: 'primary' as const,
  },
  {
    id: 2,
    name: 'Web3 Innovation Summit',
    date: 'Apr 5-7, 2026',
    location: 'San Francisco',
    status: 'Registration Open',
    badgeVariant: 'success' as const,
  },
]

// Methods
const handleQuickAction = (action: any) => {
  console.log('Quick action:', action)
  // In a real app, this would navigate or open a modal
}

const viewEvent = (event: any) => {
  console.log('View event:', event)
  // In a real app, this would navigate to the event page
}
</script>

<style scoped>
.dashboard-page {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  padding: 1.5rem 0;
}

@media (max-width: 768px) {
  .dashboard-page {
    padding: 0 1rem;
  }
  
  .page-header {
    padding: 1rem 0;
  }
}
</style>