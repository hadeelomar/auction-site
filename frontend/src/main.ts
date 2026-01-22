import { createApp } from "vue"
import { createPinia } from "pinia"
import App from "./App.vue"
import router from "./router"

// Check if we're on an auth page and let Django handle it
if (window.location.pathname.startsWith('/login') || window.location.pathname.startsWith('/signup')) {
  // Don't initialize Vue app for auth pages - let Django handle them
} else {
  const app = createApp(App)
  const pinia = createPinia()

  app.use(pinia)
  app.use(router)
  app.mount("#app")
}
