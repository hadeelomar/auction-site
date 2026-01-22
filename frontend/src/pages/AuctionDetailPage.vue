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
                
                <!-- Success/Error Messages -->
                <div v-if="bidMessage" :class="['bid-message', bidMessageType]">
                  {{ bidMessage }}
                </div>

                <!-- Bidding Disabled States -->
                <div v-if="!auction.is_active" class="bid-disabled">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                  </svg>
                  <span>This auction has ended</span>
                </div>

                <div v-else-if="isOwnAuction" class="bid-disabled">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                  </svg>
                  <span>You cannot bid on your own auction</span>
                </div>

                <div v-else-if="isHighestBidder" class="bid-disabled winning">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                    <polyline points="22 4 12 14.01 9 11.01"/>
                  </svg>
                  <span>You are the highest bidder!</span>
                </div>

                <!-- Bid Form -->
                <form v-else @submit.prevent="submitBid" class="bid-form">
                  <div class="bid-input-group">
                    <span class="currency-symbol">£</span>
                    <input
                      v-model="bidAmount"
                      type="number"
                      step="0.01"
                      :min="minBidAmount"
                      :placeholder="`Min: ${formatPrice(minBidAmount.toString())}`"
                      class="bid-input"
                      :disabled="isSubmittingBid"
                      required
                    />
                  </div>
                  <button 
                    type="submit" 
                    class="bid-btn"
                    :disabled="isSubmittingBid || !isValidBid"
                  >
                    <span v-if="isSubmittingBid">Placing Bid...</span>
                    <span v-else>Place Bid</span>
                  </button>
                </form>

                <p v-if="auction.is_active && !isOwnAuction && !isHighestBidder" class="bid-hint">
                  Enter an amount greater than {{ formatPrice(auction.current_price) }}
                </p>
              </div>

              <!-- Bid History -->
              <div v-if="bids.length > 0" class="bid-history">
                <h3>Bid History</h3>
                <div class="bid-list">
                  <div v-for="bid in bids" :key="bid.id" class="bid-item">
                    <div class="bid-info">
                      <span class="bidder-name">{{ bid.user.first_name }} {{ bid.user.last_name }}</span>
                      <span class="bid-time">{{ formatRelativeTime(bid.timestamp) }}</span>
                    </div>
                    <span class="bid-amount">{{ formatPrice(bid.bid_amount) }}</span>
                  </div>
                </div>
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import { useAuthStore } from '../stores/auth'

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

interface BidUser {
  id: number
  email: string
  first_name: string
  last_name: string
}

interface Bid {
  id: number
  bid_amount: string
  timestamp: string
  is_winning: boolean
  user: BidUser
}

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const auction = ref<AuctionItem | null>(null)
const isLoading = ref(true)
const error = ref<string | null>(null)
const bids = ref<Bid[]>([])
const bidAmount = ref<number | null>(null)
const isSubmittingBid = ref(false)
const bidMessage = ref<string | null>(null)
const bidMessageType = ref<'success' | 'error'>('success')
let pollingInterval: ReturnType<typeof setInterval> | null = null

const API_BASE_URL = 'http://localhost:8000/api'

const ownerName = computed(() => {
  if (!auction.value?.owner) return 'Unknown'
  const { first_name, last_name, email } = auction.value.owner
  if (first_name || last_name) {
    return `${first_name} ${last_name}`.trim()
  }
  return email
})

const currentUserId = computed(() => authStore.user?.id ?? null)

const isOwnAuction = computed(() => {
  if (!auction.value || !currentUserId.value) return false
  return auction.value.owner.id === currentUserId.value
})

const isHighestBidder = computed(() => {
  if (!currentUserId.value || bids.value.length === 0) return false
  const highestBid = bids.value[0]
  return highestBid.user.id === currentUserId.value
})

const minBidAmount = computed(() => {
  if (!auction.value) return 0
  return parseFloat(auction.value.current_price) + 0.01
})

