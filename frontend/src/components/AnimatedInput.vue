<template>
  <div
    class="group/input rounded-lg p-[2px] transition duration-300"
    :style="{ background: backgroundGradient }"
    @mousemove="handleMouseMove"
    @mouseenter="() => visible = true"
    @mouseleave="() => visible = false"
  >
    <input
      :type="type"
      :id="id"
      :placeholder="placeholder"
      :value="modelValue"
      @input="handleInput"
      class="shadow-input flex h-10 w-full rounded-md border-none bg-gray-50 px-3 py-2 text-sm text-black transition duration-400 group-hover/input:shadow-none file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-neutral-400 focus-visible:ring-[2px] focus-visible:ring-amber-400 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 dark:bg-zinc-800 dark:text-white dark:shadow-[0px_0px_1px_1px_#404040] dark:focus-visible:ring-amber-600"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  type?: string
  id?: string
  placeholder?: string
  modelValue?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  id: '',
  placeholder: '',
  modelValue: ''
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const radius = 100
const visible = ref<boolean>(false)
const mouseX = ref<number>(0)
const mouseY = ref<number>(0)

const backgroundGradient = computed(() => {
  if (!visible.value) return 'transparent'
  return `radial-gradient(${radius}px circle at ${mouseX.value}px ${mouseY.value}px, #f59e0b, transparent 80%)`
})

const handleMouseMove = (event: MouseEvent) => {
  const rect = (event.currentTarget as HTMLElement).getBoundingClientRect()
  mouseX.value = event.clientX - rect.left
  mouseY.value = event.clientY - rect.top
}

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>