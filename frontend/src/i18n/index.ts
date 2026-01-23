import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import ar from './locales/ar.json'
import fr from './locales/fr.json'
import es from './locales/es.json'
import de from './locales/de.json'
import zh from './locales/zh.json'
import ja from './locales/ja.json'
import ko from './locales/ko.json'
import pt from './locales/pt.json'
import ru from './locales/ru.json'
import hi from './locales/hi.json'
import tr from './locales/tr.json'
import he from './locales/he.json'

export type MessageSchema = typeof en

const i18n = createI18n<[MessageSchema], 'en' | 'ar' | 'fr' | 'es' | 'de' | 'zh' | 'ja' | 'ko' | 'pt' | 'ru' | 'hi' | 'tr' | 'he'>({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    ar,
    fr,
    es,
    de,
    zh,
    ja,
    ko,
    pt,
    ru,
    hi,
    tr,
    he
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
  const rtlLanguages = ['ar', 'he', 'fa', 'ur']
  if (rtlLanguages.includes(locale)) {
    document.documentElement.dir = 'rtl'
  } else {
    document.documentElement.dir = 'ltr'
  }
}
