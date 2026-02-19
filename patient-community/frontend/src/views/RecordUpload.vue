<template>
  <AppLayout>
    <div class="record-upload-page">
      <div class="container-wide">
        <section class="page-hero">
          <el-page-header @back="router.back()" class="back-header">
            <template #content>
              <span class="page-title">上传病历</span>
            </template>
          </el-page-header>
          <p class="hero-tagline">上传病历文件，AI 将自动提取疾病、症状与治疗方案等关键信息</p>
        </section>

        <el-card class="upload-card">
          <el-upload
            class="upload-area"
            drag
            :action="uploadAction"
            :headers="uploadHeaders"
            :on-success="handleSuccess"
            :on-error="handleError"
            :before-upload="beforeUpload"
            accept=".jpg,.jpeg,.png,.pdf,.doc,.docx"
          >
            <el-icon class="el-icon--upload" :size="64"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 JPG、PNG、PDF、DOC、DOCX 格式，单文件不超过 10MB
              </div>
            </template>
          </el-upload>

          <div v-if="uploadedRecords.length > 0" class="uploaded-list">
            <h3>已上传的病历</h3>
            <el-table :data="uploadedRecords" style="width: 100%">
              <el-table-column prop="title" label="文件名" />
              <el-table-column prop="file_type" label="类型" width="100" />
              <el-table-column label="状态" width="120">
                <template #default="scope">
                  <el-tag v-if="scope.row.is_processed" type="success">已处理</el-tag>
                  <el-tag v-else type="warning">待处理</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button
                    v-if="!scope.row.is_processed"
                    type="primary"
                    size="small"
                    @click="processRecord(scope.row.id)"
                    :loading="processing[scope.row.id]"
                  >
                    AI 提取
                  </el-button>
                  <el-button size="small" @click="viewRecord(scope.row.id)">查看</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { recordsAPI } from '@/api/records'
import AppLayout from '@/components/AppLayout.vue'

const router = useRouter()
const userStore = useUserStore()

const uploadAction = computed(() => '/api/records/upload')
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${userStore.token}`
}))

const uploadedRecords = ref([])
const processing = reactive({})

const beforeUpload = (file) => {
  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) ElMessage.error('文件大小不能超过 10MB')
  return isLt10M
}

const handleSuccess = (response) => {
  ElMessage.success('上传成功')
  uploadedRecords.value.unshift(response)
}

const handleError = () => {
  ElMessage.error('上传失败')
}

const processRecord = async (recordId) => {
  processing[recordId] = true
  try {
    const result = await recordsAPI.process(recordId)
    ElMessage.success('AI 提取完成')
    const index = uploadedRecords.value.findIndex(r => r.id === recordId)
    if (index !== -1) uploadedRecords.value[index] = result
  } catch (error) {
    ElMessage.error('AI 提取失败')
  } finally {
    processing[recordId] = false
  }
}

const viewRecord = () => router.push('/records')

const loadRecords = async () => {
  try {
    const records = await recordsAPI.getList()
    uploadedRecords.value = records.slice(0, 5)
  } catch (error) {
    console.error('加载病历失败', error)
  }
}

loadRecords()
</script>

<style scoped>
.record-upload-page {
  min-height: 60vh;
}

.page-hero {
  margin-bottom: 24px;
}

.back-header {
  margin-bottom: 8px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--pc-cool);
}

.hero-tagline {
  font-size: 15px;
  color: var(--pc-cool-muted);
}

.upload-card {
  max-width: 720px;
  border-radius: var(--pc-radius-lg);
  box-shadow: var(--pc-shadow);
}

.upload-area {
  margin-bottom: 24px;
}

:deep(.el-upload-dragger) {
  padding: 48px 24px;
  border-radius: var(--pc-radius);
  border: 2px dashed var(--pc-border);
  background: var(--pc-warm-bg);
}

:deep(.el-upload-dragger:hover) {
  border-color: var(--pc-primary);
  background: var(--pc-warm);
}

.el-upload__tip {
  color: var(--pc-cool-muted);
  font-size: 13px;
}

.uploaded-list {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f1f5f9;
}

.uploaded-list h3 {
  margin-bottom: 16px;
  font-size: 16px;
  font-weight: 600;
  color: var(--pc-cool);
}
</style>
