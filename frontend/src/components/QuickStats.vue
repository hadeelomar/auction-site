<template>
  <div class="quick-stats">
    <h3 class="stats-title">Quick Stats</h3>
    <div class="stats-list">
      <div class="stat-item">
        <span class="stat-label">Win Rate</span>
        <span class="stat-value">32%</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" style="width: 32%"></div>
      </div>

      <div class="stat-item">
        <span class="stat-label">Active Bids</span>
        <span class="stat-value">12</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill progress-blue" style="width: 60%"></div>
      </div>

      <div class="stat-item">
        <span class="stat-label">Items Listed</span>
        <span class="stat-value">8</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill progress-green" style="width: 80%"></div>
      </div>
    </div>

    <div class="top-items">
      <h4 class="items-title">Top Auctions</h4>
      <div class="items-list">
        <div v-for="(item, i) in topItems" :key="i" class="item-row">
          <span class="item-name">{{ item.name }}</span>
          <span class="item-price">{{ item.price }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const topItems = [
  { name: 'Vintage Camera', price: '£450' },
  { name: 'Antique Watch', price: '£320' },
  { name: 'Rare Painting', price: '£890' },
  { name: 'Classic Guitar', price: '£560' },
]
</script>

<style scoped>
.quick-stats {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.stats-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #f3f4f6;
  margin: 0;
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  font-size: 0.875rem;
  color: #9ca3af;
}

.stat-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #f3f4f6;
}

.progress-bar {
  width: 100%;
  height: 0.5rem;
  background: #1f2937;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #3b82f6;
  border-radius: 9999px;
  transition: width 0.3s;
}

.progress-blue {
  background: #60a5fa;
}

.progress-green {
  background: #34d399;
}

.top-items {
  padding-top: 1.5rem;
  border-top: 1px solid #1f2937;
}

.items-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #f3f4f6;
  margin: 0 0 1rem 0;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.item-name {
  font-size: 0.875rem;
  color: #9ca3af;
}

.item-price {
  font-size: 0.875rem;
  font-weight: 600;
  color: #f3f4f6;
}
</style>
