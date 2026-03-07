<template>
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <main class="lg:col-span-2 space-y-8">
      <slot name="main">
        <!-- Fallback content if main slot is empty -->
        <div v-if="false"></div>
      </slot>
    </main>
    <aside class="space-y-6">
      <slot name="sidebar">
        <!-- Fallback content if sidebar slot is empty -->
        <div v-if="false"></div>
      </slot>
    </aside>
  </div>
</template>
