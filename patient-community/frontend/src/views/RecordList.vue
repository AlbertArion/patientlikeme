<template>
  <AppLayout>
    <div class="records-page">
      <div class="container-wide">
        <section class="page-hero">
          <h1>我的病历</h1>
          <p class="hero-tagline">在统一入口管理你的病历，AI 帮你提炼关键信息</p>
          <div class="hero-actions">
            <el-button type="primary" size="large" @click="router.push('/records/upload')">
              <el-icon><Upload /></el-icon>
              上传病历
            </el-button>
          </div>
        </section>

        <el-card v-if="records.length === 0" class="empty-card">
          <el-empty description="暂无病历，请先上传">
            <el-button type="primary" @click="router.push('/records/upload')">去上传</el-button>
          </el-empty>
        </el-card>

        <div v-else class="records-grid">
          <div v-for="record in records" :key="record.id" class="record-card">
            <div class="record-header">
              <h3>{{ record.title }}</h3>
              <el-tag v-if="record.is_processed" type="success" size="small">已处理</el-tag>
              <el-tag v-else type="warning" size="small">待处理</el-tag>
            </div>
            <div class="record-meta">
              <span>上传时间：{{ formatDate(record.upload_time) }}</span>
              <span>类型：{{ record.file_type }}</span>
            </div>
            <div v-if="record.medical_info" class="medical-info">
              <div class="info-row">
                <span class="label">疾病名称</span>
                <span>{{ record.medical_info.disease_name || '未识别' }}</span>
              </div>
              <div class="info-row">
                <span class="label">症状</span>
                <span>{{ record.medical_info.symptoms || '无' }}</span>
              </div>
              <div class="info-row">
                <span class="label">治疗方案</span>
                <span>{{ record.medical_info.treatment_plan || '无' }}</span>
              </div>
            </div>
            <div class="record-actions">
              <el-button
                v-if="!record.is_processed"
                type="primary"
                size="small"
                @click="processRecord(record.id)"
                :loading="processing[record.id]"
              >
                AI 提取
              </el-button>
              <el-button type="danger" size="small" plain @click="deleteRecord(record.id)">
                删除
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { recordsAPI } from '@/api/records'
import AppLayout from '@/components/AppLayout.vue'

const router = useRouter()
const records = ref([])
const processing = reactive({})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const loadRecords = async () => {
  try {
    records.value = await recordsAPI.getList()
  } catch (error) {
    ElMessage.error('加载病历失败')
  }
}

const processRecord = async (recordId) => {
  processing[recordId] = true
  try {
    const result = await recordsAPI.process(recordId)
    ElMessage.success('AI 提取完成')
    const index = records.value.findIndex(r => r.id === recordId)
    if (index !== -1) records.value[index] = result
  } catch (error) {
    ElMessage.error('AI 提取失败')
  } finally {
    processing[recordId] = false
  }
}

const deleteRecord = async (recordId) => {
  try {
    await ElMessageBox.confirm('确定要删除这条病历吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await recordsAPI.delete(recordId)
    ElMessage.success('删除成功')
    records.value = records.value.filter(r => r.id !== recordId)
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('删除失败')
  }
}

loadRecords()
</script>

<style scoped>
.records-page {
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
  margin-bottom: 20px;
}

.hero-actions {
  display: flex;
  gap: 12px;
}

.empty-card {
  border-radius: var(--pc-radius-lg);
  box-shadow: var(--pc-shadow);
}

.records-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 24px;
}

.record-card {
  background: white;
  border-radius: var(--pc-radius-lg);
  padding: 24px;
  border: 1px solid #f1f5f9;
  box-shadow: var(--pc-shadow);
  transition: all 0.3s;
}

.record-card:hover {
  border-color: var(--pc-border);
  box-shadow: 0 8px 28px rgba(196, 30, 58, 0.1);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.record-header h3 {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: var(--pc-cool);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: 12px;
}

.record-meta {
  font-size: 13px;
  color: var(--pc-cool-muted);
  margin-bottom: 16px;
}

.record-meta span {
  margin-right: 16px;
}

.medical-info {
  padding: 16px 0;
  border-top: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 16px;
}

.info-row {
  display: flex;
  margin-bottom: 8px;
  font-size: 14px;
}

.info-row .label {
  color: var(--pc-cool-muted);
  width: 80px;
  flex-shrink: 0;
}

.record-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}
</style>
