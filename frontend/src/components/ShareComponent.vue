<template>
  <div class="share-component">
    <div class="share-header">
      <h3>{{ t('share.title') }}</h3>
      <button @click="closeShare" class="close-btn">&times;</button>
    </div>
    
    <div class="share-content">
      <!-- Share Buttons -->
      <div class="share-buttons">
        <button 
          @click="shareOnFacebook" 
          class="share-btn facebook"
          :title="t('share.facebook')"
        >
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
          </svg>
          <span>Facebook</span>
        </button>

        <button 
          @click="shareOnTwitter" 
          class="share-btn twitter"
          :title="t('share.twitter')"
        >
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
          </svg>
          <span>Twitter</span>
        </button>

        <button 
          @click="shareOnWhatsApp" 
          class="share-btn whatsapp"
          :title="t('share.whatsapp')"
        >
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.149-.67.149-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414-.074-.123-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
          </svg>
          <span>WhatsApp</span>
        </button>

        <button 
          @click="shareViaEmail" 
          class="share-btn email"
          :title="t('share.email')"
        >
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
          </svg>
          <span>Email</span>
        </button>
      </div>

      <!-- Copy Link -->
      <div class="copy-link-section">
        <div class="input-group">
          <input 
            ref="linkInput"
            :value="shareUrl" 
            readonly 
            class="link-input"
          />
          <button 
            @click="copyLink" 
            class="copy-btn"
            :class="{ copied: copied }"
          >
            <svg v-if="!copied" class="icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
            </svg>
            <svg v-else class="icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
            </svg>
            {{ copied ? t('share.copied') : t('share.copy') }}
          </button>
        </div>
      </div>

      <!-- QR Code -->
      <div class="qr-section">
        <h4>{{ t('share.qrCode') }}</h4>
        <div class="qr-container">
          <div ref="qrContainer" class="qr-code"></div>
          <button @click="downloadQR" class="download-btn">
            {{ t('share.downloadQR') }}
          </button>
        </div>
      </div>

      <!-- Embed Code -->
      <div class="embed-section">
        <h4>{{ t('share.embed') }}</h4>
        <div class="input-group">
          <textarea 
            ref="embedInput"
            :value="embedCode" 
            readonly 
            class="embed-input"
            rows="3"
          ></textarea>
          <button 
            @click="copyEmbedCode" 
            class="copy-btn"
            :class="{ copied: embedCopied }"
          >
            <svg v-if="!embedCopied" class="icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
            </svg>
            {{ embedCopied ? t('share.copied') : t('share.copy') }}
          </button>
        </div>
      </div>

      <!-- Share Analytics -->
      <div class="analytics-section" v-if="showAnalytics">
        <h4>{{ t('share.analytics') }}</h4>
        <div class="analytics-stats">
          <div class="stat">
            <span class="stat-number">{{ analytics.totalShares }}</span>
            <span class="stat-label">{{ t('share.totalShares') }}</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ analytics.totalClicks }}</span>
            <span class="stat-label">{{ t('share.totalClicks') }}</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ analytics.conversionRate }}%</span>
            <span class="stat-label">{{ t('share.conversionRate') }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import QRCode from 'qrcode'

interface Props {
  auctionId: number
  auctionTitle: string
  auctionDescription?: string
  auctionImage?: string
  currentPrice?: number
  showAnalytics?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showAnalytics: false
})

const emit = defineEmits<{
  close: []
  shareTracked: [platform: string, url: string]
}>()

const { t } = useI18n()

const linkInput = ref<HTMLInputElement>()
const embedInput = ref<HTMLTextAreaElement>()
const qrContainer = ref<HTMLElement>()
const copied = ref(false)
const embedCopied = ref(false)
const qrCodeDataUrl = ref('')

const baseUrl = window.location.origin
const shareUrl = computed(() => `${baseUrl}/auction/${props.auctionId}`)
const analytics = ref({
  totalShares: 0,
  totalClicks: 0,
  conversionRate: 0
})

const shareText = computed(() => 
  `Check out this auction: ${props.auctionTitle} - Current price: $${props.currentPrice || '0'}`
)

const embedCode = computed(() => 
  `<iframe src="${baseUrl}/embed/${props.auctionId}" width="400" height="300" frameborder="0"></iframe>`
)

// Generate QR Code
const generateQRCode = async () => {
  try {
    qrCodeDataUrl.value = await QRCode.toDataURL(shareUrl.value, {
      width: 200,
      margin: 2,
      color: {
        dark: '#000000',
        light: '#ffffff'
      }
    })
    
    await nextTick()
    if (qrContainer.value) {
      qrContainer.value.innerHTML = `<img src="${qrCodeDataUrl.value}" alt="QR Code" />`
    }
  } catch (error) {
    console.error('Error generating QR code:', error)
  }
}

// Share functions
const shareOnFacebook = () => {
  const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl.value)}`
  openShareWindow(url, 'facebook')
}

const shareOnTwitter = () => {
  const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText.value)}&url=${encodeURIComponent(shareUrl.value)}`
  openShareWindow(url, 'twitter')
}

