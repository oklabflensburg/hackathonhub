<template>
  <div v-if="rules" class="mb-8">
    <!-- Header with Icon -->
    <div class="flex items-center gap-3 mb-6">
      <Icon name="file-text" class="w-6 h-6 text-gray-700 dark:text-gray-300" />
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ title }}</h2>
      <Badge variant="neutral" size="sm">
        Rules
      </Badge>
    </div>

    <!-- Rules Content -->
    <Card class="p-4 sm:p-5 lg:p-6 bg-gray-50 dark:bg-gray-700/50">
      <div class="prose dark:prose-invert max-w-none">
        <!-- Rules List (if rules contain bullet points) -->
        <div v-if="rules.includes('•') || rules.includes('-')" class="space-y-3">
          <div
            v-for="(rule, idx) in parseRules(rules)"
            :key="idx"
            class="flex items-start gap-3"
          >
            <Icon name="check-circle" class="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5 flex-shrink-0" />
            <p class="text-gray-700 dark:text-gray-300">{{ rule }}</p>
          </div>
        </div>
        
        <!-- Plain Text Rules -->
        <div v-else>
          <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ rules }}</p>
        </div>
      </div>

      <!-- Rules Actions -->
      <div class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700 flex flex-wrap gap-3">
        <Button
          variant="outline"
          size="sm"
          @click="copyRules"
        >
          <Icon name="copy" class="w-4 h-4 mr-2" />
          Copy Rules
        </Button>
        <Button
          variant="ghost"
          size="sm"
          @click="downloadRules"
        >
          <Icon name="download" class="w-4 h-4 mr-2" />
          Download PDF
        </Button>
        <Button
          variant="ghost"
          size="sm"
          @click="printRules"
        >
          <Icon name="printer" class="w-4 h-4 mr-2" />
          Print
        </Button>
      </div>
    </Card>

    <!-- Rules Summary -->
    <div class="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-4">
      <Card class="p-3 bg-blue-50 dark:bg-blue-900/20 border-blue-100 dark:border-blue-800">
        <div class="flex items-center gap-2">
          <Icon name="clock" class="w-4 h-4 text-blue-600 dark:text-blue-400" />
          <span class="text-sm font-medium text-blue-700 dark:text-blue-300">Time Limit</span>
        </div>
        <p class="text-xs text-blue-600 dark:text-blue-400 mt-1">
          Follow the specified time constraints
        </p>
      </Card>
      <Card class="p-3 bg-green-50 dark:bg-green-900/20 border-green-100 dark:border-green-800">
        <div class="flex items-center gap-2">
          <Icon name="users" class="w-4 h-4 text-green-600 dark:text-green-400" />
          <span class="text-sm font-medium text-green-700 dark:text-green-300">Team Size</span>
        </div>
        <p class="text-xs text-green-600 dark:text-green-400 mt-1">
          Adhere to team size restrictions
        </p>
      </Card>
      <Card class="p-3 bg-purple-50 dark:bg-purple-900/20 border-purple-100 dark:border-purple-800">
        <div class="flex items-center gap-2">
          <Icon name="shield" class="w-4 h-4 text-purple-600 dark:text-purple-400" />
          <span class="text-sm font-medium text-purple-700 dark:text-purple-300">Code of Conduct</span>
        </div>
        <p class="text-xs text-purple-600 dark:text-purple-400 mt-1">
          Maintain respectful behavior
        </p>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { RulesSectionProps } from '~/types/hackathon-types'
import { Icon, Card, Button, Badge } from '~/components/atoms'

defineProps<RulesSectionProps>()

// Helper function to parse rules text into array
function parseRules(rulesText: string): string[] {
  if (!rulesText) return []
  
  // Split by bullet points, dashes, or numbers
  const lines = rulesText.split(/\n+/)
  const parsed: string[] = []
  
  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) continue
    
    // Remove bullet points, dashes, or numbers at the start
    const cleanLine = trimmed
      .replace(/^[•\-*]\s*/, '')
      .replace(/^\d+\.\s*/, '')
      .replace(/^\(\d+\)\s*/, '')
    
    if (cleanLine) {
      parsed.push(cleanLine)
    }
  }
  
  return parsed.length > 0 ? parsed : [rulesText]
}

// Copy rules to clipboard
function copyRules() {
  const rules = document.querySelector('.rules-content')?.textContent || ''
  navigator.clipboard.writeText(rules)
    .then(() => {
      // Show success message (could use a toast component)
      alert('Rules copied to clipboard!')
    })
    .catch(err => {
      console.error('Failed to copy rules:', err)
    })
}

// Download rules as PDF (placeholder)
function downloadRules() {
  alert('PDF download functionality would be implemented here')
}

// Print rules
function printRules() {
  window.print()
}
</script>