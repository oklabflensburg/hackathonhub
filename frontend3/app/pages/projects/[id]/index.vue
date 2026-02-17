<template>
  <div class="py-8">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-16">
      <svg class="w-24 h-24 text-red-400 mx-auto mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Project Not Found</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">{{ error }}</p>
      <NuxtLink 
        to="/projects" 
        class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to Projects
      </NuxtLink>
    </div>

    <!-- Project Details -->
    <div v-else-if="project" class="max-w-6xl mx-auto px-4 sm:px-6">
      <!-- Project Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ project.title }}</h1>
            <div class="flex items-center space-x-4 mt-2">
              <div class="flex items-center space-x-2">
                <div class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center overflow-hidden">
                  <img
                    v-if="project.owner?.avatar_url"
                    :src="project.owner.avatar_url"
                    :alt="project.owner.username"
                    class="w-full h-full object-cover"
                  />
                  <span v-else class="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {{ project.owner?.username?.charAt(0)?.toUpperCase() || 'U' }}
                  </span>
                </div>
                <span class="text-gray-600 dark:text-gray-400">{{ project.owner?.username || 'Unknown' }}</span>
              </div>
              <span class="text-gray-500 dark:text-gray-500">•</span>
              <span class="text-gray-600 dark:text-gray-400">{{ formatDate(project.created_at) }}</span>
            </div>
          </div>
          
          <!-- Vote Buttons -->
          <div v-if="authStore.isAuthenticated">
            <VoteButtons :project-id="project.id" />
          </div>
        </div>

        <!-- Project Status -->
        <div class="flex items-center space-x-4">
          <span 
            class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
            :class="{
              'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300': project.status === 'active',
              'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300': project.status === 'completed',
              'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300': project.status === 'archived'
            }"
          >
            {{ project.status || 'active' }}
          </span>
          
          <span v-if="project.hackathon" class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            {{ project.hackathon.name }}
          </span>
        </div>
      </div>

      <!-- Project Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Project Image -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden aspect-ratio-16-9">
            <img
              :src="projectImage"
              :alt="project.title"
              class="img-cover"
            />
          </div>

          <!-- Description -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Description</h2>
            <div class="prose dark:prose-invert max-w-none">
              <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ project.description }}</p>
            </div>
          </div>

          <!-- Technologies -->
          <div v-if="projectTechnologies.length > 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Technologies</h2>
            <div class="flex flex-wrap gap-3">
              <span 
                v-for="tech in projectTechnologies" 
                :key="tech"
                class="px-4 py-2 bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-300 rounded-lg text-sm font-medium"
              >
                {{ tech }}
              </span>
            </div>
          </div>

          <!-- Links -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Links</h2>
            <div class="space-y-4">
              <a 
                v-if="project.repository_url"
                :href="project.repository_url"
                target="_blank"
                class="flex items-center space-x-3 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              >
                <svg class="w-6 h-6 text-gray-700 dark:text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                <div class="flex-1">
                  <p class="font-medium text-gray-900 dark:text-white">GitHub Repository</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400 truncate">{{ project.repository_url }}</p>
                </div>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>

              <a 
                v-if="project.live_url"
                :href="project.live_url"
                target="_blank"
                class="flex items-center space-x-3 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              >
                <svg class="w-6 h-6 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                </svg>
                <div class="flex-1">
                  <p class="font-medium text-gray-900 dark:text-white">Live Demo</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400 truncate">{{ project.live_url }}</p>
                </div>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>

               <div v-if="!project.repository_url && !project.live_url" class="text-center py-4">
                <p class="text-gray-500 dark:text-gray-400">No links provided for this project</p>
              </div>
            </div>
          </div>

          <!-- Comments Section -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-gray-900 dark:text-white">Comments</h2>
              <span class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm">
                {{ project.comment_count || 0 }} comments
              </span>
            </div>

            <!-- Add Comment Form (for authenticated users) -->
            <div v-if="authStore.isAuthenticated" class="mb-8">
              <textarea
                v-model="newComment"
                placeholder="Add a comment..."
                rows="3"
                class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                :disabled="commentLoading"
              ></textarea>
              <div class="flex justify-end mt-3">
                <button
                  @click="submitComment"
                  :disabled="commentLoading || !newComment.trim()"
                  class="btn btn-primary px-6 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg 
                    v-if="commentLoading" 
                    class="w-5 h-5 animate-spin" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  <span v-else>Post Comment</span>
                </button>
              </div>
            </div>
            <div v-else class="mb-8 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg text-center">
              <p class="text-gray-600 dark:text-gray-400">
                Please <NuxtLink to="/login" class="text-primary-600 dark:text-primary-400 hover:underline">sign in</NuxtLink> to leave a comment
              </p>
            </div>

            <!-- Comments List -->
            <div v-if="commentsLoading" class="text-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
              <p class="mt-2 text-gray-600 dark:text-gray-400">Loading comments...</p>
            </div>
            <div v-else-if="comments.length === 0" class="text-center py-8">
              <svg class="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <p class="text-gray-500 dark:text-gray-400">No comments yet. Be the first to comment!</p>
            </div>
            <div v-else class="space-y-6">
              <div 
                v-for="comment in comments" 
                :key="comment.id"
                class="border-b border-gray-200 dark:border-gray-700 pb-6 last:border-0"
              >
                 <div class="flex items-start space-x-3">
                   <!-- User Avatar -->
                   <NuxtLink :to="'/profile'" class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center flex-shrink-0 overflow-hidden hover:opacity-90 transition-opacity">
                     <img
                       v-if="comment.user?.avatar_url"
                       :src="comment.user.avatar_url"
                       :alt="comment.user.name"
                       class="w-full h-full object-cover"
                     />
                     <span v-else class="text-sm font-medium text-gray-700 dark:text-gray-300">
                       {{ comment.user?.name?.charAt(0)?.toUpperCase() || 'U' }}
                     </span>
                   </NuxtLink>
                  
                  <!-- Comment Content -->
                  <div class="flex-1">
                    <div v-if="editingCommentId !== comment.id">
                      <div class="flex items-center justify-between mb-2">
                        <div>
                          <span class="font-medium text-gray-900 dark:text-white">{{ comment.user?.name || 'Anonymous' }}</span>
                          <span class="text-sm text-gray-500 dark:text-gray-400 ml-3">{{ formatDate(comment.created_at) }}</span>
                        </div>
                        <div v-if="authStore.user?.id === comment.user_id" class="flex items-center space-x-2">
                          <button
                            @click="editComment(comment)"
                            class="text-sm text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400"
                          >
                            Edit
                          </button>
                          <button
                            @click="deleteComment(comment.id)"
                            class="text-sm text-red-500 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300"
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                      <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ comment.content }}</p>
                      
                      <!-- Comment Actions -->
                      <div class="flex items-center space-x-4 mt-3">
                        <button
                          @click="voteComment(comment.id, 'upvote')"
                          class="flex items-center space-x-1 text-sm text-gray-500 dark:text-gray-400 hover:text-green-600 dark:hover:text-green-400"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                          </svg>
                          <span>{{ comment.upvote_count || 0 }}</span>
                        </button>
                        <button
                          @click="voteComment(comment.id, 'downvote')"
                          class="flex items-center space-x-1 text-sm text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                          </svg>
                          <span>{{ comment.downvote_count || 0 }}</span>
                        </button>
                        <button
                          @click="startReply(comment.id)"
                          class="text-sm text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400"
                        >
                          Reply
                        </button>
                       </div>
                       
                       <!-- Reply Form -->
                        <div v-if="replyingToCommentId === comment.id" class="mt-4 ml-6 border-l-2 border-gray-200 dark:border-gray-700 pl-4">
                         <textarea
                           v-model="replyContent"
                           rows="2"
                           placeholder="Write a reply..."
                           class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                           :disabled="replyLoading"
                         ></textarea>
                         <div class="flex justify-end space-x-2 mt-2">
                           <button
                             @click="cancelReply"
                             class="px-4 py-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-300"
                             :disabled="replyLoading"
                           >
                             Cancel
                           </button>
                           <button
                             @click="submitReply(comment.id)"
                             class="px-4 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                             :disabled="replyLoading || !replyContent.trim()"
                           >
                             <span v-if="replyLoading">Posting...</span>
                             <span v-else>Post Reply</span>
                           </button>
                         </div>
                        </div>
                       </div>
                       
                       <!-- Edit Form (shown when editingCommentId === comment.id) -->
                       <div v-else>
                        <div class="flex items-center justify-between mb-2">
                          <div>
                            <NuxtLink 
                              :to="'/profile'"
                              class="font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                            >
                              {{ comment.user?.name || 'Anonymous' }}
                            </NuxtLink>
                            <span class="text-sm text-gray-500 dark:text-gray-400 ml-3">{{ formatDate(comment.created_at) }}</span>
                          </div>
                          <div class="flex items-center space-x-2">
                            <button
                              @click="saveComment(comment.id)"
                              class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300"
                            >
                              Save
                            </button>
                            <button
                              @click="cancelEdit"
                              class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                        <textarea
                          v-model="editingContent"
                          rows="3"
                          class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                        ></textarea>
                      </div>
                       
                       <!-- Replies Section (only shown when not editing) -->
                       <div v-if="editingCommentId !== comment.id && comment.replies && comment.replies.length > 0" class="mt-4 ml-6 space-y-4 border-l-2 border-gray-200 dark:border-gray-700 pl-4">
                         <div 
                           v-for="reply in comment.replies" 
                           :key="reply.id"
                           class="pt-4 first:pt-0"
                         >
                           <div class="flex items-start space-x-3">
                             <!-- User Avatar -->
                             <NuxtLink :to="'/profile'" class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center flex-shrink-0 overflow-hidden hover:opacity-90 transition-opacity">
                               <img
                                 v-if="reply.user?.avatar_url"
                                 :src="reply.user.avatar_url"
                                 :alt="reply.user.name"
                                 class="w-full h-full object-cover"
                               />
                               <span v-else class="text-xs font-medium text-gray-700 dark:text-gray-300">
                                 {{ reply.user?.name?.charAt(0)?.toUpperCase() || 'U' }}
                               </span>
                             </NuxtLink>
                             
                             <!-- Reply Content -->
                             <div class="flex-1">
                                <div class="flex items-center justify-between mb-1">
                                 <div>
                                   <NuxtLink 
                                     :to="'/profile'"
                                     class="text-sm font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                                   >
                                     {{ reply.user?.name || 'Anonymous' }}
                                   </NuxtLink>
                                   <span class="text-xs text-gray-500 dark:text-gray-400 ml-2">{{ formatDate(reply.created_at) }}</span>
                                 </div>
                                 <div v-if="authStore.user?.id === reply.user_id" class="flex items-center space-x-2">
                                   <button
                                     @click="editComment(reply)"
                                     class="text-xs text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400"
                                   >
                                     Edit
                                   </button>
                                   <button
                                     @click="deleteComment(reply.id)"
                                     class="text-xs text-red-500 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300"
                                   >
                                     Delete
                                   </button>
                                 </div>
                               </div>
                               <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ reply.content }}</p>
                               
                               <!-- Reply Actions -->
                               <div class="flex items-center space-x-3 mt-2">
                                 <button
                                   @click="voteComment(reply.id, 'upvote')"
                                   class="flex items-center space-x-1 text-xs text-gray-500 dark:text-gray-400 hover:text-green-600 dark:hover:text-green-400"
                                 >
                                   <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                                   </svg>
                                   <span>{{ reply.upvote_count || 0 }}</span>
                                 </button>
                                 <button
                                   @click="voteComment(reply.id, 'downvote')"
                                   class="flex items-center space-x-1 text-xs text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400"
                                 >
                                   <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                                   </svg>
                                   <span>{{ reply.downvote_count || 0 }}</span>
                                 </button>
                                 <button
                                   @click="startReply(reply.id)"
                                   class="text-xs text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400"
                                 >
                                   Reply
                                 </button>
                               </div>
                             </div>
                           </div>
                         </div>
                       </div>
                   </div>
                 </div>
               </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Stats Card -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">Project Stats</h2>
            <div class="space-y-6">
              <div class="grid grid-cols-2 gap-4">
                <div class="text-center">
                  <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ project.upvote_count || 0 }}</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Upvotes</p>
                </div>
                <div class="text-center">
                  <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ project.downvote_count || 0 }}</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Downvotes</p>
                </div>
              </div>
              
              <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
                <div class="text-center">
                  <p class="text-4xl font-bold text-gray-900 dark:text-white">{{ project.vote_score || 0 }}</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Total Score</p>
                </div>
              </div>

              <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
                <div class="text-center">
                  <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ project.comment_count || 0 }}</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Comments</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Actions Card -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Actions</h2>
            <div class="space-y-3">
              <!-- Edit Project Button (for owner/members) -->
              <NuxtLink 
                v-if="canEditProject"
                :to="`/projects/${project.id}/edit`"
                class="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/30 transition-colors"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                <span>Edit Project</span>
              </NuxtLink>

              <NuxtLink 
                v-if="project.hackathon_id"
                :to="`/hackathons/${project.hackathon_id}`"
                class="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-400 rounded-lg hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <span>View Hackathon</span>
              </NuxtLink>

              <NuxtLink 
                to="/projects"
                class="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                <span>Back to Projects</span>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { format } from 'date-fns'
