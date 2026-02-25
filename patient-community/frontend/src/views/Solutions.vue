<template>
  <AppLayout>
    <div class="solutions-page">
      <div class="container-wide">
        <section class="page-hero">
          <div class="hero-head">
            <div>
              <h1>治疗方案</h1>
              <p class="hero-tagline">向他人学习，找到适合你的治疗方案</p>
            </div>
            <router-link v-if="userStore.isLoggedIn" to="/solutions/create" class="btn-new">
              <el-button type="primary">新建方案</el-button>
            </router-link>
          </div>
          <div class="filter-search-row">
            <span class="filter-label">筛选符合以下条件的患者：</span>
            <el-select
              v-model="filterDisease"
              placeholder="选择疾病"
              clearable
              filterable
              size="large"
              class="filter-select"
              @change="onFilterChange"
            >
              <el-option label="全部" value="" />
              <el-option
                v-for="d in diseaseOptions"
                :key="d"
                :label="d"
                :value="d"
              />
            </el-select>
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

        <el-skeleton v-if="loading" :rows="6" animated />
        <el-empty v-else-if="displaySolutions.length === 0" description="暂无相关治疗方案" />
        <div v-else class="solutions-content">
          <div
            v-for="(items, category) in groupedByCategory"
            :key="category"
            class="category-section"
          >
            <h3 class="category-title">{{ category }}</h3>
            <div class="solutions-grid">
              <div
                v-for="solution in items"
                :key="solution.id"
                class="solution-card"
              >
                <div class="solution-header">
              <h3>{{ solution.title }}</h3>
              <el-tag type="danger" size="small" effect="plain">{{ solution.disease_name }}</el-tag>
            </div>
            <p class="solution-description">{{ solution.description || '暂无详细描述' }}</p>
            <div class="solution-stats">
              <div class="stat-item">
                <span class="stat-label">感知有效性</span>
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
                <div class="bar-fill" :style="{ width: solution.success_rate || '0%' }"></div>
              </div>
              <span class="bar-legend">高</span>
            </div>
            <div class="solution-actions">
              <el-button type="primary" size="small" @click="goToDetail(solution.id)">查看详情</el-button>
              <el-button
                size="small"
                :type="solutionsStore.isUsing(solution.id) ? 'success' : undefined"
                :plain="!solutionsStore.isUsing(solution.id)"
                :disabled="solutionsStore.isUsing(solution.id)"
                @click="handleUseThis(solution)"
              >
                {{ solutionsStore.isUsing(solution.id) ? '已在用' : '我也在用' }}
              </el-button>
                </div>
              </div>
            </div>
          </div>
          <p v-if="lastUpdated" class="last-updated">最后更新时间：{{ lastUpdated }}</p>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import AppLayout from '@/components/AppLayout.vue'
import { useSolutionsStore } from '@/stores/solutions'
import { useUserStore } from '@/stores/user'
import { solutionsAPI } from '@/api/solutions'

const DISEASE_OPTIONS = ['糖尿病', '高血压', '慢性肾病', '冠心病', '类风湿关节炎', '哮喘']

const router = useRouter()
const solutionsStore = useSolutionsStore()
const userStore = useUserStore()
const searchKeyword = ref('')
const filterDisease = ref('')
const solutions = ref([])
const loading = ref(true)

const diseaseOptions = computed(() => {
  const fromData = [...new Set(solutions.value.map(s => s.disease_name))]
  return [...new Set([...DISEASE_OPTIONS, ...fromData])]
})

onMounted(async () => {
  const conds = userStore.userInfo?.interested_conditions
  if (Array.isArray(conds) && conds.length > 0) {
    filterDisease.value = conds[0]
  }
  await loadSolutions()
})

async function loadSolutions() {
  loading.value = true
  try {
    const params = filterDisease.value ? { disease: filterDisease.value } : {}
    const list = await solutionsAPI.getList(params)
    solutions.value = list || []
  } catch {
    solutions.value = []
  } finally {
    loading.value = false
  }
}

function onFilterChange() {
  loadSolutions()
}

const filteredSolutions = computed(() => {
  let list = solutions.value
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    list = list.filter(
      s =>
        (s.disease_name && s.disease_name.toLowerCase().includes(keyword)) ||
        (s.title && s.title.toLowerCase().includes(keyword)) ||
        (s.description && s.description.toLowerCase().includes(keyword))
    )
  }
  return list
})

const groupedByCategory = computed(() => {
  const groups = {}
  for (const s of filteredSolutions.value) {
    const cat = s.category || '综合方案'
    if (!groups[cat]) groups[cat] = []
    groups[cat].push(s)
  }
  return groups
})

const displaySolutions = computed(() => filteredSolutions.value)

const lastUpdated = computed(() => {
  const dates = solutions.value
    .map(s => s.updated_at || s.created_at)
    .filter(Boolean)
  if (dates.length === 0) return ''
  const max = new Date(Math.max(...dates.map(d => new Date(d))))
  return max.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
})

function goToDetail(id) {
  router.push({ name: 'SolutionDetail', params: { id } })
}

function handleUseThis(solution) {
  ElMessageBox.confirm(
    `确认标记为「我也在用」「${solution.title}」？`,
    '确认',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'info'
    }
  )
    .then(() => {
      solutionsStore.addUsing(solution.id)
      ElMessage.success('已记录，你正在使用该方案')
    })
    .catch(() => {})
}
</script>

<style scoped>
.solutions-page {
  min-height: 60vh;
}

.page-hero {
  margin-bottom: 40px;
}

.hero-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;
}

.hero-head .btn-new {
  flex-shrink: 0;
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

.filter-search-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: nowrap;
}

.filter-label {
  font-size: 14px;
  color: var(--pc-cool-muted);
  white-space: nowrap;
  flex-shrink: 0;
}

.filter-select {
  width: 220px;
  flex-shrink: 0;
}

.filter-select :deep(.el-select__wrapper) {
  min-width: 0;
}

.search-input {
  flex: 1;
  min-width: 0;
  border-radius: 10px;
}

.search-input :deep(.el-input__wrapper) {
  min-width: 0;
}

.category-section {
  margin-bottom: 40px;
}

.category-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--pc-cool);
  margin: 0 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #e2e8f0;
}

.last-updated {
  font-size: 13px;
  color: var(--pc-cool-muted);
  margin-top: 24px;
}

.solutions-grid {
  display: grid;
  gap: 24px;
  margin-bottom: 32px;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
}

@media (min-width: 900px) {
  .solutions-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 600px) {
  .solutions-grid {
    grid-template-columns: 1fr;
  }
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
  min-height: 3.2em;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
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