const shareOnWhatsApp = () => {
  const url = `https://wa.me/?text=${encodeURIComponent(shareText.value + ' ' + shareUrl.value)}`
  openShareWindow(url, 'whatsapp')
}

const shareViaEmail = () => {
  const subject = encodeURIComponent(`Check out this auction: ${props.auctionTitle}`)
  const body = encodeURIComponent(`I thought you might be interested in this auction:\n\n${props.auctionTitle}\n${shareUrl.value}\n\n${props.auctionDescription || ''}`)
  const url = `mailto:?subject=${subject}&body=${body}`
  window.location.href = url
  trackShare('email')
}

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(shareUrl.value)
    copied.value = true
    setTimeout(() => copied.value = false, 2000)
    trackShare('copy-link')
  } catch (error) {
    // Fallback for older browsers
    if (linkInput.value) {
      linkInput.value.select()
      document.execCommand('copy')
      copied.value = true
      setTimeout(() => copied.value = false, 2000)
      trackShare('copy-link')
    }
  }
}

const copyEmbedCode = async () => {
  try {
    await navigator.clipboard.writeText(embedCode.value)
    embedCopied.value = true
    setTimeout(() => embedCopied.value = false, 2000)
    trackShare('embed')
  } catch (error) {
    // Fallback for older browsers
    if (embedInput.value) {
      embedInput.value.select()
      document.execCommand('copy')
      embedCopied.value = true
      setTimeout(() => embedCopied.value = false, 2000)
      trackShare('embed')
    }
  }
}

const downloadQR = () => {
  if (qrCodeDataUrl.value) {
    const link = document.createElement('a')
    link.download = `auction-${props.auctionId}-qr.png`
    link.href = qrCodeDataUrl.value
    link.click()
    trackShare('qr-download')
  }
}

const openShareWindow = (url: string, platform: string) => {
  const width = 600
  const height = 400
  const left = (window.innerWidth - width) / 2
  const top = (window.innerHeight - height) / 2
  
  window.open(
    url,
    'share',
    `width=${width},height=${height},left=${left},top=${top},resizable,scrollbars`
  )
  
  trackShare(platform)
}

const trackShare = (platform: string) => {
  emit('shareTracked', platform, shareUrl.value)
  
  // Update analytics
  analytics.value.totalShares++
  
  // Send to backend for tracking
  fetch('/api/shares/track', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      auction_id: props.auctionId,
      platform: platform,
      url: shareUrl.value
    })
  }).catch(error => console.error('Error tracking share:', error))
}

const getCookie = (name: string): string => {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) {
    return parts.pop()?.split(';').shift() || ''
  }
  return ''
}

const closeShare = () => {
  emit('close')
}

onMounted(() => {
  generateQRCode()
  
  // Load analytics if enabled
  if (props.showAnalytics) {
    fetch(`/api/shares/analytics/${props.auctionId}`)
      .then(response => response.json())
      .then(data => {
        analytics.value = data
      })
      .catch(error => console.error('Error loading analytics:', error))
  }
})
</script>

<style scoped>
.share-component {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.share-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.share-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.25rem;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: #f3f4f6;
  color: #1f2937;
}

.share-content {
  padding: 1.5rem;
}

.share-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.share-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  color: white;
}

.share-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.share-btn .icon {
  width: 20px;
  height: 20px;
}

.share-btn.facebook {
  background-color: #1877f2;
}

.share-btn.twitter {
  background-color: #1da1f2;
}

.share-btn.whatsapp {
  background-color: #25d366;
}

.share-btn.email {
  background-color: #ea4335;
}

.copy-link-section {
  margin-bottom: 1.5rem;
}

.input-group {
  display: flex;
  gap: 0.5rem;
}

.link-input,
.embed-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-family: monospace;
  font-size: 0.875rem;
  background-color: #f9fafb;
}

.embed-input {
  resize: vertical;
  min-height: 80px;
}

.copy-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  color: #374151;
}

.copy-btn:hover {
  background-color: #f3f4f6;
  border-color: #9ca3af;
}

.copy-btn.copied {
  background-color: #10b981;
  color: white;
  border-color: #10b981;
}

.copy-btn .icon {
  width: 16px;
  height: 16px;
}

.qr-section,
.embed-section,
.analytics-section {
  margin-bottom: 1.5rem;
}

.qr-section h4,
.embed-section h4,
.analytics-section h4 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.qr-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.qr-code {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
}

.qr-code img {
  max-width: 100%;
  height: auto;
}

.download-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  color: #374151;
}

.download-btn:hover {
  background-color: #f3f4f6;
  border-color: #9ca3af;
}

.analytics-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 1rem;
}

.stat {
  text-align: center;
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 0.5rem;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

.stat-label {
  display: block;
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

@media (max-width: 640px) {
  .share-buttons {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .input-group {
    flex-direction: column;
  }
  
  .analytics-stats {
    grid-template-columns: 1fr;
  }
}
</style>
