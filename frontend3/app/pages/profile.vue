<template>
  <div class="py-8">
    <!-- Page Header -->
    <div class="mb-8 flex justify-between items-start">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">{{ $t('profile.title') }}</h1>
        <p class="text-gray-600 dark:text-gray-400">{{ $t('profile.subtitle') }}</p>
      </div>
      <div v-if="user && !isEditing">
        <button @click="startEditing"
          class="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          {{ $t('common.edit') }}
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8">
      <!-- Left Column: Profile Info -->
      <div class="lg:col-span-2">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6 mb-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">{{ $t('profile.profileInformation') }}
          </h2>

          <!-- Loading State -->
          <div v-if="loading" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>

          <!-- Profile Display -->
          <ClientOnly>
            <div v-if="user" class="space-y-6">
              <!-- Edit Mode -->
              <div v-if="isEditing">
                <div class="space-y-6">
                  <div class="flex items-start space-x-6 pb-4 border-b border-gray-200 dark:border-gray-700">
                    <div class="relative">
                      <div v-if="user?.avatar_url && !avatarPreview"
                        class="w-24 h-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg">
                        <img :src="user.avatar_url" :alt="user.username" class="w-full h-full object-cover object-top"
                          style="object-position: top" @error="handleAvatarError" />
                      </div>
                      <div v-else-if="avatarPreview"
                        class="w-24 h-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg">
                        <img :src="avatarPreview" :alt="user.username" class="w-full h-full object-cover object-top" />
                      </div>
                      <div v-else
                        class="w-24 h-24 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center border-4 border-white dark:border-gray-800 shadow-lg">
                        <span class="text-3xl font-bold text-primary-600 dark:text-primary-300">
                          {{ userInitials }}
                        </span>
                      </div>
                      <!-- Avatar upload controls -->
                      <div class="absolute -bottom-2 -right-2 flex flex-col space-y-1">
                        <label for="avatar-upload" class="cursor-pointer">
                          <div
                            class="w-8 h-8 rounded-full bg-primary-600 hover:bg-primary-700 flex items-center justify-center shadow-lg transition-colors">
                            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                          </div>
                          <input id="avatar-upload" type="file" accept="image/*" class="hidden"
                            @change="handleAvatarUpload" :disabled="uploadingAvatar" />
                        </label>
                        <button v-if="user?.avatar_url" @click="removeAvatar" :disabled="uploadingAvatar"
                          class="w-8 h-8 rounded-full bg-red-600 hover:bg-red-700 flex items-center justify-center shadow-lg transition-colors">
                          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                      <!-- Upload progress indicator -->
                      <div v-if="uploadingAvatar"
                        class="absolute inset-0 bg-black bg-opacity-50 rounded-full flex items-center justify-center">
                        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
                      </div>
                    </div>
                    <div class="flex-1">
                      <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Edit Profile</h3>
                      <p class="text-gray-600 dark:text-gray-400">{{ user.email }}</p>
                      <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">{{ $t('profile.memberSince') }} {{
                        formatDate(user.created_at) }}</p>
                      <p v-if="uploadingAvatar" class="text-sm text-primary-600 dark:text-primary-400 mt-1">Uploading
                        avatar...</p>
                      <p v-if="uploadError" class="text-sm text-red-600 dark:text-red-400 mt-1">{{ uploadError }}</p>
                    </div>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Username
                      </label>
                      <input v-model="editForm.username" type="text"
                        class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent">
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Display Name
                      </label>
                      <input v-model="editForm.name" type="text"
                        class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        placeholder="Your full name">
                    </div>
                    <div class="md:col-span-2">
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Bio
                      </label>
                      <textarea v-model="editForm.bio" rows="3"
                        class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        placeholder="Tell us about yourself"></textarea>
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Location
                      </label>
                      <input v-model="editForm.location" type="text"
                        class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        placeholder="City, Country">
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Company
                      </label>
                      <input v-model="editForm.company" type="text"
                        class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        placeholder="Your company or organization">
                    </div>
                  </div>

                  <!-- GitHub Connection in Edit Mode -->
                  <div class="pt-6 border-t border-gray-200 dark:border-gray-700">
                    <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">GitHub Connection</h4>
                    <div class="flex items-center justify-between">
                      <div class="flex items-center space-x-3">
                        <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                          <path
                            d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                        </svg>
                        <div>
                          <p class="text-sm font-medium text-gray-900 dark:text-white">
                            {{ user?.github_id ? 'Connected to GitHub' : 'Not connected to GitHub' }}
                          </p>
                          <p class="text-xs text-gray-500 dark:text-gray-400">
                            {{ user?.github_id ? `Connected as ${user.username}` : 'Connect your GitHub account to link
                            your identity' }}
                          </p>
                        </div>
                      </div>
                      <button v-if="!user?.github_id" @click="connectGitHub"
                        class="inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium bg-gray-800 text-white hover:bg-gray-900 dark:bg-gray-700 dark:hover:bg-gray-600 transition-colors">
                        <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
                          <path
                            d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                        </svg>
                        Connect with GitHub
                      </button>
                      <span v-if="user?.github_id"
                        class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                        Connected
                      </span>
                    </div>
                  </div>

                  <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
                    <button @click="cancelEditing" :disabled="saving"
                      class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50">
                      {{ $t('common.cancel') }}
                    </button>
                    <button @click="saveProfile" :disabled="saving"
                      class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 flex items-center">
                      <svg v-if="saving" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none"
                        viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                        </circle>
                        <path class="opacity-75" fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                        </path>
                      </svg>
                      {{ saving ? 'Saving...' : $t('common.save') }}
                    </button>
                  </div>
                </div>
              </div>

              <!-- Display Mode -->
              <div v-else>
                <div class="flex items-start space-x-6">
                  <div class="relative">
                    <div v-if="user?.avatar_url"
                      class="w-24 h-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg">
                      <img :src="user.avatar_url" :alt="user.username" class="w-full h-full object-cover object-top"
                        style="object-position: top" @error="handleAvatarError" />
                    </div>
                    <div v-else
                      class="w-24 h-24 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center border-4 border-white dark:border-gray-800 shadow-lg">
                      <span class="text-3xl font-bold text-primary-600 dark:text-primary-300">
                        {{ userInitials }}
                      </span>
                    </div>
                  </div>
                  <div>
                    <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ user.username }}</h3>
                    <p class="text-gray-600 dark:text-gray-400">{{ user.email }}</p>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">{{ $t('profile.memberSince') }} {{
                      formatDate(user.created_at) }}</p>
                  </div>
                </div>

                <div
                  class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                  <div>
                    <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ $t('profile.githubAccount')
                    }}</h4>
                    <div class="flex items-center justify-start space-x-3">
                      <svg class="w-5 h-5 text-gray-700 dark:text-gray-300 flex-shrink-0" fill="currentColor"
                        viewBox="0 0 24 24">
                        <path
                          d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                      </svg>
                      <span class="text-gray-900 dark:text-white flex-shrink-0">{{ user?.github_id ? user.username :
                        $t('profile.notConnected') }}</span>
                      <span v-if="user?.github_id"
                        class="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                        {{ $t('profile.connected') }}
                      </span>
                      <button v-if="!user?.github_id" @click="connectGitHub"
                        class="ml-2 inline-flex items-center px-3 py-1 rounded-lg text-xs font-medium bg-gray-800 text-white hover:bg-gray-900 dark:bg-gray-700 dark:hover:bg-gray-600 transition-colors">
                        <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 24 24">
                          <path
                            d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                        </svg>
                        {{ $t('profile.connectGitHub') }}
                      </button>
                    </div>
                  </div>

                  <div>
                    <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ $t('profile.accountType')
                      }}
                    </h4>
                    <span
                      class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-300">
                      {{ user.is_admin ? $t('profile.administrator') : $t('profile.standardUser') }}
                    </span>
                  </div>

                  <!-- Additional profile fields -->
                  <div v-if="user.name" class="md:col-span-2">
                    <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Name</h4>
                    <p class="text-gray-900 dark:text-white">{{ user.name }}</p>
                  </div>
                  <div v-if="user.bio" class="md:col-span-2">
                    <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Bio</h4>
                    <p class="text-gray-900 dark:text-white">{{ user.bio }}</p>
                  </div>
                  <div v-if="user.location">
                    <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ $t('profile.location') }}
                    </h4>
                    <p class="text-gray-900 dark:text-white">{{ user.location }}</p>
                  </div>
                  <div v-if="user.company">
                    <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">{{ $t('profile.company') }}
                    </h4>
                    <p class="text-gray-900 dark:text-white">{{ user.company }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- No User State -->
            <div v-else class="text-center py-8">
              <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <p class="text-gray-600 dark:text-gray-400 mb-4">{{ $t('profile.pleaseLogin') }}</p>
              <NuxtLink to="/"
                class="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
                {{ $t('profile.goToLogin') }}
              </NuxtLink>
            </div>
          </ClientOnly>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4 md:gap-6">
          <!-- Hackathons Created Card -->
          <ImprovedStatsCard :label="$t('profile.hackathonsCreated')" :value="stats.hackathonsCreated || 0"
            link="/hackathons?filter=my" :actionText="$t('profile.viewYourHackathons')" :icon="HackathonIcon"
            iconBackground="gradient-blue" />

          <!-- Projects Submitted Card -->
          <ImprovedStatsCard :label="$t('profile.projectsSubmitted')" :value="stats.projectsSubmitted || 0"
            link="/my-projects" :actionText="$t('profile.viewYourProjects')" :icon="ProjectIcon"
            iconBackground="gradient-green" />

          <!-- Total Votes Card -->
          <ImprovedStatsCard :label="$t('profile.totalVotes')" :value="stats.totalVotes || 0" link="/my-votes"
            :actionText="$t('profile.viewYourVotes')" :icon="VoteIcon" iconBackground="gradient-purple" />
        </div>
      </div>

      <!-- Right Column: Actions -->
      <div class="space-y-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-5 lg:p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ $t('profile.quickActions') }}</h3>
          <div class="space-y-3">
            <NuxtLink to="/create"
              class="flex items-center justify-between p-3 rounded-lg bg-primary-50 dark:bg-primary-900/30 hover:bg-primary-100 dark:hover:bg-primary-900/50 transition-colors">
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor"
                  viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <span class="font-medium text-primary-700 dark:text-primary-300">{{ $t('profile.createHackathon')
                }}</span>
              </div>
              <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor"
                viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </NuxtLink>

            <NuxtLink to="/my-projects"
              class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor"
                  viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <span class="font-medium text-gray-700 dark:text-gray-300">{{ $t('profile.viewMyProjects') }}</span>
              </div>
              <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor"
                viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </NuxtLink>

            <NuxtLink to="/my-votes"
              class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor"
                  viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                </svg>
                <span class="font-medium text-gray-700 dark:text-gray-300">{{ $t('profile.viewMyVotes') }}</span>
              </div>
              <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor"
                viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </NuxtLink>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 sm:p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ $t('profile.accountSettings') }}</h3>
          <div class="space-y-4">
            <NuxtLink to="/notifications?tab=preferences"
              class="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/30 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <span class="font-medium">{{ $t('profile.notificationPreferences') }}</span>
            </NuxtLink>

            <button @click="handleLogout"
              class="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span class="font-medium">{{ $t('profile.logOut') }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, h } from 'vue'
