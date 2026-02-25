<template>
  <AppLayout>
    <div class="solution-create-page">
      <div class="container-wide">
        <div class="create-card">
          <div class="create-back">
            <router-link to="/solutions" class="back-link">
              <el-icon><ArrowLeft /></el-icon>
              <span>返回治疗方案</span>
            </router-link>
          </div>
          <h1>新建治疗方案</h1>
          <p class="create-tip">提交后将进入审核，通过后会在方案列表中展示。</p>
          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-width="100px"
            class="create-form"
          >
            <el-form-item label="方案名称" prop="title">
              <el-input
                v-model="form.title"
                placeholder="如：综合管理方案、降压治疗方案"
                maxlength="200"
                show-word-limit
              />
            </el-form-item>
            <el-form-item label="疾病类型" prop="disease_name">
              <el-input
                v-model="form.disease_name"
                placeholder="如：糖尿病、高血压、慢性肾病"
                maxlength="100"
                show-word-limit
              />
            </el-form-item>
            <el-form-item label="方案描述" prop="description">
              <el-input
                v-model="form.description"
                type="textarea"
                :rows="5"
                placeholder="请详细描述该治疗方案的内容、适用人群与注意事项等"
                maxlength="2000"
                show-word-limit
              />
            </el-form-item>
            <el-form-item label="感知有效性" prop="success_rate">
              <el-input
                v-model="form.success_rate"
                placeholder="如：85%（选填）"
                maxlength="20"
              />
            </el-form-item>
            <el-form-item label="使用人数" prop="user_count">
              <el-input-number
                v-model="form.user_count"
                :min="0"
                placeholder="选填，默认 0"
                style="width: 160px"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="submitting" @click="onSubmit">提交审核</el-button>
              <router-link to="/solutions" style="margin-left: 12px">
                <el-button>取消</el-button>
              </router-link>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import AppLayout from '@/components/AppLayout.vue'
import { solutionsAPI } from '@/api/solutions'

const router = useRouter()
const formRef = ref(null)
const submitting = ref(false)
const form = reactive({
  title: '',
  disease_name: '',
  description: '',
  success_rate: '',
  user_count: 0
})

const rules = {
  title: [{ required: true, message: '请输入方案名称', trigger: 'blur' }],
  disease_name: [{ required: true, message: '请输入疾病类型', trigger: 'blur' }]
}

async function onSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    await solutionsAPI.create({
      title: form.title.trim(),
      disease_name: form.disease_name.trim(),
      description: form.description?.trim() || '',
      success_rate: form.success_rate?.trim() || null,
      user_count: form.user_count ?? 0
    })
    ElMessage.success('已提交，等待审核通过后即可在列表中展示')
    router.push('/solutions')
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '提交失败')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.solution-create-page {
  min-height: 60vh;
  padding: 24px 0 48px;
}

.create-card {
  background: white;
  border-radius: var(--pc-radius-lg);
  padding: 32px;
  border: 1px solid #f1f5f9;
  box-shadow: var(--pc-shadow);
  max-width: 640px;
}

.create-back {
  margin-bottom: 20px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--pc-cool-muted);
  text-decoration: none;
}

.back-link:hover {
  color: var(--pc-primary);
}

.create-card h1 {
  margin: 0 0 8px;
  font-size: 24px;
  font-weight: 700;
  color: var(--pc-cool);
}

.create-tip {
  margin: 0 0 24px;
  font-size: 14px;
  color: var(--pc-cool-muted);
}

.create-form {
  margin-top: 8px;
}
</style>