import { useRoute } from '#imports'
import { useAuthStore } from '~/stores/auth'
import { useVotingStore } from '~/stores/voting'
import VoteButtons from '~/components/VoteButtons.vue'

const route = useRoute()
const authStore = useAuthStore()
const votingStore = useVotingStore()

const loading = ref(true)
const error = ref<string | null>(null)
const project = ref<any>(null)

// Comments state
const comments = ref<any[]>([])
const commentsLoading = ref(false)
const newComment = ref('')
const commentLoading = ref(false)
const editingCommentId = ref<number | null>(null)
const editingContent = ref('')
const replyingToCommentId = ref<number | null>(null)
const replyContent = ref('')
const replyLoading = ref(false)

const projectTechnologies = computed(() => {
  if (!project.value?.technologies) return []
  return project.value.technologies.split(',').map((tech: string) => tech.trim()).filter(Boolean)
})

const projectImage = computed(() => {
  if (!project.value?.image_path) return 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80'
  return project.value.image_path
})

const canEditProject = computed(() => {
  if (!authStore.isAuthenticated || !project.value) {
    return false
  }
  
  // Check if user is the project owner
  // Convert both to numbers for comparison
  const userId = Number(authStore.user?.id)
  const ownerId = Number(project.value.owner_id)
  const isOwner = userId === ownerId
  
  if (isOwner) return true
  
  // TODO: Check if user is a team member
  // For now, only owner can edit
  return false
})

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  try {
    return format(new Date(dateString), 'MMM dd, yyyy')
  } catch {
    return dateString
  }
}

