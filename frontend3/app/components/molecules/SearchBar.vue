<template>
  <div>
    <Input
      v-model="localValue"
      :placeholder="placeholder"
      clearable
      @input="onInput"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Input from '~/components/atoms/Input.vue'

interface Props {
  placeholder?: string
  debounce?: number
  modelValue?: string
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Search…',
  debounce: 300,
  modelValue: '',
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  search: [value: string]
}>()

const localValue = ref(props.modelValue)
let timer: ReturnType<typeof setTimeout> | null = null

watch(() => props.modelValue, (value) => {
  localValue.value = value
})

const onInput = () => {
  emit('update:modelValue', localValue.value)

  if (timer) {
    clearTimeout(timer)
  }

  timer = setTimeout(() => {
    emit('search', localValue.value)
  }, props.debounce)
}
</script>
