<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Hero Section -->
    <div class="bg-gradient-to-br from-primary-500 to-purple-600 text-white">
      <div class="container mx-auto px-4 py-16">
        <div class="max-w-3xl mx-auto text-center">
          <h1 class="text-5xl font-bold mb-6">About Hackathon Hub</h1>
          <p class="text-xl opacity-90">
            A platform where innovators, developers, and creators come together to build the future.
          </p>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="container mx-auto px-4 py-12">
      <div class="max-w-4xl mx-auto">
        <!-- Mission -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 mb-8">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Our Mission</h2>
          <div class="prose dark:prose-invert max-w-none">
            <p class="text-gray-700 dark:text-gray-300 mb-4">
              Hackathon Hub was born from a simple idea: to make hackathons more accessible, collaborative, and impactful. We believe that great ideas deserve a platform where they can grow, connect with the right people, and turn into reality.
            </p>
            <p class="text-gray-700 dark:text-gray-300">
              Our mission is to democratize innovation by providing tools that help organizers run better events, participants build amazing projects, and communities discover groundbreaking solutions.
            </p>
          </div>
        </div>

        <!-- Features -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div class="w-12 h-12 rounded-lg bg-primary-100 dark:bg-primary-900 flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-primary-600 dark:text-primary-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Global Community</h3>
            <p class="text-gray-600 dark:text-gray-400">
              Connect with thousands of developers, designers, and innovators from around the world.
            </p>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div class="w-12 h-12 rounded-lg bg-primary-100 dark:bg-primary-900 flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-primary-600 dark:text-primary-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Real-time Collaboration</h3>
            <p class="text-gray-600 dark:text-gray-400">
              Work together seamlessly with built-in tools for team formation, project management, and communication.
            </p>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div class="w-12 h-12 rounded-lg bg-primary-100 dark:bg-primary-900 flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-primary-600 dark:text-primary-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Secure Platform</h3>
            <p class="text-gray-600 dark:text-gray-400">
              Your data and projects are protected with enterprise-grade security and privacy controls.
            </p>
          </div>
        </div>

        <!-- Team -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 mb-8">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">Meet Our Team</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="text-center">
              <div class="w-32 h-32 rounded-full bg-gradient-to-br from-primary-500 to-purple-600 mx-auto mb-4 flex items-center justify-center">
                <span class="text-white text-4xl font-bold">JS</span>
              </div>
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-1">Jane Smith</h3>
              <p class="text-primary-600 dark:text-primary-400 mb-2">CEO & Founder</p>
              <p class="text-gray-600 dark:text-gray-400">
                Former Google engineer passionate about developer communities.
              </p>
            </div>

            <div class="text-center">
              <div class="w-32 h-32 rounded-full bg-gradient-to-br from-primary-500 to-purple-600 mx-auto mb-4 flex items-center justify-center">
                <span class="text-white text-4xl font-bold">JD</span>
              </div>
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-1">John Doe</h3>
              <p class="text-primary-600 dark:text-primary-400 mb-2">CTO</p>
              <p class="text-gray-600 dark:text-gray-400">
                Full-stack developer with 10+ years of experience in scalable systems.
              </p>
            </div>

            <div class="text-center">
              <div class="w-32 h-32 rounded-full bg-gradient-to-br from-primary-500 to-purple-600 mx-auto mb-4 flex items-center justify-center">
                <span class="text-white text-4xl font-bold">AJ</span>
              </div>
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-1">Alex Johnson</h3>
              <p class="text-primary-600 dark:text-primary-400 mb-2">Head of Community</p>
              <p class="text-gray-600 dark:text-gray-400">
                Community builder who has organized 50+ hackathons worldwide.
              </p>
            </div>
          </div>
        </div>

        <!-- Stats -->
        <div class="bg-gradient-to-br from-primary-500 to-purple-600 rounded-2xl shadow-lg p-8 text-white">
          <h2 class="text-3xl font-bold mb-8 text-center">By The Numbers</h2>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div class="text-center">
              <div class="text-4xl font-bold mb-2">500+</div>
              <div class="opacity-90">Hackathons Hosted</div>
            </div>
            <div class="text-center">
              <div class="text-4xl font-bold mb-2">50K+</div>
              <div class="opacity-90">Active Users</div>
            </div>
            <div class="text-center">
              <div class="text-4xl font-bold mb-2">10K+</div>
              <div class="opacity-90">Projects Created</div>
            </div>
            <div class="text-center">
              <div class="text-4xl font-bold mb-2">$5M+</div>
              <div class="opacity-90">In Prizes Awarded</div>
            </div>
          </div>
        </div>

        <!-- CTA -->
        <div class="text-center mt-12">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Ready to Join?</h2>
          <p class="text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
            Whether you're an organizer looking to host an event or a participant ready to build something amazing, Hackathon Hub has everything you need.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <NuxtLink to="/hackathons" class="btn btn-primary">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Browse Hackathons
            </NuxtLink>
            <NuxtLink to="/create" class="btn btn-outline">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create Your Own
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// About page component
</script>