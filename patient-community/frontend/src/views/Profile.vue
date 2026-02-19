<template>
  <AppLayout>
    <div class="profile-page">
      <div class="container-wide">
        <section class="page-hero">
          <h1>个人信息</h1>
          <p class="hero-tagline">管理你的账号信息，保持联系方式准确以便获得社区支持</p>
        </section>

        <el-card class="profile-card" v-loading="loading">
          <div class="profile-header">
            <el-avatar :size="80" class="avatar">
              {{ form.username?.charAt(0) || '?' }}
            </el-avatar>
            <div class="profile-title">
              <h2>{{ form.username }}</h2>
              <span class="join-time" v-if="form.created_at">
                加入于 {{ formatDate(form.created_at) }}
              </span>
            </div>
          </div>

          <el-divider />

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-width="100px"
            class="profile-form"
          >
            <el-form-item label="用户名">
              <el-input v-model="form.username" disabled>
                <template #suffix>
                  <el-tag size="small" type="info">不可修改</el-tag>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input
                v-model="form.email"
                placeholder="请输入邮箱"
                clearable
              >
                <template #prefix>
                  <el-icon><Message /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input
                v-model="form.phone"
                placeholder="请输入手机号"
                clearable
              >
                <template #prefix>
                  <el-icon><Phone /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="saving" @click="handleSubmit">
                保存修改
              </el-button>
              <el-button @click="loadProfile">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { authAPI } from '@/api/auth'
import { useUserStore } from '@/stores/user'
import AppLayout from '@/components/AppLayout.vue'

const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(true)
const saving = ref(false)

const form = reactive({
  username: '',
  email: '',
  phone: '',
  created_at: null
})

const rules = {
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$|^$/, message: '请输入正确的手机号或留空', trigger: 'blur' }
  ]
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

const loadProfile = async () => {
  loading.value = true
  try {
    const data = await authAPI.getProfile()
    form.username = data.username ?? ''
    form.email = data.email ?? ''
    form.phone = data.phone ?? ''
    form.created_at = data.created_at ?? null
    userStore.setUserInfo(data)
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '获取个人信息失败')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    saving.value = true
    const data = await authAPI.updateProfile({
      email: form.email || null,
      phone: form.phone || null
    })
    userStore.setUserInfo(data)
    ElMessage.success('保存成功')
  } catch (error) {
    if (error?.message) return
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-page {
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

.profile-card {
  max-width: 560px;
  border-radius: var(--pc-radius-lg);
  box-shadow: var(--pc-shadow);
  border: 1px solid #f1f5f9;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
}

.avatar {
  background: linear-gradient(135deg, var(--pc-primary) 0%, var(--pc-primary-dark) 100%);
  color: white;
  font-size: 32px;
  font-weight: 600;
}

.profile-title h2 {
  margin: 0 0 8px 0;
  font-size: 22px;
  font-weight: 600;
  color: var(--pc-cool);
}

.join-time {
  font-size: 13px;
  color: var(--pc-cool-muted);
}

.profile-form {
  margin-top: 8px;
}
</style>
