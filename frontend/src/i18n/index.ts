import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import ar from './locales/ar.json'

export type MessageSchema = typeof en

const i18n = createI18n<[MessageSchema], 'en' | 'ar'>({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    ar
  }
})

export default i18n

export function setI18nLanguage(locale: string): void {
  if (i18n.mode === 'legacy') {
    i18n.global.locale = locale as 'en' | 'ar'
  } else {
    (i18n.global.locale as any).value = locale
  }
  
  document.querySelector('html')?.setAttribute('lang', locale)
  
  // Set RTL direction for Arabic and Hebrew
  const rtlLanguages = ['ar', 'he']
  if (rtlLanguages.includes(locale)) {
    document.documentElement.dir = 'rtl'
  } else {
    document.documentElement.dir = 'ltr'
  }
}
