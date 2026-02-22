<template>
  <AppLayout>
    <div class="dashboard-page">
      <div class="container-wide">
        <section class="page-hero">
          <h1>我的健康</h1>
          <p class="hero-tagline">用好你的健康洞察，在理解与支持中更好地前行</p>
          <p class="hero-desc">
            在统一入口管理病历、查看相似患者与社区动态，让决策更清晰、行动更有据。
          </p>
        </section>

        <section class="stats-row">
          <div class="stat-card" @click="router.push('/records')">
            <div class="stat-icon stat-icon-records">
              <el-icon :size="28"><Document /></el-icon>
            </div>
            <div class="stat-body">
              <div class="stat-value">{{ stats.recordCount }}</div>
              <div class="stat-label">病历数量</div>
            </div>
          </div>
          <div class="stat-card" @click="router.push('/similar-patients')">
            <div class="stat-icon stat-icon-similar">
              <el-icon :size="28"><User /></el-icon>
            </div>
            <div class="stat-body">
              <div class="stat-value">{{ stats.similarCount }}</div>
              <div class="stat-label">相似患者</div>
            </div>
          </div>
          <div class="stat-card" @click="router.push('/community')">
            <div class="stat-icon stat-icon-posts">
              <el-icon :size="28"><ChatDotRound /></el-icon>
            </div>
            <div class="stat-body">
              <div class="stat-value">{{ stats.postCount }}</div>
              <div class="stat-label">我的帖子</div>
            </div>
          </div>
        </section>

        <section class="content-grid">
          <div class="card-block quick-actions-block">
            <h2 class="block-title">快速操作</h2>
            <div class="quick-actions">
              <button class="action-btn primary" @click="router.push('/records/upload')">
                <el-icon><Upload /></el-icon>
                <span>上传病历</span>
              </button>
              <button class="action-btn" @click="router.push('/similar-patients')">
                <el-icon><Search /></el-icon>
                <span>查找相似患者</span>
              </button>
              <button class="action-btn" @click="router.push('/community')">
                <el-icon><ChatDotRound /></el-icon>
                <span>发布帖子</span>
              </button>
            </div>
          </div>
          <div class="card-block activities-block">
            <h2 class="block-title">最近活动</h2>
            <el-empty v-if="activities.length === 0" description="暂无活动记录" />
            <div v-else class="activities">
              <div v-for="activity in activities" :key="activity.id" class="activity-item">
                <div class="activity-content">{{ activity.content }}</div>
                <div class="activity-time">{{ activity.time }}</div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import AppLayout from '@/components/AppLayout.vue'

const router = useRouter()
const userStore = useUserStore()

const stats = reactive({
  recordCount: 0,
  similarCount: 0,
  postCount: 0
})

const activities = ref([])

onMounted(async () => {
  // 可在此从 API 拉取统计与活动
})
</script>

<style scoped>
.dashboard-page {
  min-height: 60vh;
}

.page-hero {
  margin-bottom: 40px;
}

.page-hero h1 {
  font-size: 32px;
  font-weight: 700;
  color: var(--pc-cool);
  margin-bottom: 12px;
  letter-spacing: -0.02em;
}

.hero-tagline {
  font-size: 16px;
  font-weight: 500;
  color: var(--pc-primary);
  margin-bottom: 8px;
}

.hero-desc {
  font-size: 15px;
  color: var(--pc-cool-muted);
  line-height: 1.6;
  max-width: 560px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  background: white;
  border-radius: var(--pc-radius-lg);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: var(--pc-shadow);
  border: 1px solid #f1f5f9;
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  border-color: var(--pc-border);
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(196, 30, 58, 0.12);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon-records {
  background: linear-gradient(135deg, var(--pc-primary) 0%, var(--pc-primary-dark) 100%);
}

.stat-icon-similar {
  background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
}

.stat-icon-posts {
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--pc-cool);
}

.stat-label {
  font-size: 14px;
  color: var(--pc-cool-muted);
  margin-top: 4px;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

@media (max-width: 900px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

.card-block {
  background: white;
  border-radius: var(--pc-radius-lg);
  padding: 24px;
  box-shadow: var(--pc-shadow);
  border: 1px solid #f1f5f9;
}

.block-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--pc-cool);
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--pc-warm);
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: white;
  font-size: 15px;
  color: var(--pc-cool);
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.action-btn:hover {
  border-color: var(--pc-primary);
  background: var(--pc-warm);
  color: var(--pc-primary);
}

.action-btn.primary {
  background: var(--pc-primary);
  border-color: var(--pc-primary);
  color: white;
}

.action-btn.primary:hover {
  background: var(--pc-primary-dark);
  border-color: var(--pc-primary-dark);
  color: white;
}

.activities {
  max-height: 280px;
  overflow-y: auto;
}

.activity-item {
  padding: 14px 0;
  border-bottom: 1px solid #f1f5f9;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-content {
  color: var(--pc-cool);
  font-size: 14px;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: var(--pc-cool-muted);
}
</style>
