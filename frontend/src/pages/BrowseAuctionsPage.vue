<template>
  <div class="browse-page">
    <Navbar />
    
    <main class="main-content">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">Find Amazing Deals</h1>
          <p class="hero-subtitle">Bid on unique items from sellers around the world</p>
        </div>
      </section>

      <!-- Updated categories with full-width spacing, light grey circles, and darker grey SVG icons -->
      <section class="categories-section">
        <div class="section-header">
          <h2 class="section-title">Top Categories</h2>
          <button class="see-all-btn">See All</button>
        </div>
        <div class="categories-grid">
          <div v-for="category in categories" :key="category.name" class="category-card">
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
            <span class="category-name">{{ category.name }}</span>
          </div>
        </div>
      </section>

      <!-- Featured Auctions -->
      <section class="auctions-section">
        <div class="section-header">
          <h2 class="section-title">Featured Auctions</h2>
          <button class="see-all-btn">See All</button>
        </div>
        <div class="auctions-grid">
          <router-link 
            v-for="auction in filteredAuctions" 
            :key="auction.id" 
            :to="`/auction/${auction.id}`"
            class="auction-card"
          >
            <div class="auction-image">
              <img :src="auction.image" :alt="auction.title" />
              <span v-if="auction.discount" class="discount-badge">{{ auction.discount }}% OFF</span>
              <button class="favorite-btn" @click.prevent>
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
                </svg>
              </button>
            </div>
            <div class="auction-details">
              <h3 class="auction-title">{{ auction.title }}</h3>
              <div class="auction-price">
                <span class="current-price">{{ formatPrice(auction.currentPrice) }}</span>
                <span v-if="auction.originalPrice" class="original-price">{{ formatPrice(auction.originalPrice) }}</span>
              </div>
              <div class="auction-meta">
                <span class="bids-count">{{ auction.bids }} bids</span>
                <span class="time-left">{{ auction.timeLeft }}</span>
              </div>
            </div>
          </router-link>
        </div>
      </section>

      <!-- Ending Soon -->
      <section class="auctions-section">
        <div class="section-header">
          <h2 class="section-title">Ending Soon</h2>
          <button class="see-all-btn">See All</button>
        </div>
        <div class="auctions-grid">
          <router-link 
            v-for="auction in endingSoon" 
            :key="auction.id" 
            :to="`/auction/${auction.id}`"
            class="auction-card"
          >
            <div class="auction-image">
              <img :src="auction.image" :alt="auction.title" />
              <span class="ending-badge">Ends in {{ auction.timeLeft }}</span>
            </div>
            <div class="auction-details">
              <h3 class="auction-title">{{ auction.title }}</h3>
              <div class="auction-price">
                <span class="current-price">{{ formatPrice(auction.currentPrice) }}</span>
              </div>
              <div class="auction-meta">
                <span class="bids-count">{{ auction.bids }} bids</span>
              </div>
            </div>
          </router-link>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <p>2026 AuctionHub. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const route = useRoute()

const categories = ref([
  { name: 'Electronics' },
  { name: 'Fashion' },
  { name: 'Home' },
  { name: 'Sports' },
  { name: 'Art' },
  { name: 'Vehicles' }
])

const auctions = ref([
  {
    id: 1,
    title: 'Apple Watch Series 6',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 45000,
    originalPrice: 55000,
    discount: 18,
    bids: 24,
    timeLeft: '2d 5h'
  },
  {
    id: 2,
    title: 'Vintage Camera Collection',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 32000,
    bids: 18,
    timeLeft: '1d 12h'
  },
  {
    id: 3,
    title: 'Nike Air Force 1',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 12500,
    originalPrice: 15000,
    discount: 17,
    bids: 45,
    timeLeft: '3d 8h'
  },
  {
    id: 4,
    title: 'MacBook Pro M3',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 180000,
    bids: 12,
    timeLeft: '5d 2h'
  },
  {
    id: 5,
    title: 'Antique Wooden Table',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 75000,
    bids: 8,
    timeLeft: '4d 18h'
  },
  {
    id: 6,
    title: 'Sony Headphones WH-1000XM5',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 28000,
    originalPrice: 35000,
    discount: 20,
    bids: 31,
    timeLeft: '2d 1h'
  },
  {
    id: 7,
    title: 'Designer Handbag',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 95000,
    bids: 15,
    timeLeft: '6d 4h'
  },
  {
    id: 8,
    title: 'Gaming Console Bundle',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 55000,
    bids: 52,
    timeLeft: '1d 6h'
  }
])

const endingSoon = ref([
  {
    id: 9,
    title: 'Rare Pokemon Cards',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 125000,
    bids: 89,
    timeLeft: '2h 30m'
  },
  {
    id: 10,
    title: 'Signed Football Jersey',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 42000,
    bids: 34,
    timeLeft: '4h 15m'
  },
  {
    id: 11,
    title: 'Vintage Rolex Watch',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 450000,
    bids: 23,
    timeLeft: '1h 45m'
  },
  {
    id: 12,
    title: 'Limited Edition Sneakers',
    image: '/placeholder.svg?height=200&width=200',
    currentPrice: 38000,
    bids: 67,
    timeLeft: '3h 20m'
  }
])

const searchQuery = computed(() => route.query.search as string || '')

const filteredAuctions = computed(() => {
  if (!searchQuery.value) return auctions.value
  const query = searchQuery.value.toLowerCase()
  return auctions.value.filter(auction => 
    auction.title.toLowerCase().includes(query)
  )
})

const formatPrice = (price: number): string => {
  return '£' + price.toLocaleString()
}
</script>

<style scoped>
.browse-page {
  min-height: 100vh;
  background: #f9fafb;
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
  text-align: center;
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
  color: #ea580c;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.2s;
}

.see-all-btn:hover {
  color: #c2410c;
}

/* Updated categories grid to be centered with bigger circles */
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

/* Category icons as larger circles with light grey background */
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
  background: #ea580c;
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

.favorite-btn {
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

.favorite-btn:hover {
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
  background: #111827;
  padding: 2rem;
  margin-top: 4rem;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  text-align: center;
  color: #9ca3af;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .main-content {
    padding: 0 1rem 2rem;
  }

  .hero-section {
    padding: 2rem 1.5rem;
  }

  .hero-title {
    font-size: 1.75rem;
  }

  /* Allow wrapping on mobile but still spread out */
  .categories-grid {
    flex-wrap: wrap;
    justify-content: space-around;
    gap: 1.5rem;
    padding: 0;
  }

  .category-icon {
    width: 64px;
    height: 64px;
  }

  .category-icon svg {
    width: 28px;
    height: 28px;
  }

  .auctions-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}
</style>