const fetchProject = async () => {
  try {
    loading.value = true
    error.value = null
    
    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    
    // First, increment the view count
    try {
      await fetch(`${backendUrl}/api/projects/${projectId}/view`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    } catch (viewErr) {
      console.warn('Failed to increment view count:', viewErr)
      // Continue loading project even if view increment fails
    }
    
    // Then fetch the project details
    const response = await fetch(`${backendUrl}/api/projects/${projectId}`)
    
    if (!response.ok) {
      if (response.status === 404) {
        error.value = 'Project not found'
      } else {
        error.value = `Failed to load project: ${response.status}`
      }
      return
    }
    
    project.value = await response.json()
    
    // Also fetch vote stats for this project
    await votingStore.getProjectVoteStats(projectId)
  } catch (err) {
    console.error('Error fetching project:', err)
    error.value = 'Failed to load project details'
  } finally {
    loading.value = false
  }
}

// Comments methods
const fetchComments = async () => {
  try {
    commentsLoading.value = true
    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    
    const response = await fetch(`${backendUrl}/api/projects/${projectId}/comments`)
    
    if (response.ok) {
      comments.value = await response.json()
    }
  } catch (err) {
    console.error('Error fetching comments:', err)
  } finally {
    commentsLoading.value = false
  }
}

const submitComment = async () => {
  if (!newComment.value.trim() || commentLoading.value) return
  
  try {
    commentLoading.value = true
    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    
    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      console.error('No authentication token')
      return
    }
    
    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: newComment.value.trim()
      })
    })
    
    if (response.ok) {
      newComment.value = ''
      await fetchComments()
      // Update comment count in project
      if (project.value) {
        project.value.comment_count = (project.value.comment_count || 0) + 1
      }
    } else {
      console.error('Failed to submit comment:', response.status)
    }
  } catch (err) {
    console.error('Error submitting comment:', err)
  } finally {
    commentLoading.value = false
  }
}