import { format } from 'date-fns'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '~/stores/auth'
import { useUIStore } from '~/stores/ui'
import { usePreferencesStore } from '~/stores/preferences'
import ImprovedStatsCard from '~/components/ImprovedStatsCard.vue'
import { uploadFile, createPreviewUrl, validateFile } from '~/utils/fileUpload'

const { t } = useI18n()
const authStore = useAuthStore()
const uiStore = useUIStore()
const preferencesStore = usePreferencesStore()

// Icon components for stats cards using render function
const HackathonIcon = {
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10'
      })
    ])
  }
}

const ProjectIcon = {
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
      })
    ])
  }
}

const VoteIcon = {
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5'
      })
    ])
  }
}

const loading = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const user = computed(() => authStore.user)
const stats = ref({
  hackathonsCreated: 0,
  projectsSubmitted: 0,
  totalVotes: 0
})

const editForm = ref({
  username: '',
  name: '',
  bio: '',
  location: '',
  company: ''
})

// Avatar upload state
const avatarPreview = ref<string | null>(null)
const uploadingAvatar = ref(false)
const uploadError = ref<string | null>(null)

const userInitials = computed(() => {
  return authStore.userInitials
})

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  try {
    return format(new Date(dateString), 'MMM dd, yyyy')
  } catch {
    return dateString
  }
}

