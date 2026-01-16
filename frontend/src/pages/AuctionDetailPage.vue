<template>
  <div class="page-wrapper">
    <Navbar />
    
    <main class="main-content">
      <div class="page-container">
        <!-- Back Button -->
        <button class="back-btn" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m15 18-6-6 6-6"/>
          </svg>
          Back to Auctions
        </button>

        <!-- Loading State -->
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Loading auction details...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
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
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
                    <circle cx="9" cy="9" r="2"/>
                    <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                  </svg>
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
                  <span class="price-value">{{ formatPrice(auction.starting_price) }}</span>
                </div>
                <div class="price-item current">
                  <span class="price-label">Current Price</span>
                  <span class="price-value highlight">{{ formatPrice(auction.current_price) }}</span>
                </div>
              </div>

              <div class="auction-meta">
                <div class="meta-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  <span class="meta-label">Seller:</span>
                  <span class="meta-value">{{ ownerName }}</span>
                </div>
                <div class="meta-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect width="18" height="18" x="3" y="4" rx="2" ry="2"/>
                    <line x1="16" x2="16" y1="2" y2="6"/>
                    <line x1="8" x2="8" y1="2" y2="6"/>
                    <line x1="3" x2="21" y1="10" y2="10"/>
                  </svg>
                  <span class="meta-label">Listed:</span>
                  <span class="meta-value">{{ formatDate(auction.created_at) }}</span>
                </div>
                <div class="meta-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                  </svg>
                  <span class="meta-label">Ends:</span>
                  <span class="meta-value">{{ formatDate(auction.ends_at) }}</span>
                </div>
              </div>

              <!-- Bidding Section -->
              <div class="bidding-section">
                <h3>Place a Bid</h3>
                <p class="placeholder-text">Bidding interface coming soon (Issue #13)</p>
              </div>
            </div>
          </div>

          <!-- Q&A Section -->
          <div class="qa-section">
            <h2>Questions & Answers</h2>
            <div class="qa-placeholder">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
              <p>Q&A section coming soon (Issue #15)</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'

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

const auction = ref<AuctionItem | null>(null)
const isLoading = ref(true)
const error = ref<string | null>(null)

const API_BASE_URL = 'http://localhost:8000/api'

const ownerName = computed(() => {
  if (!auction.value?.owner) return 'Unknown'
  const { first_name, last_name, email } = auction.value.owner
  if (first_name || last_name) {
    return `${first_name} ${last_name}`.trim()
  }
  return email
})

function formatPrice(price: string): string {
  return '£' + parseFloat(price).toFixed(2)
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
  router.push({ name: 'home' })
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
.page-wrapper {
  min-height: 100vh;
  background: #f9fafb;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-container {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  border: 1px solid #e5e7eb;
  color: #6b7280;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #f3f4f6;
  color: #111827;
  border-color: #d1d5db;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  color: #6b7280;
  gap: 1rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #ea580c;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.retry-btn {
  margin-top: 0.5rem;
  background: linear-gradient(135deg, #ea580c, #f97316);
  border: none;
  color: #fff;
  padding: 0.625rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.retry-btn:hover {
  box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
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
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  overflow: hidden;
}

.auction-image-container {
  aspect-ratio: 4/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9fafb;
}

.auction-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  color: #9ca3af;
  font-size: 0.875rem;
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
  color: #111827;
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.3;
}

.status-badge {
  padding: 0.375rem 0.875rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  flex-shrink: 0;
}

.status-badge.active {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.ended {
  background: #fee2e2;
  color: #991b1b;
}

.auction-description {
  color: #6b7280;
  line-height: 1.7;
  margin: 0;
}

.price-section {
  display: flex;
  gap: 2rem;
  padding: 1.25rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.price-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.price-label {
  color: #6b7280;
  font-size: 0.8125rem;
}

.price-value {
  color: #111827;
  font-size: 1.5rem;
  font-weight: 700;
}

.price-value.highlight {
  color: #ea580c;
}

.auction-meta {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
  padding: 1.25rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
}

.meta-item svg {
  flex-shrink: 0;
}

.meta-label {
  font-size: 0.875rem;
}

.meta-value {
  color: #111827;
  font-size: 0.875rem;
  font-weight: 500;
}

.bidding-section {
  padding: 1.5rem;
  background: #fff7ed;
  border: 2px dashed #fed7aa;
  border-radius: 12px;
  text-align: center;
}

.bidding-section h3 {
  color: #111827;
  margin: 0 0 0.5rem 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.placeholder-text {
  color: #9a3412;
  margin: 0;
  font-size: 0.875rem;
}

.qa-section {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 1.5rem;
}

.qa-section h2 {
  color: #111827;
  margin: 0 0 1rem 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.qa-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 2rem;
  background: #f9fafb;
  border: 2px dashed #e5e7eb;
  border-radius: 12px;
  color: #9ca3af;
}

.qa-placeholder p {
  margin: 0;
  font-size: 0.875rem;
}
</style>
