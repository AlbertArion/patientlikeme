<template>
  <AppLayout>
    <div class="solution-detail-page">
      <div class="container-wide">
        <div v-if="solution" class="detail-layout">
          <div class="detail-card">
            <div class="detail-back">
              <router-link to="/solutions" class="back-link">
                <el-icon><ArrowLeft /></el-icon>
                <span>返回治疗方案</span>
              </router-link>
            </div>
            <div class="detail-header">
              <h1>{{ solution.title }}</h1>
              <el-tag type="danger" size="large" effect="plain">{{ solution.disease_name }}</el-tag>
            </div>
            <p class="detail-description">{{ solution.description || '暂无详细描述' }}</p>
            <div class="detail-stats">
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
            <div class="detail-actions">
              <el-button
                type="primary"
                size="large"
                :type="solutionsStore.isUsing(solution.id) ? 'success' : 'primary'"
                :disabled="solutionsStore.isUsing(solution.id)"
                @click="handleUseThis"
              >
                {{ solutionsStore.isUsing(solution.id) ? '已在用' : '我也在用' }}
              </el-button>
            </div>
          </div>

          <section v-if="diseaseIntro" class="disease-intro-card">
            <h3 class="section-title">相关疾病简介</h3>
            <p class="disease-intro-text">{{ diseaseIntro }}</p>
          </section>

          <section v-if="groupedMethods && Object.keys(groupedMethods).length" class="treatment-methods-card">
            <h3 class="section-title">治疗手段分类</h3>
            <p class="section-desc">点击查看该方案下按类别整理的治疗方式及社区使用人数</p>
            <div
              v-for="(items, category) in groupedMethods"
              :key="category"
              class="method-category"
            >
              <h4 class="method-category-title">{{ category }}</h4>
              <div class="method-list">
                <div
                  v-for="(m, idx) in items"
                  :key="idx"
                  class="method-row"
                >
                  <span class="method-name">{{ m.name }}</span>
                  <span class="method-count">{{ m.patient_count }} 患者</span>
                </div>
              </div>
            </div>
          </section>
        </div>
        <div v-else class="not-found">
          <el-empty description="未找到该治疗方案">
            <router-link to="/solutions">
              <el-button type="primary">返回列表</el-button>
            </router-link>
          </el-empty>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import AppLayout from '@/components/AppLayout.vue'
import { useSolutionsStore } from '@/stores/solutions'
import { solutionsAPI } from '@/api/solutions'

const DISEASE_INTROS = {
  糖尿病: '糖尿病是一种以高血糖为特征的代谢性疾病，需通过饮食、运动、药物等综合管理控制血糖，预防并发症。',
  高血压: '高血压是常见慢性病，需长期规范用药与生活方式干预，以降低心脑血管风险。',
  慢性肾病: '慢性肾病进展可导致肾功能减退，早期干预与规范治疗有助于延缓进展、保护残余肾功能。',
  冠心病: '冠心病由冠状动脉狭窄或闭塞引起，需药物、介入或手术及心脏康复等综合治疗。',
  类风湿关节炎: '类风湿关节炎为慢性自身免疫性疾病，需药物与康复锻炼结合以控制炎症、保护关节功能。',
  哮喘: '哮喘是慢性气道炎症性疾病，需规范用药与避免诱因，以控制症状、减少急性发作。'
}

const route = useRoute()
const solutionsStore = useSolutionsStore()
const solution = ref(null)

const diseaseIntro = computed(() => {
  const name = solution.value?.disease_name
  return name ? DISEASE_INTROS[name] || '' : ''
})

const groupedMethods = computed(() => {
  const list = solution.value?.treatment_methods
  if (!list || !Array.isArray(list) || list.length === 0) return null
  const groups = {}
  for (const m of list) {
    const cat = m.category || '其他'
    if (!groups[cat]) groups[cat] = []
    groups[cat].push(m)
  }
  return groups
})

async function fetchDetail() {
  const id = route.params.id
  if (!id) {
    solution.value = null
    return
  }
  try {
    solution.value = await solutionsAPI.getDetail(id)
  } catch {
    solution.value = null
  }
}

onMounted(fetchDetail)
watch(() => route.params.id, fetchDetail)

function handleUseThis() {
  if (solution.value && solutionsStore.isUsing(solution.value.id)) return
  ElMessageBox.confirm('确认标记为「我也在用」该方案？', '确认', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'info'
  })
    .then(() => {
      if (solution.value) solutionsStore.addUsing(solution.value.id)
      ElMessage.success('已记录，你正在使用该方案')
    })
    .catch(() => {})
}
</script>

<style scoped>
.solution-detail-page {
  min-height: 60vh;
  padding: 24px 0 48px;
}

.detail-back {
  margin-bottom: 20px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--pc-cool-muted);
  text-decoration: none;
  transition: color 0.2s;
}

.back-link:hover {
  color: var(--pc-primary);
}

.detail-card {
  background: white;
  border-radius: var(--pc-radius-lg);
  padding: 32px;
  border: 1px solid #f1f5f9;
  box-shadow: var(--pc-shadow);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.detail-header h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: var(--pc-cool);
  letter-spacing: -0.02em;
  flex: 1;
}

.detail-description {
  font-size: 16px;
  color: var(--pc-cool-muted);
  line-height: 1.7;
  margin-bottom: 28px;
}

.detail-stats {
  display: flex;
  gap: 32px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-label {
  font-size: 13px;
  color: var(--pc-cool-muted);
}

.stat-value {
  font-size: 24px;
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
  margin-bottom: 28px;
}

.bar-label {
  font-size: 14px;
  color: var(--pc-cool-muted);
  width: 72px;
  flex-shrink: 0;
}

.bar-track {
  flex: 1;
  max-width: 320px;
  height: 10px;
  background: #f1f5f9;
  border-radius: 5px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--pc-primary) 0%, var(--pc-primary-light) 100%);
  border-radius: 5px;
  transition: width 0.3s;
}

.bar-legend {
  font-size: 12px;
  color: var(--pc-cool-muted);
}

.detail-actions {
  padding-top: 20px;
  border-top: 1px solid #f1f5f9;
}

.detail-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.disease-intro-card,
.treatment-methods-card {
  background: white;
  border-radius: var(--pc-radius-lg);
  padding: 24px 32px;
  border: 1px solid #f1f5f9;
  box-shadow: var(--pc-shadow);
}

.section-title {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--pc-cool);
}

.section-desc {
  font-size: 14px;
  color: var(--pc-cool-muted);
  margin-bottom: 20px;
  line-height: 1.5;
}

.disease-intro-text {
  font-size: 15px;
  color: var(--pc-cool-muted);
  line-height: 1.7;
  margin: 0;
}

.method-category {
  margin-bottom: 24px;
}

.method-category:last-child {
  margin-bottom: 0;
}

.method-category-title {
  margin: 0 0 12px 0;
  font-size: 15px;
  font-weight: 600;
  color: var(--pc-cool);
  padding-bottom: 8px;
  border-bottom: 1px solid #e2e8f0;
}

.method-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.method-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 8px;
  font-size: 14px;
}

.method-name {
  color: var(--pc-cool);
  font-weight: 500;
}

.method-count {
  color: var(--pc-cool-muted);
  font-size: 13px;
}

.not-found {
  padding: 48px 0;
}
</style>
