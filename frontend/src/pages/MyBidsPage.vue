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

        <!-- bids list -->
        <div class="bids-list">
          <div v-for="bid in filteredBids" :key="bid.id" class="bid-card">
            <div class="bid-image">
              <img :src="bid.image" :alt="bid.title" />
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
            </div>
            <div class="bid-actions">
              <button v-if="bid.status === 'outbid'" class="rebid-button">Rebid</button>
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
import { ref, computed } from 'vue'
import Navbar from '../components/Navbar.vue'

const activeTab = ref('active')

const bids = ref([
  { id: 1, title: 'Vintage Camera Collection', image: '/placeholder.svg?height=80&width=80', yourBid: 32000, currentBid: 35000, status: 'outbid', statusText: 'Outbid', timeLeft: '1d 12h left' },
  { id: 2, title: 'Apple Watch Series 6', image: '/placeholder.svg?height=80&width=80', yourBid: 45000, currentBid: 45000, status: 'winning', statusText: 'Winning', timeLeft: '2d 5h left' },
  { id: 3, title: 'Rare Pokemon Cards', image: '/placeholder.svg?height=80&width=80', yourBid: 125000, currentBid: 125000, status: 'won', statusText: 'Won', timeLeft: 'Ended' },
  { id: 4, title: 'Gaming Console Bundle', image: '/placeholder.svg?height=80&width=80', yourBid: 52000, currentBid: 58000, status: 'lost', statusText: 'Lost', timeLeft: 'Ended' }
])

const filteredBids = computed(() => {
  if (activeTab.value === 'active') return bids.value.filter(b => b.status === 'winning' || b.status === 'outbid')
  if (activeTab.value === 'won') return bids.value.filter(b => b.status === 'won')
  if (activeTab.value === 'lost') return bids.value.filter(b => b.status === 'lost')
  return bids.value
})

const formatPrice = (price: number): string => '£' + price.toLocaleString()
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
