import { createApp } from "vue"
import { createPinia } from "pinia"
import App from "./App.vue"
import router from "./router"
import i18n from "./i18n"
import { useI18nStore } from "./stores/i18n"

// Check if we're on an auth page and let Django handle it
if (window.location.pathname.startsWith('/login') || window.location.pathname.startsWith('/signup')) {
  // Don't initialize Vue app for auth pages - let Django handle them
} else {
  const app = createApp(App)
  const pinia = createPinia()

  app.use(pinia)
  app.use(router)
  app.use(i18n)

  // Initialize i18n store after pinia is set up
  const i18nStore = useI18nStore()
  i18nStore.initialize()

  app.mount("#app")
}