const editComment = (comment: any) => {
  editingCommentId.value = comment.id
  editingContent.value = comment.content
}

const saveComment = async (commentId: number) => {
  if (!editingContent.value.trim()) return
  
  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    
    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      console.error('No authentication token')
      return
    }
    
    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/comments/${commentId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: editingContent.value.trim()
      })
    })
    
    if (response.ok) {
      editingCommentId.value = null
      editingContent.value = ''
      await fetchComments()
    } else {
      console.error('Failed to update comment:', response.status)
    }
  } catch (err) {
    console.error('Error updating comment:', err)
  }
}

const cancelEdit = () => {
  editingCommentId.value = null
  editingContent.value = ''
}

const deleteComment = async (commentId: number) => {
  if (!confirm('Are you sure you want to delete this comment?')) return
  
  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    
    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      console.error('No authentication token')
      return
    }
    
    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/comments/${commentId}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      await fetchComments()
      // Update comment count in project
      if (project.value) {
        project.value.comment_count = Math.max(0, (project.value.comment_count || 1) - 1)
      }
    } else {
      console.error('Failed to delete comment:', response.status)
    }
  } catch (err) {
    console.error('Error deleting comment:', err)
  }
}

const voteComment = async (commentId: number, voteType: 'upvote' | 'downvote') => {
  try {
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    
    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      console.error('No authentication token')
      return
    }
    
    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/comments/${commentId}/vote`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ vote_type: voteType })
    })
    
    if (response.ok) {
      // Refresh comments to get updated vote counts
      await fetchComments()
    } else {
      console.error('Failed to vote on comment:', response.status)
    }
  } catch (err) {
    console.error('Error voting on comment:', err)
  }
}

// Reply functions
const startReply = (commentId: number) => {
  replyingToCommentId.value = commentId
  replyContent.value = ''
}

const cancelReply = () => {
  replyingToCommentId.value = null
  replyContent.value = ''
}

const submitReply = async (commentId: number) => {
  if (!replyContent.value.trim() || replyLoading.value) return
  
  try {
    replyLoading.value = true
    const projectId = parseInt(route.params.id as string)
    const config = useRuntimeConfig()
    const backendUrl = config.public.apiUrl || 'http://localhost:8000'
    
    // Check if user is authenticated
    if (!authStore.isAuthenticated) {
      console.error('No authentication token')
      return
    }
    
    // Use fetchWithAuth for automatic token refresh
    const response = await authStore.fetchWithAuth(`${backendUrl}/api/projects/${projectId}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: replyContent.value.trim(),
        parent_comment_id: commentId
      })
    })
    
    if (response.ok) {
      replyContent.value = ''
      replyingToCommentId.value = null
      await fetchComments()
      // Update comment count in project
      if (project.value) {
        project.value.comment_count = (project.value.comment_count || 0) + 1
      }
    } else {
      console.error('Failed to submit reply:', response.status)
    }
  } catch (err) {
    console.error('Error submitting reply:', err)
  } finally {
    replyLoading.value = false
  }
}

onMounted(() => {
  fetchProject()
  fetchComments()
})
</script>
