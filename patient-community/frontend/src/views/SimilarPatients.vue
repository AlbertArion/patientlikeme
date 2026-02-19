<template>
  <AppLayout>
    <div class="similar-page">
      <div class="container-wide">
        <section class="page-hero">
          <h1>相似患者</h1>
          <p class="hero-tagline">基于病历信息，发现与你有相似经历的病友，互相支持、少走弯路</p>
        </section>

        <el-alert
          v-if="!hasRecords"
          title="请先上传并处理病历"
          type="info"
          description="上传病历并完成「AI 提取」后，系统将为您匹配相似患者与推荐方案。"
          show-icon
          :closable="false"
          class="tip-alert"
        />

        <el-card v-else-if="loading" class="loading-card">
          <el-skeleton :rows="5" animated />
        </el-card>

        <el-card v-else-if="patients.length === 0" class="empty-card">
          <el-empty description="暂未找到相似患者">
            <el-button type="primary" @click="$router.push('/records/upload')">去上传病历</el-button>
          </el-empty>
        </el-card>

        <template v-else>
          <div class="section-title-row">
            <h2>为你匹配的病友</h2>
          </div>
          <div class="patients-grid">
          <div v-for="patient in patients" :key="patient.user_id" class="patient-card">
            <div class="patient-header">
              <el-avatar :size="56" class="avatar">{{ patient.username?.charAt(0) }}</el-avatar>
              <div class="patient-info">
                <h3>{{ patient.username }}</h3>
                <span class="similarity-badge">相似度 {{ patient.similarity }}%</span>
              </div>
            </div>
            <div class="disease-info">
              <el-icon><Document /></el-icon>
              <span>疾病：{{ patient.disease_name || '未识别' }}</span>
            </div>
            <div class="patient-actions">
              <el-button type="primary" size="small">
                <el-icon><ChatDotRound /></el-icon>
                发起交流
              </el-button>
              <el-button size="small" plain>查看详情</el-button>
            </div>
          </div>
        </div>
        </template>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { matchAPI } from '@/api/match'
import { recordsAPI } from '@/api/records'
import AppLayout from '@/components/AppLayout.vue'

const patients = ref([])
const loading = ref(true)
const hasRecords = ref(true)

const loadSimilarPatients = async () => {
  try {
    loading.value = true
    const records = await recordsAPI.getList()
    const processedRecords = records.filter(r => r.is_processed)
    if (processedRecords.length === 0) {
      hasRecords.value = false
      loading.value = false
      return
    }
    const result = await matchAPI.getSimilarPatients()
    patients.value = result
  } catch (error) {
    ElMessage.error('加载相似患者失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadSimilarPatients()
})
</script>

<style scoped>
.similar-page {
  min-height: 60vh;
}

.page-hero {
  margin-bottom: 32px;
}

.page-hero h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--pc-cool);
  margin-bottom: 8px;
}

.hero-tagline {
  font-size: 15px;
  color: var(--pc-cool-muted);
}

.tip-alert {
  border-radius: var(--pc-radius);
}

.loading-card,
.empty-card {
  border-radius: var(--pc-radius-lg);
  box-shadow: var(--pc-shadow);
}

.section-title-row {
  margin-bottom: 24px;
}

.section-title-row h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--pc-cool);
}

.patients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.patient-card {
  background: white;
  border-radius: var(--pc-radius-lg);
  padding: 24px;
  border: 1px solid #f1f5f9;
  box-shadow: var(--pc-shadow);
  transition: all 0.3s;
}

.patient-card:hover {
  border-color: var(--pc-border);
  box-shadow: 0 8px 28px rgba(196, 30, 58, 0.1);
}

.patient-header {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 16px;
}

.avatar {
  background: linear-gradient(135deg, var(--pc-primary) 0%, var(--pc-primary-dark) 100%);
}

.patient-info h3 {
  margin: 0 0 6px 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--pc-cool);
}

.similarity-badge {
  display: inline-block;
  font-size: 13px;
  color: var(--pc-primary);
  font-weight: 500;
}

.disease-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 0;
  border-top: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 16px;
  font-size: 14px;
  color: var(--pc-cool-muted);
}

.patient-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}
</style>
