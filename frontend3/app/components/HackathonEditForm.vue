<template>
  <div v-if="visible" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
      <div class="p-4 sm:p-5 lg:p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ $t('hackathons.details.editHackathon') }}</h2>
          <button @click="$emit('cancel')"
            class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSave" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {{ $t('hackathons.details.name') }}
            </label>
            <input v-model="localFormData.name" type="text" required
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {{ $t('hackathons.details.description') }}
            </label>
            <textarea v-model="localFormData.description" rows="3" required
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {{ $t('hackathons.details.startDate') }}
              </label>
              <input v-model="localFormData.start_date" type="datetime-local" required
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {{ $t('hackathons.details.endDate') }}
              </label>
              <input v-model="localFormData.end_date" type="datetime-local" required
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {{ $t('hackathons.details.location') }}
            </label>
            <input v-model="localFormData.location" type="text" required
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {{ $t('hackathons.details.imageUrl') }}
            </label>
            <input v-model="localFormData.image_url" type="url"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              :placeholder="$t('hackathons.details.imageUrlPlaceholder')" />
            <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
              {{ $t('hackathons.details.imageUrlHelper') }}
            </p>
          </div>

          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                {{ $t('hackathons.details.prizes') }}
              </label>
              <button type="button" @click="localFormData.prizes.push({ name: '', description: '', value: '' })"
                class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300">
                + {{ $t('hackathons.details.addPrize') }}
              </button>
            </div>

            <div class="space-y-3">
              <div v-for="(prize, index) in localFormData.prizes" :key="index"
                class="p-3 border border-gray-300 dark:border-gray-600 rounded-lg">
                <div class="flex justify-between items-start mb-2">
                  <span class="font-medium text-gray-700 dark:text-gray-300">{{ $t('hackathons.details.prizeNumber', {
                    number: Number(index) + 1 }) }}</span>
                  <button type="button" @click="localFormData.prizes.splice(index, 1)"
                    class="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300">
                    {{ $t('hackathons.details.remove') }}
                  </button>
                </div>

                <div class="space-y-2">
                  <div>
                    <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">{{
                      $t('hackathons.details.prizeName') }}</label>
                    <input v-model="prize.name" type="text"
                      :placeholder="$t('hackathons.details.prizeNamePlaceholder')"
                      class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white" />
                  </div>
                  <div>
                    <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">{{ $t('common.description')
                      }}</label>
                    <input v-model="prize.description" type="text"
                      :placeholder="$t('hackathons.details.prizeDescriptionPlaceholder')"
                      class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white" />
                  </div>
                  <div>
                    <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">{{
                      $t('hackathons.details.value') }}</label>
                    <input v-model="prize.value" type="text"
                      :placeholder="$t('hackathons.details.prizeAmountPlaceholder')"
                      class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white" />
                  </div>
                </div>
              </div>

              <div v-if="localFormData.prizes.length === 0"
                class="text-center py-4 text-gray-500 dark:text-gray-400 border border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
                {{ $t('hackathons.details.noPrizesAdded') }}
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {{ $t('hackathons.details.rulesAndGuidelines') }}
            </label>
            <textarea v-model="localFormData.rules" rows="4"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"></textarea>
          </div>

          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                {{ $t('hackathons.details.organizers') }}
              </label>
              <button type="button" @click="localFormData.organizers.push({ name: '', role: '' })"
                class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300">
                + {{ $t('hackathons.details.addOrganizer') }}
              </button>
            </div>

            <div class="space-y-3">
              <div v-for="(organizer, index) in localFormData.organizers" :key="index"
                class="p-3 border border-gray-300 dark:border-gray-600 rounded-lg">
                <div class="flex justify-between items-start mb-2">
                  <span class="font-medium text-gray-700 dark:text-gray-300">{{
                    $t('hackathons.details.organizerNumber', { number: Number(index) + 1 }) }}</span>
                  <button type="button" @click="localFormData.organizers.splice(index, 1)"
                    class="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300">
                    {{ $t('hackathons.details.remove') }}
                  </button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                  <div>
                    <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">{{
                      $t('hackathons.details.name') }}</label>
                    <input v-model="organizer.name" type="text"
                      :placeholder="$t('hackathons.details.organizerNamePlaceholder')"
                      class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white" />
                  </div>
                  <div>
                    <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">{{
                      $t('hackathons.details.role') }}</label>
                    <input v-model="organizer.role" type="text"
                      :placeholder="$t('hackathons.details.organizerRolePlaceholder')"
                      class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white" />
                  </div>
                </div>
              </div>

              <div v-if="localFormData.organizers.length === 0"
                class="text-center py-4 text-gray-500 dark:text-gray-400 border border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
                {{ $t('hackathons.details.noOrganizersAdded') }}
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {{ $t('hackathons.details.prizePool') }}
            </label>
            <input v-model="localFormData.prize_pool" type="text"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              :placeholder="$t('hackathons.details.prizeAmountInputPlaceholder')" />
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="$emit('cancel')"
              class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              :disabled="loading">
              {{ $t('hackathons.details.cancel') }}
            </button>
            <button type="submit"
              class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center"
              :disabled="loading">
              <svg v-if="loading" class="w-5 h-5 mr-2 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              {{ loading ? $t('hackathons.details.saving') : $t('hackathons.details.saveChanges') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  visible: boolean
  formData: any
  loading?: boolean
}>()

const emit = defineEmits<{
  save: [data: any]
  cancel: []
}>()

// Create a local copy of formData to avoid direct mutation
const localFormData = ref({ ...props.formData })

// Update localFormData when props.formData changes
watch(() => props.formData, (newData) => {
  localFormData.value = { ...newData }
}, { deep: true })

// Emit save event with current form data
const handleSave = () => {
  emit('save', localFormData.value)
}
</script>