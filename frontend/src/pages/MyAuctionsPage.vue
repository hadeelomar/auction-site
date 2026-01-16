<template>
  <div class="page-wrapper">
    <Navbar />
    
    <main class="main-content">
      <div class="page-container">
        <div class="page-header">
          <div class="header-content">
            <h1 class="page-title">My Auctions</h1>
            <p class="page-description">Manage auctions you've created</p>
          </div>
          <router-link to="/create" class="create-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14"/>
              <path d="M12 5v14"/>
            </svg>
            New Auction
          </router-link>
        </div>

        <!-- auctions list -->
        <div class="auctions-list">
          <div v-for="auction in auctions" :key="auction.id" class="auction-card">
            <div class="auction-image">
              <img :src="auction.image" :alt="auction.title" />
            </div>
            <div class="auction-details">
              <h3 class="auction-title">{{ auction.title }}</h3>
              <div class="auction-stats">
                <span class="stat">
                  <strong>{{ formatPrice(auction.currentBid) }}</strong> current bid
                </span>
                <span class="stat">
                  <strong>{{ auction.bidsCount }}</strong> bids
                </span>
              </div>
              <div class="auction-meta">
                <span :class="['auction-status', auction.status]">{{ auction.statusText }}</span>
                <span class="auction-time">{{ auction.timeLeft }}</span>
              </div>
            </div>
            <div class="auction-actions">
              <button class="edit-button">Edit</button>
              <button class="delete-button">Delete</button>
            </div>
          </div>

          <div v-if="auctions.length === 0" class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>
              <path d="m3.3 7 8.7 5 8.7-5"/>
              <path d="M12 22V12"/>
            </svg>
            <p>You haven't created any auctions yet</p>
            <router-link to="/create" class="empty-create-button">Create your first auction</router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Navbar from '../components/Navbar.vue'

const auctions = ref([
  { id: 1, title: 'Vintage Camera Collection', image: '/placeholder.svg?height=80&width=80', currentBid: 32000, bidsCount: 18, status: 'active', statusText: 'Active', timeLeft: '1d 12h left' },
  { id: 2, title: 'Antique Wooden Table', image: '/placeholder.svg?height=80&width=80', currentBid: 75000, bidsCount: 8, status: 'active', statusText: 'Active', timeLeft: '4d 18h left' },
  { id: 3, title: 'Rare Vinyl Records', image: '/placeholder.svg?height=80&width=80', currentBid: 15000, bidsCount: 25, status: 'ended', statusText: 'Ended', timeLeft: 'Sold' }
])

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
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
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

.create-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  background: linear-gradient(135deg, #ea580c, #f97316);
  border: none;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
}

.create-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
}

.auctions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.auction-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.2s;
}

.auction-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.auction-image {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.auction-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.auction-details {
  flex: 1;
}

.auction-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.5rem;
}

.auction-stats {
  display: flex;
  gap: 1.5rem;
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.stat strong {
  color: #111827;
}

.auction-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.auction-status {
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 50px;
}

.auction-status.active {
  background: #d1fae5;
  color: #059669;
}

.auction-status.ended {
  background: #f3f4f6;
  color: #6b7280;
}

.auction-time {
  font-size: 0.8125rem;
  color: #9ca3af;
}

.auction-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-button, .delete-button {
  padding: 0.5rem 1rem;
  font-size: 0.8125rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-button {
  color: #374151;
  background: #ffffff;
  border: 1px solid #d1d5db;
}

.edit-button:hover {
  background: #f3f4f6;
}

.delete-button {
  color: #dc2626;
  background: #ffffff;
  border: 1px solid #fecaca;
}

.delete-button:hover {
  background: #fef2f2;
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

.empty-create-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  background: linear-gradient(135deg, #ea580c, #f97316);
  border-radius: 10px;
  text-decoration: none;
}

@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .auction-card {
    flex-direction: column;
    text-align: center;
  }
  
  .auction-stats {
    justify-content: center;
  }
  
  .auction-meta {
    justify-content: center;
  }
}
</style>