const isValidBid = computed(() => {
  if (!bidAmount.value || !auction.value) return false
  return bidAmount.value > parseFloat(auction.value.current_price)
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

function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffSecs = Math.floor(diffMs / 1000)
  const diffMins = Math.floor(diffSecs / 60)
  const diffHours = Math.floor(diffMins / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffSecs < 60) return 'just now'
  if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
  return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
}

function goBack(): void {
  router.push({ name: 'home' })
}

function showMessage(message: string, type: 'success' | 'error'): void {
  bidMessage.value = message
  bidMessageType.value = type
  setTimeout(() => {
    bidMessage.value = null
  }, 5000)
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
    await fetchBids()
  } catch (err) {
    error.value = 'Could not connect to the server'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

async function fetchBids(): Promise<void> {
  if (!auction.value) return

  try {
    const response = await fetch(`${API_BASE_URL}/auctions/${auction.value.id}/`, {
      credentials: 'include'
    })

    if (response.ok) {
      const data = await response.json()
      const newPrice = data.item.current_price
      
      if (auction.value && newPrice !== auction.value.current_price) {
        auction.value.current_price = newPrice
        auction.value.is_active = data.item.is_active
      }
    }
  } catch (err) {
    console.error('Failed to fetch bids:', err)
  }
}

async function submitBid(): Promise<void> {
  if (!auction.value || !bidAmount.value || !isValidBid.value) return

  isSubmittingBid.value = true
  bidMessage.value = null

  try {
    const response = await fetch(`${API_BASE_URL}/bids/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        item_id: auction.value.id,
        bid_amount: bidAmount.value.toFixed(2)
      })
    })

    const data = await response.json()

    if (!response.ok) {
      showMessage(data.error || 'Failed to place bid', 'error')
      return
    }

    auction.value.current_price = data.item.current_price
    auction.value.is_active = data.item.is_active
    
    bids.value.unshift(data.bid)
    
    bidAmount.value = null
    showMessage('Bid placed successfully!', 'success')
  } catch (err) {
    showMessage('Could not connect to the server', 'error')
    console.error(err)
  } finally {
    isSubmittingBid.value = false
  }
}

function startPolling(): void {
  pollingInterval = setInterval(async () => {
    if (auction.value?.is_active) {
      await fetchBids()
    } else {
      stopPolling()
    }
  }, 7000)
}

function stopPolling(): void {
  if (pollingInterval) {
    clearInterval(pollingInterval)
    pollingInterval = null
  }
}

onMounted(async () => {
  await fetchAuction()
  if (auction.value?.is_active) {
    startPolling()
  }
})

onUnmounted(() => {
  stopPolling()
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
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.bidding-section h3 {
  color: #111827;
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.bid-message {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.bid-message.success {
  background: #d1fae5;
  color: #065f46;
}

.bid-message.error {
  background: #fee2e2;
  color: #991b1b;
}

.bid-disabled {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  background: #f3f4f6;
  border-radius: 8px;
  color: #6b7280;
  font-size: 0.875rem;
}

.bid-disabled.winning {
  background: #d1fae5;
  color: #065f46;
}

.bid-form {
  display: flex;
  gap: 0.75rem;
}

.bid-input-group {
  flex: 1;
  display: flex;
  align-items: center;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.currency-symbol {
  padding: 0 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

.bid-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.75rem 0.75rem 0.75rem 0;
  font-size: 1rem;
  color: #111827;
  outline: none;
}

.bid-input::placeholder {
  color: #9ca3af;
}

.bid-input:disabled {
  opacity: 0.6;
}

.bid-btn {
  background: linear-gradient(135deg, #ea580c, #f97316);
  border: none;
  color: #fff;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.2s;
  white-space: nowrap;
}

.bid-btn:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
}

.bid-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.bid-hint {
  margin: 0.75rem 0 0 0;
  color: #6b7280;
  font-size: 0.8125rem;
}

.bid-history {
  padding: 1.5rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.bid-history h3 {
  color: #111827;
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.bid-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.bid-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 8px;
}

.bid-info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.bidder-name {
  color: #111827;
  font-weight: 500;
  font-size: 0.875rem;
}

.bid-time {
  color: #9ca3af;
  font-size: 0.75rem;
}

.bid-amount {
  color: #ea580c;
  font-weight: 700;
  font-size: 1rem;
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
