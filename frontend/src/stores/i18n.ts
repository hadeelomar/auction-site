import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Language {
  code: string
  name: string
  isRTL: boolean
  defaultCurrency: string
}

export interface Currency {
  code: string
  symbol: string
  name: string
  rate: number
}

const API_BASE_URL = 'http://localhost:8000/api'

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null
  return null
}

export const useI18nStore = defineStore('i18n', () => {
  const currentLanguage = ref('en')
  const currentCurrency = ref('GBP')
  const isRTL = ref(false)
  const languages = ref<Language[]>([])
  const currencies = ref<Currency[]>([])
  const isLoading = ref(false)

  const direction = computed(() => isRTL.value ? 'rtl' : 'ltr')

  const currentCurrencySymbol = computed(() => {
    const currency = currencies.value.find(c => c.code === currentCurrency.value)
    return currency?.symbol || '£'
  })

  async function fetchLanguages(): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/i18n/languages/`, {
        credentials: 'include'
      })
      if (response.ok) {
        const data = await response.json()
        languages.value = data.languages
        currentLanguage.value = data.currentLanguage
        isRTL.value = data.isRTL
      }
    } catch (err) {
      console.error('Failed to fetch languages:', err)
    }
  }

  async function fetchCurrencies(): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/i18n/currencies/`, {
        credentials: 'include'
      })
      if (response.ok) {
        const data = await response.json()
        currencies.value = data.currencies
      }
    } catch (err) {
      console.error('Failed to fetch currencies:', err)
    }
  }

  async function setLanguage(langCode: string): Promise<boolean> {
    isLoading.value = true
    try {
      const csrfToken = getCookie('csrftoken')
      const response = await fetch(`${API_BASE_URL}/i18n/language/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken || ''
        },
        credentials: 'include',
        body: JSON.stringify({ language: langCode })
      })

      if (response.ok) {
        const data = await response.json()
        currentLanguage.value = data.language
        isRTL.value = data.isRTL
        
        // Update document direction
        document.documentElement.dir = isRTL.value ? 'rtl' : 'ltr'
        document.documentElement.lang = langCode
        
        return true
      }
      return false
    } catch (err) {
      console.error('Failed to set language:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function setCurrency(currencyCode: string): Promise<boolean> {
    isLoading.value = true
    try {
      const csrfToken = getCookie('csrftoken')
      const response = await fetch(`${API_BASE_URL}/i18n/currency/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken || ''
        },
        credentials: 'include',
        body: JSON.stringify({ currency: currencyCode })
      })

      if (response.ok) {
        const data = await response.json()
        currentCurrency.value = data.currency
        return true
      }
      return false
    } catch (err) {
      console.error('Failed to set currency:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function convertPrice(amount: number | string, toCurrency?: string): Promise<string> {
    const target = toCurrency || currentCurrency.value
    try {
      const response = await fetch(
        `${API_BASE_URL}/i18n/convert/?amount=${amount}&from=GBP&to=${target}`,
        { credentials: 'include' }
      )
      if (response.ok) {
        const data = await response.json()
        return data.formatted
      }
    } catch (err) {
      console.error('Failed to convert currency:', err)
    }
    return `£${amount}`
  }

  function formatPrice(amount: number | string): string {
    const num = typeof amount === 'string' ? parseFloat(amount) : amount
    const currency = currencies.value.find(c => c.code === currentCurrency.value)
    
    if (!currency) {
      return `£${num.toLocaleString()}`
    }

    // Convert from GBP to target currency
    const converted = num * currency.rate
    return `${currency.symbol}${converted.toLocaleString(undefined, { 
      minimumFractionDigits: 2, 
      maximumFractionDigits: 2 
    })}`
  }

  async function initialize(): Promise<void> {
    await Promise.all([fetchLanguages(), fetchCurrencies()])
    
    // Apply RTL if needed
    if (isRTL.value) {
      document.documentElement.dir = 'rtl'
    }
    document.documentElement.lang = currentLanguage.value
  }

  return {
    currentLanguage,
    currentCurrency,
    isRTL,
    direction,
    languages,
    currencies,
    isLoading,
    currentCurrencySymbol,
    fetchLanguages,
    fetchCurrencies,
    setLanguage,
    setCurrency,
    convertPrice,
    formatPrice,
    initialize
  }
})
