<template>
  <!-- Added dashboard wrapper with sidebar and header -->
  <div class="dashboard-wrapper">
    <Sidebar :open="sidebarOpen" @toggle="sidebarOpen = !sidebarOpen" />
    <div class="dashboard-content">
      <DashboardHeader 
        page-title="Create Auction"
        :isDark="isDark" 
        @toggle-theme="isDark = !isDark"
      />
      <main class="main-content">
        <div class="page-container">
          <p class="page-description">List a new item for auction</p>
          <div class="empty-state">
            <p>This page is under construction</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import DashboardHeader from '../components/DashboardHeader.vue'

const sidebarOpen = ref(true)
const isDark = ref(true)
</script>

<style scoped>
/* Added dashboard wrapper styles */
.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background: #0a0e1a;
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

.page-container {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-description {
  color: #9ca3af;
  margin-bottom: 2rem;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background: #0f1523;
  border: 1px solid #1f2937;
  border-radius: 0.75rem;
  color: #6b7280;
}
</style>
