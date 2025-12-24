<template>
  <div class="overview">
    <div class="stats-grid">
      <StatCard 
        title="Active Auctions"
        value="24"
        change="+12% from last month"
        icon="gavel"
        color="blue"
      />
      <StatCard 
        title="Total Bids"
        value="156"
        change="+23% from last week"
        icon="hand"
        color="green"
      />
      <StatCard 
        title="Won Auctions"
        value="8"
        change="+2 this week"
        icon="trophy"
        color="purple"
      />
      <StatCard 
        title="Total Spent"
        value="£3,240"
        change="+8% from last month"
        icon="dollar"
        color="orange"
      />
    </div>

    <div class="content-grid">
      <div class="activity-section">
        <div class="section-header">
          <h3 class="section-title">Recent Activity</h3>
          <button class="view-all-button">View all</button>
        </div>
        <div class="activity-list">
          <ActivityItem 
            v-for="(activity, i) in activities"
            :key="i"
            :activity="activity"
          />
        </div>
      </div>

      <div class="stats-section">
        <QuickStats />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import StatCard from './StatCard.vue'
import ActivityItem from './ActivityItem.vue'
import QuickStats from './QuickStats.vue'

const activities = [
  { icon: 'gavel', title: 'New bid placed', desc: 'Vintage Camera Auction #1234', time: '2 min ago', color: 'blue' },
  { icon: 'trophy', title: 'Auction won', desc: 'You won the Antique Watch auction', time: '5 min ago', color: 'green' },
  { icon: 'message', title: 'New message', desc: 'Question about Item #5678', time: '10 min ago', color: 'purple' },
  { icon: 'dollar', title: 'Payment received', desc: 'Buyer paid for Item #3456', time: '1 hour ago', color: 'orange' },
  { icon: 'bell', title: 'Auction ending soon', desc: 'Rare Collectible ends in 2 hours', time: '2 hours ago', color: 'red' },
]
</script>

<style scoped>
.overview {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.activity-section,
.stats-section {
  background: #0f1523;
  border: 1px solid #1f2937;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #f3f4f6;
  margin: 0;
}

.view-all-button {
  font-size: 0.875rem;
  font-weight: 500;
  color: #60a5fa;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.2s;
}

.view-all-button:hover {
  color: #93c5fd;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
