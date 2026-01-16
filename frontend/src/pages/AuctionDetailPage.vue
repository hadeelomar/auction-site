<template>
  <div class="dashboard-wrapper">
    <Sidebar :open="sidebarOpen" @toggle="sidebarOpen = !sidebarOpen" />
    <div class="dashboard-content">
      <DashboardHeader 
        :page-title="pageTitle"
        :isDark="isDark" 
        @toggle-theme="isDark = !isDark"
      />
      <main class="main-content">
        <div class="page-container">
          <!-- Back Button -->
          <button class="back-btn" @click="goBack">
            &larr; Back to Auctions
          </button>

          <!-- Loading State -->
          <div v-if="isLoading" class="loading-state">
            <p>Loading auction details...</p>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="error-state">
            <p>{{ error }}</p>
            <button class="retry-btn" @click="fetchAuction">Try Again</button>
          </div>

          <!-- Auction Details -->
          <div v-else-if="auction" class="auction-detail">
            <div class="auction-grid">
              <!-- Image Section -->
              <div class="auction-image-section">
                <div class="auction-image-container">
                  <img 
                    v-if="auction.image" 
                    :src="auction.image" 
                    :alt="auction.title"
                    class="auction-image"
                  />
                  <div v-else class="no-image">
                    <span>No Image Available</span>
                  </div>
                </div>
              </div>

              <!-- Info Section -->
              <div class="auction-info-section">
                <div class="auction-header">
                  <h1 class="auction-title">{{ auction.title }}</h1>
                  <span :class="['status-badge', auction.is_active ? 'active' : 'ended']">
                    {{ auction.is_active ? 'Active' : 'Ended' }}
                  </span>
                </div>

                <p class="auction-description">{{ auction.description }}</p>

                <div class="price-section">
                  <div class="price-item">
                    <span class="price-label">Starting Price</span>
                    <span class="price-value">${{ formatPrice(auction.starting_price) }}</span>
                  </div>
                  <div class="price-item current">
                    <span class="price-label">Current Price</span>
                    <span class="price-value">${{ formatPrice(auction.current_price) }}</span>
                  </div>
                </div>

                <div class="auction-meta">
                  <div class="meta-item">
                    <span class="meta-label">Seller</span>
                    <span class="meta-value">{{ ownerName }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="meta-label">Listed On</span>
                    <span class="meta-value">{{ formatDate(auction.created_at) }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="meta-label">Ends At</span>
                    <span class="meta-value">{{ formatDate(auction.ends_at) }}</span>
                  </div>
                </div>

                <!-- Bidding Placeholder (Issue #13) -->
                <div class="placeholder-section">
                  <h3>Place a Bid</h3>
                  <p class="placeholder-text">Bidding interface coming soon (Issue #13)</p>
                </div>
              </div>
            </div>

            <!-- Q&A Placeholder (Issue #15) -->
            <div class="qa-section">
              <h2>Questions & Answers</h2>
              <div class="placeholder-section">
                <p class="placeholder-text">Q&A section coming soon (Issue #15)</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import DashboardHeader from '../components/DashboardHeader.vue'

interface AuctionOwner {
  id: number
  email: string
  first_name: string
  last_name: string
}

interface AuctionItem {
  id: number
  title: string
  description: string
  image: string | null
  starting_price: string
  current_price: string
  created_at: string
  ends_at: string
  owner: AuctionOwner
  is_active: boolean
}

const route = useRoute()
const router = useRouter()

const sidebarOpen = ref(true)
const isDark = ref(true)
const auction = ref<AuctionItem | null>(null)
const isLoading = ref(true)
const error = ref<string | null>(null)

const API_BASE_URL = 'http://localhost:8000/api'

const pageTitle = computed(() => {
  return auction.value?.title || 'Auction Details'
})

const ownerName = computed(() => {
  if (!auction.value?.owner) return 'Unknown'
  const { first_name, last_name, email } = auction.value.owner
  if (first_name || last_name) {
    return `${first_name} ${last_name}`.trim()
  }
  return email
})

function formatPrice(price: string): string {
  return parseFloat(price).toFixed(2)
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function goBack(): void {
  router.push({ name: 'browse-auctions' })
}

async function fetchAuction(): Promise<void> {
  const auctionId = route.params.id as string
  
  if (!auctionId) {
    error.value = 'No auction ID provided'
    isLoading.value = false
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const response = await fetch(`${API_BASE_URL}/auctions/${auctionId}/`, {
      credentials: 'include'
    })

    if (!response.ok) {
      if (response.status === 404) {
        error.value = 'Auction not found'
      } else {
        error.value = 'Failed to load auction details'
      }
      return
    }

    const data = await response.json()
    auction.value = data.item
  } catch (err) {
    error.value = 'Could not connect to the server'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchAuction()
})
</script>

<style scoped>
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

.back-btn {
  background: transparent;
  border: 1px solid #374151;
  color: #9ca3af;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  margin-bottom: 1.5rem;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #1f2937;
  color: #fff;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background: #0f1523;
  border: 1px solid #1f2937;
  border-radius: 0.75rem;
  color: #6b7280;
}

.retry-btn {
  margin-top: 1rem;
  background: #3b82f6;
  border: none;
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
}

.retry-btn:hover {
  background: #2563eb;
}

.auction-detail {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.auction-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

@media (max-width: 900px) {
  .auction-grid {
    grid-template-columns: 1fr;
  }
}

.auction-image-section {
  background: #0f1523;
  border: 1px solid #1f2937;
  border-radius: 0.75rem;
  overflow: hidden;
}

.auction-image-container {
  aspect-ratio: 4/3;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auction-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  color: #6b7280;
  font-size: 1rem;
}

.auction-info-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.auction-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.auction-title {
  color: #fff;
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.status-badge.active {
  background: #065f46;
  color: #34d399;
}

.status-badge.ended {
  background: #7f1d1d;
  color: #fca5a5;
}

.auction-description {
  color: #9ca3af;
  line-height: 1.6;
  margin: 0;
}

.price-section {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  background: #0f1523;
  border: 1px solid #1f2937;
  border-radius: 0.75rem;
}

.price-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.price-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.price-value {
  color: #fff;
  font-size: 1.5rem;
  font-weight: 600;
}

.price-item.current .price-value {
  color: #34d399;
}

.auction-meta {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  background: #0f1523;
  border: 1px solid #1f2937;
  border-radius: 0.75rem;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.meta-value {
  color: #d1d5db;
  font-size: 0.875rem;
}

.placeholder-section {
  padding: 1.5rem;
  background: #0f1523;
  border: 1px dashed #374151;
  border-radius: 0.75rem;
  text-align: center;
}

.placeholder-section h3 {
  color: #fff;
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
}

.placeholder-text {
  color: #6b7280;
  margin: 0;
  font-size: 0.875rem;
}

.qa-section {
  background: #0f1523;
  border: 1px solid #1f2937;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.qa-section h2 {
  color: #fff;
  margin: 0 0 1rem 0;
  font-size: 1.25rem;
}
</style>
