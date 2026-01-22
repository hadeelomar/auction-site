<template>
  <div class="page-wrapper">
    <Navbar />
    
    <main class="main-content">
      <div class="page-container">
        <div class="page-header">
          <div class="header-content">
            <h1 class="page-title">{{ t('myAuctions.title') }}</h1>
            <p class="page-description">{{ t('myAuctions.description') }}</p>
          </div>
          <router-link to="/create" class="create-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14"/>
              <path d="M12 5v14"/>
            </svg>
            {{ t('myAuctions.newAuction') }}
          </router-link>
        </div>

        <!-- Loading state -->
        <div v-if="loading" class="loading-state">
          <p>{{ t('myAuctions.loading') }}</p>
        </div>
        
        <!-- Error state -->
        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <button @click="fetchMyAuctions" class="retry-button">{{ t('common.retry') }}</button>
        </div>
        
        <!-- auctions list -->
        <div v-else class="auctions-list">
          <div v-for="auction in auctions" :key="auction.id" class="auction-card">
            <div class="auction-image">
              <img :src="auction.image || '/placeholder.svg?height=80&width=80'" :alt="auction.title" />
            </div>
            <div class="auction-details">
              <h3 class="auction-title">{{ auction.title }}</h3>
              <div class="auction-stats">
                <span class="stat">
                  <strong>{{ formatPrice(auction.current_price) }}</strong> {{ t('myAuctions.currentBid') }}
                </span>
                <span class="stat">
                  <strong>{{ auction.bid_count }}</strong> {{ t('browse.bids') }}
                </span>
              </div>
              <div class="auction-meta">
                <span :class="['auction-status', auction.ends_at > new Date().toISOString() ? 'active' : 'ended']">
                  {{ auction.ends_at > new Date().toISOString() ? t('auction.active') : t('auction.ended') }}
                </span>
                <span class="auction-time">{{ auction.time_left }}</span>
              </div>
            </div>
            <div class="auction-actions">
              <button 
                @click="handleEdit(auction)" 
                class="edit-button"
                :disabled="auction.bid_count > 0"
                :title="auction.bid_count > 0 ? 'Cannot edit auction with bids' : 'Edit auction'"
              >
                {{ t('common.edit') }}
              </button>
              <button 
                @click="handleDelete(auction)" 
                class="delete-button"
                :disabled="deletingAuction === auction.id || auction.bid_count > 0"
                :title="auction.bid_count > 0 ? 'Cannot delete auction with bids' : 'Delete auction'"
              >
                {{ deletingAuction === auction.id ? t('myAuctions.deleting') : t('common.delete') }}
              </button>
            </div>
          </div>

          <div v-if="auctions.length === 0" class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>
              <path d="m3.3 7 8.7 5 8.7-5"/>
              <path d="M12 22V12"/>
            </svg>
            <p>{{ t('myAuctions.noAuctions') }}</p>
            <router-link to="/create" class="empty-create-button">{{ t('myAuctions.createFirst') }}</router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import Navbar from '../components/Navbar.vue'
import { useI18nStore } from '../stores/i18n'

const { t } = useI18n()
const i18nStore = useI18nStore()

interface Auction {
  id: number
  title: string
  description: string
  image: string | null
  starting_price: number
  current_price: number
  bid_count: number
  time_left: string
  ends_at: string
  category: string
  owner: {
    id: number
    username: string
    first_name: string
    last_name: string
  }
}

const auctions = ref<Auction[]>([])
const loading = ref(true)
const error = ref('')
const deletingAuction = ref<number | null>(null)

const router = useRouter()

const formatPrice = (price: number): string => i18nStore.formatPrice(price)

const fetchMyAuctions = async () => {
  try {
    loading.value = true
    error.value = ''
    
    // Get current user info first
    const userResponse = await fetch('/api/auth/user/')
    if (!userResponse.ok) {
      throw new Error('Failed to get user info')
    }
    
    const userData = await userResponse.json()
    if (!userData.is_authenticated) {
      // User not logged in, keep empty state
      auctions.value = []
      return
    }
    
    // Fetch auctions for this user
    const response = await fetch(`/api/auctions/search/?owner=${userData.username}`)
    if (!response.ok) {
      throw new Error('Failed to fetch auctions')
    }
    
    const data = await response.json()
    auctions.value = data.auctions
    
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load auctions'
    console.error('Error fetching my auctions:', err)
  } finally {
    loading.value = false
  }
}

const handleEdit = (auction: Auction) => {
  // Navigate to edit page with auction ID
  router.push(`/edit/${auction.id}`)
}

const handleDelete = async (auction: Auction) => {
  if (!confirm(`Are you sure you want to delete "${auction.title}"? This action cannot be undone.`)) {
    return
  }
  
  try {
    deletingAuction.value = auction.id
    
    const response = await fetch(`/api/auctions/${auction.id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Failed to delete auction')
    }
    
    // Remove auction from list
    auctions.value = auctions.value.filter(a => a.id !== auction.id)
    
  } catch (err) {
    alert(err instanceof Error ? err.message : 'Failed to delete auction')
  } finally {
    deletingAuction.value = null
  }
}

onMounted(() => {
  fetchMyAuctions()
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

.edit-button:disabled, .delete-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

.loading-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #6b7280;
  font-size: 1.125rem;
}

.error-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #dc2626;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #ea580c;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.retry-button:hover {
  background: #c2410c;
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
