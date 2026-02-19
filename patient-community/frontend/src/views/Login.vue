<template>
  <div class="login-page">
    <header class="auth-header">
      <router-link to="/" class="logo">患者社区</router-link>
    </header>
    <div class="login-container">
      <div class="login-card">
        <h2>登录</h2>
        <el-form :model="form" :rules="rules" ref="formRef" label-width="0">
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="用户名/手机号/邮箱"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="密码"
              size="large"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              style="width: 100%"
              :loading="loading"
              @click="handleLogin"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
        <div class="links">
          <router-link to="/register">还没有账号？立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authAPI } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    
    const response = await authAPI.login(form)
    
    userStore.setToken(response.access_token)
    userStore.setUserInfo(response.user)
    
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (error) {
    if (error.response) {
      ElMessage.error(error.response.data.detail || '登录失败')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 40px;
  background: linear-gradient(160deg, #fef2f2 0%, #fff5f5 50%, #f8fafc 100%);
}

.auth-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-header .logo {
  font-size: 22px;
  font-weight: 700;
  color: var(--pc-primary);
  text-decoration: none;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
  flex: 1;
  display: flex;
  align-items: center;
}

.login-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.login-card h2 {
  text-align: center;
  margin-bottom: 30px;
  color: var(--pc-cool);
  font-size: 28px;
}

.links {
  text-align: center;
  margin-top: 20px;
}

.links a {
  color: var(--pc-primary);
  text-decoration: none;
}

.links a:hover {
  text-decoration: underline;
}
</style>
