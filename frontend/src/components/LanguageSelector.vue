<template>
  <div class="language-selector" :class="{ open: isOpen }">
    <button class="selector-btn" @click="isOpen = !isOpen">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="2" y1="12" x2="22" y2="12"/>
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
      </svg>
      <span>{{ currentLanguageName }}</span>
      <svg class="chevron" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="m6 9 6 6 6-6"/>
      </svg>
    </button>
    
    <div v-if="isOpen" class="dropdown">
      <div class="dropdown-section">
        <span class="section-title">Language</span>
        <button
          v-for="lang in i18nStore.languages"
          :key="lang.code"
          class="dropdown-item"
          :class="{ active: lang.code === i18nStore.currentLanguage }"
          @click="selectLanguage(lang.code)"
        >
          <span>{{ lang.name }}</span>
          <span v-if="lang.isRTL" class="rtl-badge">RTL</span>
        </button>
      </div>
      
      <div class="dropdown-divider"></div>
      
      <div class="dropdown-section">
        <span class="section-title">Currency</span>
        <button
          v-for="currency in i18nStore.currencies"
          :key="currency.code"
          class="dropdown-item"
          :class="{ active: currency.code === i18nStore.currentCurrency }"
          @click="selectCurrency(currency.code)"
        >
          <span>{{ currency.symbol }} {{ currency.code }}</span>
          <span class="currency-name">{{ currency.name }}</span>
        </button>
      </div>
    </div>
    
    <div v-if="isOpen" class="backdrop" @click="isOpen = false"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18nStore } from '../stores/i18n'

const i18nStore = useI18nStore()
const isOpen = ref(false)

const currentLanguageName = computed(() => {
  const lang = i18nStore.languages.find(l => l.code === i18nStore.currentLanguage)
  return lang?.name || 'English'
})

async function selectLanguage(code: string): Promise<void> {
  await i18nStore.setLanguage(code)
  isOpen.value = false
}

async function selectCurrency(code: string): Promise<void> {
  await i18nStore.setCurrency(code)
  isOpen.value = false
}
</script>

<style scoped>
.language-selector {
  position: relative;
}

.selector-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  color: #374151;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.selector-btn:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.chevron {
  transition: transform 0.2s;
}

.language-selector.open .chevron {
  transform: rotate(180deg);
}

.dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  min-width: 200px;
  max-height: 400px;
  overflow-y: auto;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  z-index: 100;
}

.dropdown-section {
  padding: 0.5rem;
}

.section-title {
  display: block;
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.dropdown-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 0.25rem 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0.5rem 0.75rem;
  background: transparent;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
  transition: all 0.15s;
  text-align: left;
}

.dropdown-item:hover {
  background: #f3f4f6;
}

.dropdown-item.active {
  background: #fff7ed;
  color: #ea580c;
}

.rtl-badge {
  font-size: 0.625rem;
  padding: 0.125rem 0.375rem;
  background: #dbeafe;
  color: #2563eb;
  border-radius: 4px;
  font-weight: 600;
}

.currency-name {
  font-size: 0.75rem;
  color: #9ca3af;
}

.backdrop {
  position: fixed;
  inset: 0;
  z-index: 50;
}

[dir="rtl"] .dropdown {
  left: 0;
  right: auto;
}
</style>