const fetchUserProfile = async () => {
  try {
    if (!authStore.isAuthenticated) return

    loading.value = true
    // Fetch full user profile from /api/users/me endpoint
    const response = await authStore.fetchWithAuth('/api/users/me')

    if (response.ok) {
      const userData = await response.json()
      // Update auth store with full user data
      authStore.user = userData
      preferencesStore.auth.setUser(userData)
    } else {
      console.warn('Failed to fetch user profile, using cached data')
    }
  } catch (error) {
    console.warn('Error fetching user profile, using cached data:', error)
  } finally {
    loading.value = false
  }
}

const fetchUserStats = async () => {
  try {
    if (!authStore.isAuthenticated) return

    // Try to fetch user stats from API (endpoint might not exist)
    try {
      const response = await authStore.fetchWithAuth('/api/users/me/stats')

      if (response.ok) {
        stats.value = await response.json()
      } else if (response.status === 404) {
        // Stats endpoint doesn't exist, use placeholder values
        console.warn('Stats endpoint not available, using placeholder values')
        stats.value = {
          hackathonsCreated: 0,
          projectsSubmitted: 0,
          totalVotes: 0
        }
      }
    } catch (error) {
      // Stats endpoint doesn't exist or failed, use placeholder values
      console.warn('Stats endpoint not available, using placeholder values')
      stats.value = {
        hackathonsCreated: 0,
        projectsSubmitted: 0,
        totalVotes: 0
      }
    }
  } catch (error) {
    console.error('Error fetching user stats:', error)
    uiStore.showError('Failed to load profile stats', 'Unable to load your profile statistics. Please try again later.')
  }
}

