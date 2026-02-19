<template>
  <AppLayout>
    <div class="solutions-page">
      <div class="container-wide">
        <section class="page-hero">
          <h1>治疗方案</h1>
          <p class="hero-tagline">向他人学习，找到适合你的治疗方案</p>
          <div class="hero-search">
            <el-input
              v-model="searchKeyword"
              placeholder="输入疾病或治疗方案名称搜索"
              size="large"
              clearable
              class="search-input"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </section>

        <div class="solutions-grid">
          <div
            v-for="solution in filteredSolutions"
            :key="solution.id"
            class="solution-card"
          >
            <div class="solution-header">
              <h3>{{ solution.title }}</h3>
              <el-tag type="danger" size="small" effect="plain">{{ solution.disease_name }}</el-tag>
            </div>
            <p class="solution-description">{{ solution.description }}</p>
            <div class="solution-stats">
              <div class="stat-item">
                <span class="stat-label">成功率</span>
                <span class="stat-value success">{{ solution.success_rate }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">使用人数</span>
                <span class="stat-value">{{ solution.user_count }}</span>
              </div>
            </div>
            <div class="effectiveness-bar">
              <span class="bar-label">社区反馈</span>
              <div class="bar-track">
                <div class="bar-fill" :style="{ width: solution.success_rate }"></div>
              </div>
              <span class="bar-legend">高</span>
            </div>
            <div class="solution-actions">
              <el-button type="primary" size="small">查看详情</el-button>
              <el-button size="small" plain>我也在用</el-button>
            </div>
          </div>
        </div>

        <el-empty v-if="filteredSolutions.length === 0" description="暂无相关治疗方案" />
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import AppLayout from '@/components/AppLayout.vue'

const searchKeyword = ref('')

const solutions = ref([
  {
    id: 1,
    disease_name: '糖尿病',
    title: '综合管理方案',
    description: '包括饮食控制、运动疗法和药物治疗的综合方案，通过科学的血糖管理和生活方式调整，有效控制糖尿病进展。',
    success_rate: '85%',
    user_count: 150
  },
  {
    id: 2,
    disease_name: '高血压',
    title: '降压治疗方案',
    description: '通过药物和生活方式调整控制血压，包括合理用药、低盐饮食、适量运动等综合措施。',
    success_rate: '90%',
    user_count: 200
  },
  {
    id: 3,
    disease_name: '慢性肾病',
    title: '肾功能保护方案',
    description: '延缓肾功能衰退的综合治疗方案，包括药物治疗、饮食管理和定期监测。',
    success_rate: '75%',
    user_count: 80
  },
  {
    id: 4,
    disease_name: '冠心病',
    title: '心血管康复方案',
    description: '通过药物治疗、运动康复和心理干预，改善心血管功能，预防心血管事件。',
    success_rate: '82%',
    user_count: 120
  },
  {
    id: 5,
    disease_name: '类风湿关节炎',
    title: '关节保护方案',
    description: '综合运用药物治疗、物理治疗和功能锻炼，减轻关节炎症，保护关节功能。',
    success_rate: '78%',
    user_count: 95
  },
  {
    id: 6,
    disease_name: '哮喘',
    title: '呼吸管理方案',
    description: '通过规范化的药物治疗和环境控制，有效控制哮喘症状，提高生活质量。',
    success_rate: '88%',
    user_count: 160
  }
])

const filteredSolutions = computed(() => {
  if (!searchKeyword.value) return solutions.value
  const keyword = searchKeyword.value.toLowerCase()
  return solutions.value.filter(
    s =>
      s.disease_name.toLowerCase().includes(keyword) ||
      s.title.toLowerCase().includes(keyword) ||
      s.description.toLowerCase().includes(keyword)
  )
})
</script>

<style scoped>
.solutions-page {
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
  color: var(--pc-cool-muted);
  margin-bottom: 24px;
}

.hero-search {
  max-width: 440px;
}

.search-input {
  border-radius: 10px;
}

.solutions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.solution-card {
  background: white;
  border-radius: var(--pc-radius-lg);
  padding: 24px;
  border: 1px solid #f1f5f9;
  box-shadow: var(--pc-shadow);
  transition: all 0.3s;
}

.solution-card:hover {
  border-color: var(--pc-border);
  box-shadow: 0 8px 28px rgba(196, 30, 58, 0.1);
}

.solution-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.solution-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--pc-cool);
  flex: 1;
}

.solution-description {
  font-size: 14px;
  color: var(--pc-cool-muted);
  line-height: 1.6;
  margin-bottom: 20px;
}

.solution-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--pc-cool-muted);
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--pc-cool);
}

.stat-value.success {
  color: var(--pc-primary);
}

.effectiveness-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.bar-label {
  font-size: 13px;
  color: var(--pc-cool-muted);
  width: 64px;
  flex-shrink: 0;
}

.bar-track {
  flex: 1;
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--pc-primary) 0%, var(--pc-primary-light) 100%);
  border-radius: 4px;
  transition: width 0.3s;
}

.bar-legend {
  font-size: 11px;
  color: var(--pc-cool-muted);
  width: 16px;
}

.solution-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  padding-top: 8px;
  border-top: 1px solid #f1f5f9;
}
</style>
