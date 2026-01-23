<template>
  <div class="browse-page">
    <Navbar />
    
    <main class="main-content">
      <div class="page-container">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-content">
          <div class="hero-desert">
            <div class="desert-box desert-box-1"></div>
            <div class="desert-box desert-box-2"></div>
            <div class="desert-box desert-box-3"></div>
            <div class="desert-box desert-box-4"></div>
            <div class="desert-circle desert-circle-1"></div>
            <div class="desert-circle desert-circle-2"></div>
            <div class="desert-line desert-line-1"></div>
            <div class="desert-line desert-line-2"></div>
          </div>
          <div class="hero-text">
            <h1 class="hero-title">{{ t('browse.heroTitle') }}</h1>
            <p class="hero-subtitle">{{ t('browse.heroSubtitle') }}</p>
          </div>
        </div>
      </section>

      <section class="categories-section">
        <div class="section-header">
          <h2 class="section-title">{{ t('browse.topCategories') }}</h2>
        </div>
        <div class="categories-grid">
          <div 
            v-for="category in categories" 
            :key="category.name" 
            class="category-card"
            :class="{ active: selectedCategory === category.name }"
            @click="handleCategoryClick(category.name)"
          >
            <div class="category-icon">
              <!-- Electronics -->
              <svg v-if="category.name === 'Electronics'" xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="5" y="2" width="14" height="20" rx="2" ry="2"/>
                <line x1="12" y1="18" x2="12.01" y2="18"/>
              </svg>
              <!-- Fashion -->
              <svg v-else-if="category.name === 'Fashion'" xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>
              </svg>
              <!-- Home -->
              <svg v-else-if="category.name === 'Home'" xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
              <!-- Sports -->
              <svg v-else-if="category.name === 'Sports'" xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>
                <path d="M2 12h20"/>
              </svg>
              <!-- Art -->
              <svg v-else-if="category.name === 'Art'" xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="13.5" cy="6.5" r=".5"/>
                <circle cx="17.5" cy="10.5" r=".5"/>
                <circle cx="8.5" cy="7.5" r=".5"/>
                <circle cx="6.5" cy="12.5" r=".5"/>
                <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.555C21.965 6.012 17.461 2 12 2z"/>
              </svg>
              <!-- Vehicles -->
              <svg v-else-if="category.name === 'Vehicles'" xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/>
                <circle cx="7" cy="17" r="2"/>
                <path d="M9 17h6"/>
                <circle cx="17" cy="17" r="2"/>
              </svg>
            </div>
            <span class="category-name">{{ t('categories.' + category.key) }}</span>
          </div>
        </div>
      </section>

      <!-- Auctions -->
      <section class="auctions-section">
        <div class="section-header">
          <h2 class="section-title">{{ t('browse.auctions') }}</h2>
        </div>
        
        <!-- Loading state -->
        <div v-if="loading" class="loading-state">
          <p>Loading auctions...</p>
        </div>
        
        <!-- Error state -->
        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <button @click="fetchAuctions" class="retry-button">Retry</button>
        </div>
        
        <!-- Empty state -->
        <div v-else-if="filteredAuctions.length === 0" class="empty-state">
          <p>{{ searchQuery || selectedCategory ? 'No auctions found matching your criteria.' : 'No active auctions available.' }}</p>
        </div>
        
        <!-- Auctions grid -->
        <div v-else class="auctions-grid">
          <router-link 
            v-for="auction in filteredAuctions" 
            :key="auction.id" 
            :to="`/auction/${auction.id}`"
            class="auction-card"
          >
            <div class="auction-image">
              <img :src="auction.image || '/placeholder.svg?height=200&width=200'" :alt="auction.title" />
              <span v-if="auction.starting_price > auction.current_price" class="discount-badge">
                {{ Math.round((1 - auction.current_price / auction.starting_price) * 100) }}% OFF
              </span>
              <button class="favourite-btn" @click.prevent>
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
                </svg>
              </button>
            </div>
            <div class="auction-details">
              <h3 class="auction-title">{{ auction.title }}</h3>
              <div class="auction-price">
                <span class="current-price">{{ formatPrice(auction.current_price) }}</span>
                <span v-if="auction.starting_price > auction.current_price" class="original-price">{{ formatPrice(auction.starting_price) }}</span>
              </div>
              <div class="auction-meta">
                <span class="bids-count">{{ auction.bid_count }} {{ t('browse.bids') }}</span>
                <span class="time-left">{{ auction.time_left }}</span>
              </div>
            </div>
          </router-link>
        </div>
      </section>

      </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <p>2026 Bido. {{ t('footer.allRightsReserved') }}</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
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

