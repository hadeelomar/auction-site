<template>
  <div class="page-wrapper">
    <Navbar />
    
    <main class="main-content">
      <div class="page-container">
        <div class="page-header">
          <h1 class="page-title">My Bids</h1>
          <p class="page-description">Track all your active and past bids</p>
        </div>

        <!-- tabs -->
        <div class="tabs">
          <button :class="['tab', { active: activeTab === 'active' }]" @click="activeTab = 'active'">Active Bids</button>
          <button :class="['tab', { active: activeTab === 'won' }]" @click="activeTab = 'won'">Won</button>
          <button :class="['tab', { active: activeTab === 'lost' }]" @click="activeTab = 'lost'">Lost</button>
        </div>

        <!-- Rebid Message -->
        <div v-if="rebidMessage" :class="['rebid-message', rebidMessageType]">
          {{ rebidMessage }}
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Loading your bids...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <p>{{ error }}</p>
          <button class="retry-btn" @click="fetchUserBids">Try Again</button>
        </div>

        <!-- bids list -->
        <div v-else class="bids-list">
          <div v-for="bid in filteredBids" :key="bid.id" class="bid-card">
            <div class="bid-image">
              <img v-if="bid.image" :src="bid.image" :alt="bid.title" />
              <div v-else class="no-image">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
                  <circle cx="9" cy="9" r="2"/>
                  <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                </svg>
              </div>
            </div>
            <div class="bid-details">
              <h3 class="bid-title">{{ bid.title }}</h3>
              <div class="bid-info">
                <span class="bid-amount">Your bid: <strong>{{ formatPrice(bid.yourBid) }}</strong></span>
                <span class="bid-current">Current: <strong>{{ formatPrice(bid.currentBid) }}</strong></span>
              </div>
              <div class="bid-meta">
                <span :class="['bid-status', bid.status]">{{ bid.statusText }}</span>
                <span class="bid-time">{{ bid.timeLeft }}</span>
              </div>
              
              <!-- Rebid Form -->
              <div v-if="rebidItemId === bid.id" class="rebid-form">
                <div class="rebid-input-group">
                  <span class="currency-symbol">£</span>
                  <input
                    type="number"
                    v-model="rebidAmount"
                    :min="parseFloat(bid.currentBid) + 1"
                    :placeholder="`Min: £${(parseFloat(bid.currentBid) + 1).toLocaleString()}`"
                    class="rebid-input"
                    :disabled="isSubmittingRebid"
                  />
                </div>
                <div class="rebid-form-actions">
                  <button @click="closeRebidForm" class="cancel-btn" :disabled="isSubmittingRebid">Cancel</button>
                  <button @click="submitRebid(bid.id, bid.currentBid)" class="submit-rebid-btn" :disabled="isSubmittingRebid || !rebidAmount">
                    {{ isSubmittingRebid ? 'Placing...' : 'Place Bid' }}
                  </button>
                </div>
              </div>
            </div>
            <div class="bid-actions">
              <button 
                v-if="bid.status === 'outbid' && rebidItemId !== bid.id" 
                class="rebid-button"
                @click="openRebidForm(bid.id, bid.currentBid)"
              >
                Rebid
              </button>
              <router-link :to="`/auction/${bid.id}`" class="view-button">View</router-link>
            </div>
          </div>

          <div v-if="filteredBids.length === 0" class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="m14.5 12.5-8 8a2.119 2.119 0 1 1-3-3l8-8"/>
              <path d="m16 16 6-6"/>
              <path d="m8 8 6-6"/>
              <path d="m9 7 8 8"/>
              <path d="m21 11-8-8"/>
            </svg>
            <p>No bids in this category yet</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'

interface Bid {
  id: number
  bid_id: number
  title: string
  image: string | null
  yourBid: string
  currentBid: string
  status: 'winning' | 'outbid' | 'won' | 'lost'
  statusText: string
  timeLeft: string
  endsAt: string
  isActive: boolean
}

const API_BASE_URL = 'http://localhost:8000/api'

const activeTab = ref('active')
const bids = ref<Bid[]>([])
const isLoading = ref(true)
const error = ref<string | null>(null)

const rebidItemId = ref<number | null>(null)
const rebidAmount = ref<number | null>(null)
const isSubmittingRebid = ref(false)
const rebidMessage = ref<string | null>(null)
const rebidMessageType = ref<'success' | 'error'>('success')

