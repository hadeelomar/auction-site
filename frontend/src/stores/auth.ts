import { defineStore } from "pinia"
import { ref } from "vue"

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  profile_image: string | null
  date_of_birth: string | null
}

const API_BASE_URL = "http://localhost:8000/api"

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop()?.split(";").shift() || null
  return null
}

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function fetchCsrfToken() {
    try {
      await fetch(`${API_BASE_URL}/auth/csrf/`, {
        credentials: "include",
      })
    } catch (err) {
      console.error("Failed to fetch CSRF token:", err)
    }
  }

  async function signup(fullName: string, email: string, password: string, passwordConfirm: string, dateOfBirth: string) {
    isLoading.value = true
    error.value = null

    try {
      await fetchCsrfToken()
      const csrfToken = getCookie("csrftoken")

      const response = await fetch(`${API_BASE_URL}/auth/signup/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken || "",
        },
        credentials: "include",
        body: JSON.stringify({
          full_name: fullName,
          email,
          password,
          password_confirm: passwordConfirm,
          date_of_birth: dateOfBirth
        }),
      })

      const data = await response.json()

      if (response.ok) {
        user.value = data.user
        isAuthenticated.value = true
        return { success: true }
      } else {
        error.value = data.error || "Signup failed"
        return { success: false, error: error.value }
      }
    } catch (err) {
      error.value = "Network error. Please try again."
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  async function login(email: string, password: string) {
    isLoading.value = true
    error.value = null

    try {
      await fetchCsrfToken()
      const csrfToken = getCookie("csrftoken")

      const response = await fetch(`${API_BASE_URL}/auth/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken || "",
        },
        credentials: "include",
        body: JSON.stringify({
          email,
          password,
        }),
      })

      const data = await response.json()

      if (response.ok) {
        user.value = data.user
        isAuthenticated.value = true
        return { success: true }
      } else {
        error.value = data.error || "Invalid credentials"
        return { success: false, error: error.value }
      }
    } catch (err) {
      error.value = "Network error. Please try again."
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    isLoading.value = true
    error.value = null

    try {
      await fetchCsrfToken()
      const csrfToken = getCookie("csrftoken")

      const response = await fetch(`${API_BASE_URL}/auth/logout/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken || "",
        },
        credentials: "include",
      })

      if (response.ok) {
        user.value = null
        isAuthenticated.value = false
        return { success: true }
      } else {
        error.value = "Logout failed"
        return { success: false, error: error.value }
      }
    } catch (err) {
      error.value = "Network error. Please try again."
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  async function checkAuth() {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/user/`, {
        credentials: "include",
      })

      if (response.ok) {
        const data = await response.json()
        user.value = data
        isAuthenticated.value = true
      } else {
        user.value = null
        isAuthenticated.value = false
      }
    } catch (err) {
      user.value = null
      isAuthenticated.value = false
    }
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    signup,
    login,
    logout,
    checkAuth,
  }
})