const route = useRoute()

const categories = ref([
  { name: 'Electronics', key: 'electronics' },
  { name: 'Fashion', key: 'fashion' },
  { name: 'Home', key: 'home' },
  { name: 'Sports', key: 'sports' },
  { name: 'Art', key: 'art' },
  { name: 'Vehicles', key: 'vehicles' }
])

const auctions = ref<Auction[]>([])
const endingSoon = ref<Auction[]>([])
const loading = ref(true)
const error = ref('')
const selectedCategory = ref('')

const searchQuery = computed(() => route.query.search as string || '')

const filteredAuctions = computed(() => {
  let filtered = auctions.value
  
  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(auction => 
      auction.title.toLowerCase().includes(query) ||
      auction.description.toLowerCase().includes(query)
    )
  }
  
  // Filter by category
  if (selectedCategory.value) {
    filtered = filtered.filter(auction => 
      auction.category?.toLowerCase() === selectedCategory.value.toLowerCase()
    )
  }
  
  return filtered
})

const formatPrice = (price: number): string => {
  return i18nStore.formatPrice(price)
}

const fetchAuctions = async () => {
  try {
    loading.value = true
    error.value = ''
    
    // Fetch all active auctions from search endpoint
    const response = await fetch('http://localhost:8001/api/auctions/search/?status=active')
    if (!response.ok) {
      throw new Error('Failed to fetch auctions')
    }
    
    const data = await response.json()
    auctions.value = data.auctions
    
    // Get ending soon auctions (next 24 hours)
    const endingSoonResponse = await fetch('http://localhost:8001/api/auctions/search/?status=ending_soon')
    if (endingSoonResponse.ok) {
      const endingSoonData = await endingSoonResponse.json()
      endingSoon.value = endingSoonData.auctions
    }
    
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load auctions'
    console.error('Error fetching auctions:', err)
  } finally {
    loading.value = false
  }
}

const handleCategoryClick = (category: string) => {
  if (selectedCategory.value === category) {
    selectedCategory.value = ''
  } else {
    selectedCategory.value = category
  }
}

onMounted(() => {
  fetchAuctions()
})
</script>

<style scoped>
.browse-page {
  min-height: 100vh;
  background: #f9fafb;
}

.page-container {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem 3rem;
}

.hero-section {
  background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
  border-radius: 20px;
  padding: 3rem;
  margin: 2rem 0;
  position: relative;
  overflow: hidden;
}

.hero-content {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 2;
  gap: 3rem;
}

.hero-desert {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

.hero-text {
  position: relative;
  z-index: 3;
  text-align: center;
  margin-left: 8rem;
}

/* Subtle desert sand boxes */
.desert-box {
  position: absolute;
  background: linear-gradient(135deg, #fed7aa, #fdba74);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(251, 191, 36, 0.1);
}

.desert-box-1 {
  width: 140px;
  height: 90px;
  top: 15%;
  left: 2%;
  transform: rotate(-8deg);
  animation: float 12s ease-in-out infinite;
}

.desert-box-2 {
  width: 100px;
  height: 140px;
  top: 45%;
  left: 8%;
  transform: rotate(12deg);
  animation: float 15s ease-in-out infinite reverse;
}

.desert-box-3 {
  width: 120px;
  height: 70px;
  bottom: 20%;
  left: 4%;
  transform: rotate(-5deg);
  animation: float 10s ease-in-out infinite;
}

.desert-box-4 {
  width: 80px;
  height: 80px;
  top: 30%;
  left: 15%;
  transform: rotate(15deg);
  animation: float 8s ease-in-out infinite reverse;
}

/* Sand particles */
.desert-circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(254, 215, 170, 0.3), rgba(253, 186, 116, 0.2));
}

.desert-circle-1 {
  width: 180px;
  height: 180px;
  top: -40px;
  left: -60px;
  animation: pulse 14s ease-in-out infinite;
}

.desert-circle-2 {
  width: 120px;
  height: 120px;
  bottom: -30px;
  left: 10%;
  animation: pulse 11s ease-in-out infinite reverse;
}

/* Sand drift lines */
.desert-line {
  position: absolute;
  background: linear-gradient(90deg, rgba(254, 215, 170, 0.4), rgba(253, 186, 116, 0.2));
  border-radius: 2px;
}