async function fetchUserBids(): Promise<void> {
  isLoading.value = true
  error.value = null

  try {
    const response = await fetch(`${API_BASE_URL}/user/bids/`, {
      credentials: 'include'
    })

    if (!response.ok) {
      if (response.status === 401) {
        error.value = 'Please sign in to view your bids'
      } else {
        error.value = 'Failed to load bids'
      }
      return
    }

    const data = await response.json()
    bids.value = data.bids
  } catch (err) {
    error.value = 'Could not connect to the server'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null
  return null
}

async function submitRebid(itemId: number, currentBid: string): Promise<void> {
  if (!rebidAmount.value) return

  if (rebidAmount.value <= parseFloat(currentBid)) {
    showRebidMessage(`Bid must be greater than £${parseFloat(currentBid).toLocaleString()}`, 'error')
    return
  }

  isSubmittingRebid.value = true
  rebidMessage.value = null

  try {
    const csrfToken = getCookie('csrftoken')
    const response = await fetch(`${API_BASE_URL}/bids/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || ''
      },
      credentials: 'include',
      body: JSON.stringify({
        item_id: itemId,
        bid_amount: rebidAmount.value
      })
    })

    const data = await response.json()

    if (!response.ok) {
      showRebidMessage(data.error || 'Failed to place bid', 'error')
      return
    }

    showRebidMessage('Bid placed successfully!', 'success')
    rebidItemId.value = null
    rebidAmount.value = null
    
    // Refresh bids to get updated data
    await fetchUserBids()
  } catch (err) {
    showRebidMessage('Could not connect to the server', 'error')
    console.error(err)
  } finally {
    isSubmittingRebid.value = false
  }
}

function showRebidMessage(message: string, type: 'success' | 'error'): void {
  rebidMessage.value = message
  rebidMessageType.value = type
  setTimeout(() => {
    rebidMessage.value = null
  }, 5000)
}

function openRebidForm(itemId: number, currentBid: string): void {
  rebidItemId.value = itemId
  rebidAmount.value = Math.ceil(parseFloat(currentBid) + 1)
  rebidMessage.value = null
}

function closeRebidForm(): void {
  rebidItemId.value = null
  rebidAmount.value = null
}

const filteredBids = computed(() => {
  if (activeTab.value === 'active') return bids.value.filter(b => b.status === 'winning' || b.status === 'outbid')
  if (activeTab.value === 'won') return bids.value.filter(b => b.status === 'won')
  if (activeTab.value === 'lost') return bids.value.filter(b => b.status === 'lost')
  return bids.value
})

const formatPrice = (price: string | number): string => {
  const num = typeof price === 'string' ? parseFloat(price) : price
  return '£' + num.toLocaleString()
}

onMounted(() => {
  fetchUserBids()
})
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  background: #f9fafb;
}

.main-content {
  max-width: 900px;
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

.page-header {
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.5rem;
}

.page-description {
  color: #6b7280;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

.tab {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  background: none;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.tab:hover {
  color: #111827;
  background: #f3f4f6;
}

.tab.active {
  color: #ea580c;
  background: #fff7ed;
}

.bids-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bid-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.2s;
}

.bid-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.bid-image {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.bid-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.bid-details {
  flex: 1;
}

.bid-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.5rem;
}

.bid-info {
  display: flex;
  gap: 1.5rem;
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.bid-info strong {
  color: #111827;
}

.bid-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.bid-status {
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 50px;
}

.bid-status.winning {
  background: #d1fae5;
  color: #059669;
}

.bid-status.outbid {
  background: #fee2e2;
  color: #dc2626;
}

.bid-status.won {
  background: #dbeafe;
  color: #2563eb;
}

.bid-status.lost {
  background: #f3f4f6;
  color: #6b7280;
}

.bid-time {
  font-size: 0.8125rem;
  color: #9ca3af;
}

.bid-actions {
  display: flex;
  gap: 0.5rem;
}

.rebid-button, .view-button {
  padding: 0.5rem 1rem;
  font-size: 0.8125rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.rebid-button {
  color: #ffffff;
  background: linear-gradient(135deg, #ea580c, #f97316);
  border: none;
}

.view-button {
  color: #374151;
  background: #ffffff;
  border: 1px solid #d1d5db;
}

.view-button:hover {
  background: #f3f4f6;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  color: #9ca3af;
  text-align: center;
}

.empty-state svg {
  margin-bottom: 1rem;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  color: #6b7280;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #ea580c;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  color: #9ca3af;
  text-align: center;
}

.error-state svg {
  margin-bottom: 1rem;
  color: #ef4444;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #ea580c;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.retry-btn:hover {
  background: #dc4c07;
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  color: #9ca3af;
}

.rebid-message {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.rebid-message.success {
  background: #d1fae5;
  color: #065f46;
}

.rebid-message.error {
  background: #fee2e2;
  color: #991b1b;
}

.rebid-form {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 8px;
}

.rebid-input-group {
  display: flex;
  align-items: center;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.rebid-input-group .currency-symbol {
  padding: 0 0.5rem;
  color: #6b7280;
  font-weight: 500;
}

.rebid-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.5rem 0.5rem 0.5rem 0;
  font-size: 0.875rem;
  outline: none;
}

.rebid-input:disabled {
  opacity: 0.6;
}

.rebid-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.cancel-btn {
  padding: 0.375rem 0.75rem;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  color: #6b7280;
  cursor: pointer;
  font-size: 0.75rem;
}

.cancel-btn:hover {
  background: #f3f4f6;
}

.submit-rebid-btn {
  padding: 0.375rem 0.75rem;
  background: #ea580c;
  border: none;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  font-size: 0.75rem;
  font-weight: 500;
}

.submit-rebid-btn:hover:not(:disabled) {
  background: #dc4c07;
}

.submit-rebid-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .bid-card {
    flex-direction: column;
    text-align: center;
  }
  
  .bid-info {
    justify-content: center;
  }
  
  .bid-meta {
    justify-content: center;
  }
}
</style>