const handleAvatarError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  // The parent div will show the fallback initials automatically
  // because we're using v-if/v-else
}

const handleAvatarUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files || input.files.length === 0) {
    return
  }

  const file = input.files[0]
  if (!file) {
    return
  }

  // Validate file
  const validationError = validateFile(file, 5) // 5MB max for avatars
  if (validationError) {
    uploadError.value = validationError
    return
  }

  // Create preview
  try {
    avatarPreview.value = await createPreviewUrl(file)
    uploadError.value = null
  } catch (error) {
    uploadError.value = 'Failed to create preview'
    return
  }

  // Upload file
  uploadingAvatar.value = true
  uploadError.value = null

  try {
    // Upload the file
    const result = await uploadFile(file, { type: 'avatar', maxSizeMB: 5 })

    // Update user profile with new avatar URL
    const response = await authStore.fetchWithAuth('/api/users/me', {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ avatar_url: result.url })
    })

    if (response.ok) {
      const updatedUser = await response.json()
      // Update auth store with new user data
      authStore.user = updatedUser
      preferencesStore.auth.setUser(updatedUser)
      uiStore.showSuccess('Avatar updated', 'Your avatar has been successfully updated.')

      // Clear preview after successful update
      avatarPreview.value = null
    } else {
      const errorData = await response.json()
      uploadError.value = errorData.detail || 'Failed to update avatar'
      uiStore.showError('Failed to update avatar', uploadError.value || 'Unknown error')
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Avatar upload failed'
    uploadError.value = errorMessage
    uiStore.showError('Avatar upload failed', errorMessage)
  } finally {
    uploadingAvatar.value = false
    // Clear file input
    input.value = ''
  }
}

const removeAvatar = async () => {
  if (!user.value || !user.value.avatar_url) return

  uploadingAvatar.value = true
  uploadError.value = null

  try {
    // Update user profile to remove avatar URL
    const response = await authStore.fetchWithAuth('/api/users/me', {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ avatar_url: null })
    })

    if (response.ok) {
      const updatedUser = await response.json()
      // Update auth store with new user data
      authStore.user = updatedUser
      preferencesStore.auth.setUser(updatedUser)
      uiStore.showSuccess('Avatar removed', 'Your avatar has been successfully removed.')
    } else {
      const errorData = await response.json()
      uploadError.value = errorData.detail || 'Failed to remove avatar'
      uiStore.showError('Failed to remove avatar', uploadError.value || 'Unknown error')
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to remove avatar'
    uploadError.value = errorMessage
    uiStore.showError('Failed to remove avatar', errorMessage)
  } finally {
    uploadingAvatar.value = false
  }
}

const connectGitHub = () => {
  // The backend will get current user from Authorization header
  authStore.loginWithGitHub('/profile')
}

const handleLogout = () => {
  authStore.logout()
  navigateTo('/')
}

const startEditing = () => {
  if (!user.value) return
  isEditing.value = true
  editForm.value = {
    username: user.value.username || '',
    name: user.value.name || '',
    bio: user.value.bio || '',
    location: user.value.location || '',
    company: user.value.company || ''
  }
}

const cancelEditing = () => {
  isEditing.value = false
}

const saveProfile = async () => {
  if (!user.value) return

  saving.value = true
  try {
    const response = await authStore.fetchWithAuth('/api/users/me', {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(editForm.value)
    })

    if (response.ok) {
      const updatedUser = await response.json()
      // Update auth store with new user data
      authStore.user = updatedUser
      // Also update preferences store
      preferencesStore.auth.setUser(updatedUser)
      uiStore.showSuccess('Profile updated', 'Your profile has been successfully updated.')
      isEditing.value = false
    } else {
      const errorData = await response.json()
      uiStore.showError('Failed to update profile', errorData.detail || 'An error occurred while updating your profile.')
    }
  } catch (error) {
    console.error('Error updating profile:', error)
    uiStore.showError('Failed to update profile', 'An error occurred while updating your profile.')
  } finally {
    saving.value = false
  }
}

const checkGitHubOAuthError = () => {
  if (typeof window === 'undefined') return

  const urlParams = new URLSearchParams(window.location.search)
  const error = urlParams.get('error')

  if (error && error.includes('github_account_already_linked')) {
    // Extract the actual error message (everything after the colon)
    const errorMessage = error.split(':').slice(1).join(':').trim()

    uiStore.showError(
      'GitHub Account Already Linked',
      errorMessage || 'This GitHub account is already associated with another user. Please use a different GitHub account or contact support.'
    )

    // Clean up URL parameters
    const newUrl = window.location.pathname
    window.history.replaceState({}, '', newUrl)
  }
}

onMounted(() => {
  fetchUserProfile()
  fetchUserStats()
  checkGitHubOAuthError()
})
</script>