.desert-line-1 {
  width: 250px;
  height: 2px;
  top: 25%;
  left: -80px;
  transform: rotate(25deg);
  animation: slide 18s ease-in-out infinite;
}

.desert-line-2 {
  width: 180px;
  height: 2px;
  bottom: 35%;
  left: -60px;
  transform: rotate(-20deg);
  animation: slide 14s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(-8deg); }
  50% { transform: translateY(-8px) rotate(-5deg); }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.2; }
  50% { transform: scale(1.05); opacity: 0.3; }
}

@keyframes slide {
  0%, 100% { transform: translateX(0px) rotate(25deg); }
  50% { transform: translateX(20px) rotate(28deg); }
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 650;
  color: #111827;
  margin-bottom: 0.5rem;
}

.hero-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  margin-bottom: 0;
}

.categories-section,
.auctions-section {
  margin-top: 2.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
}

.see-all-btn {
  font-size: 0.875rem;
  font-weight: 500;
  color: #f97316;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.2s;
}

.see-all-btn:hover {
  color: #ea580c;
}

.categories-grid {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 0 1rem;
}

.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.category-card:hover .category-icon {
  background: #e5e7eb;
  color: #374151;
}

.category-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: #f3f4f6;
  color: #6b7280;
  transition: all 0.2s;
}

.category-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.auctions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

.auction-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.2s;
  text-decoration: none;
}

.auction-card:hover {
  border-color: #d1d5db;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}

.auction-image {
  position: relative;
  aspect-ratio: 1;
  background: #f3f4f6;
}

.auction-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.discount-badge {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #ffffff;
  background: linear-gradient(135deg, #ea580c, #f97316);
  border-radius: 6px;
}

.ending-badge {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #ffffff;
  background: #dc2626;
  border-radius: 6px;
}

.favourite-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: #ffffff;
  border: none;
  border-radius: 50%;
  color: #9ca3af;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.favourite-btn:hover {
  color: #ef4444;
}

.auction-details {
  padding: 1rem;
}

.auction-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.auction-price {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.current-price {
  font-size: 1.125rem;
  font-weight: 700;
  color: #ea580c;
}

.original-price {
  font-size: 0.875rem;
  color: #9ca3af;
  text-decoration: line-through;
}

.auction-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8125rem;
  color: #6b7280;
}

.footer {
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  padding: 2rem 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
}

.footer-content p {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

/* Error state styles */
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

/* Empty state styles */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #6b7280;
  font-size: 1.125rem;
}

/* Active category style */
.category-card.active .category-icon {
  background: linear-gradient(135deg, #ea580c, #f97316);
  color: white;
}

.category-card.active .category-name {
  color: #ea580c;
  font-weight: 600;
}

@media (max-width: 768px) {
  .main-content {
    padding: 0 1rem 2rem;
  }

  .hero-section {
    padding: 2rem 1.5rem;
  }

  .hero-content {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
  }

  .hero-text {
    text-align: center;
    order: 2;
    margin-left: 0;
  }

  .hero-desert {
    position: relative;
    width: 100%;
    height: 180px;
    order: 1;
  }

  .desert-box-1 {
    width: 70px;
    height: 45px;
    top: 5%;
    left: 5%;
  }

  .desert-box-2 {
    width: 50px;
    height: 70px;
    top: 35%;
    left: 20%;
  }

  .desert-box-3 {
    width: 60px;
    height: 35px;
    bottom: 15%;
    left: 10%;
  }

  .desert-box-4 {
    width: 40px;
    height: 40px;
    top: 50%;
    left: 35%;
  }

  .desert-circle-1 {
    width: 90px;
    height: 90px;
    top: 0;
    left: -20px;
  }

  .desert-circle-2 {
    width: 70px;
    height: 70px;
    bottom: 0;
    right: 0;
  }

  .desert-line-1 {
    width: 120px;
    height: 1px;
    top: 25%;
    left: -30px;
  }

  .desert-line-2 {
    width: 90px;
    height: 1px;
    bottom: 25%;
    left: -20px;
  }

  .hero-title {
    font-size: 1.75rem;
  }

  .categories-grid {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;
    padding: 0;
    max-width: 320px;
    margin: 0 auto;
  }

  .category-icon {
    width: 90px;
    height: 90px;
  }

  .category-icon svg {
    width: 36px;
    height: 36px;
  }

  .category-name {
    font-size: 0.9rem;
  }

  .auctions-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}
</style>
