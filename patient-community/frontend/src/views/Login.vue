<template>
  <div class="login-page">
    <header class="auth-header">
      <router-link to="/" class="logo">
        <span class="logo-text">患者社区</span>
        <span class="logo-tagline">找到和你一样的人</span>
      </router-link>
    </header>

    <div class="auth-body">
      <aside class="auth-brand">
        <div class="brand-inner">
          <h1>欢迎回来</h1>
          <p class="tagline">找到和你一样的人</p>
          <p class="desc">登录后即可管理病历、查看相似病友、参与社区讨论，在理解与支持中更好地前行。</p>
          <ul class="feature-list">
            <li>病历管理 · AI 智能提取</li>
            <li>相似患者 · 方案推荐</li>
            <li>社区交流 · 经验分享</li>
          </ul>
        </div>
      </aside>

      <main class="auth-form-wrap">
        <div class="login-card">
          <h2>登录</h2>
          <p class="card-hint">使用用户名、邮箱或手机号登录</p>
          <el-form :model="form" :rules="rules" ref="formRef" label-width="0" class="form">
            <el-form-item prop="username">
              <el-input
                v-model="form.username"
                placeholder="用户名 / 邮箱 / 手机号"
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
                class="submit-btn"
                :loading="loading"
                @click="handleLogin"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>
          <div class="links">
            还没有账号？
            <router-link to="/register">立即注册</router-link>
          </div>
        </div>
      </main>
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
  background: linear-gradient(160deg, #fef2f2 0%, #fff5f5 45%, #f8fafc 100%);
}

.auth-header {
  flex-shrink: 0;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(196, 30, 58, 0.08);
  background: rgba(255, 255, 255, 0.8);
}

.auth-header .logo {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: var(--pc-primary);
  letter-spacing: -0.02em;
}

.logo-tagline {
  font-size: 11px;
  color: var(--pc-cool-muted);
  margin-top: 2px;
}

.auth-body {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: calc(100vh - 64px);
}

@media (max-width: 900px) {
  .auth-body {
    grid-template-columns: 1fr;
  }
  .auth-brand {
    padding: 32px 24px 24px;
  }
}

.auth-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
}

.brand-inner {
  max-width: 380px;
}

.auth-brand h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--pc-cool);
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.auth-brand .tagline {
  font-size: 18px;
  font-weight: 500;
  color: var(--pc-primary);
  margin: 0 0 20px 0;
}

.auth-brand .desc {
  font-size: 15px;
  color: var(--pc-cool-muted);
  line-height: 1.6;
  margin: 0 0 24px 0;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 14px;
  color: var(--pc-cool-muted);
  line-height: 2;
}

.feature-list li::before {
  content: "·";
  color: var(--pc-primary);
  font-weight: bold;
  margin-right: 8px;
}

.auth-form-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 24px;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: var(--pc-radius-lg);
  padding: 40px 44px;
  box-shadow: 0 4px 24px rgba(196, 30, 58, 0.08);
  border: 1px solid rgba(196, 30, 58, 0.06);
}

.login-card h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--pc-cool);
  text-align: center;
}

.card-hint {
  margin: 0 0 28px 0;
  font-size: 14px;
  color: var(--pc-cool-muted);
  text-align: center;
}

.form :deep(.el-form-item) {
  margin-bottom: 18px;
}

.submit-btn {
  width: 100%;
  margin-top: 8px;
}

.links {
  text-align: center;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #f1f5f9;
  font-size: 14px;
  color: var(--pc-cool-muted);
}

.links a {
  color: var(--pc-primary);
  text-decoration: none;
  font-weight: 500;
}

.links a:hover {
  text-decoration: underline;
}
</style>
