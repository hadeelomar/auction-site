<template>
  <div class="dashboard-wrapper">
    <Sidebar 
      :open="sidebarOpen" 
      :selected="selectedPage"
      @toggle="sidebarOpen = !sidebarOpen"
      @select="selectedPage = $event"
    />
    <div class="dashboard-content">
      <DashboardHeader 
        :isDark="isDark" 
        @toggle-theme="isDark = !isDark"
      />
      <main class="main-content">
        <DashboardOverview v-if="selectedPage === 'Dashboard'" />
        <div v-else class="empty-state">
          <h2>{{ selectedPage }}</h2>
          <p>This page is under construction</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import DashboardHeader from '../components/DashboardHeader.vue'
import DashboardOverview from '../components/DashboardOverview.vue'

const sidebarOpen = ref(true)
const selectedPage = ref('Dashboard')
const isDark = ref(true)

watch(isDark, (newValue) => {
  if (newValue) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}, { immediate: true })
</script>

<style scoped>
.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background: #0a0e1a;
  color: #f3f4f6;
}

.dashboard-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: auto;
}

.main-content {
  flex: 1;
  padding: 2rem;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
  color: #9ca3af;
}

.empty-state h2 {
  font-size: 2rem;
  font-weight: 600;
  color: #f3f4f6;
  margin-bottom: 0.5rem;
}

.empty-state p {
  font-size: 1rem;
}
</style>
