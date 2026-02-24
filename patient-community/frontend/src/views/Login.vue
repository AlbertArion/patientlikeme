<template>
  <div class="login-page">
    <header class="auth-header">
      <div class="auth-header-inner container-wide">
        <router-link to="/" class="logo">
          <img src="/favicon.png" alt="患者社区" class="logo-img" />
          <div class="logo-text-wrap">
            <span class="logo-text">患者社区</span>
            <span class="logo-tagline">找到和你一样的人</span>
          </div>
        </router-link>
        <nav class="nav-links">
          <router-link to="/dashboard" :class="{ active: isActive('/dashboard') }">控制台</router-link>
          <router-link to="/records" :class="{ active: isActive('/records') }">我的病历</router-link>
          <router-link to="/similar-patients" :class="{ active: isActive('/similar-patients') }">相似患者</router-link>
          <router-link to="/community" :class="{ active: isActive('/community') }">社区</router-link>
          <router-link to="/solutions" :class="{ active: isActive('/solutions') }">治疗方案</router-link>
        </nav>
        <button class="nav-menu-btn" aria-label="菜单" @click="authMenuOpen = true">
          <el-icon :size="24"><Operation /></el-icon>
        </button>
        <div class="nav-actions">
          <router-link to="/login" class="btn btn-ghost">登录</router-link>
          <router-link :to="{ path: '/register', query: $route.query }" class="btn btn-primary">立即加入</router-link>
        </div>
      </div>
    </header>
    <el-drawer
      v-model="authMenuOpen"
      direction="rtl"
      size="280px"
      :with-header="false"
      class="auth-nav-drawer"
    >
      <nav class="drawer-nav">
        <router-link to="/" @click="authMenuOpen = false" :class="{ active: isActive('/') }">首页</router-link>
        <router-link to="/dashboard" @click="authMenuOpen = false" :class="{ active: isActive('/dashboard') }">控制台</router-link>
        <router-link to="/records" @click="authMenuOpen = false" :class="{ active: isActive('/records') }">我的病历</router-link>
        <router-link to="/similar-patients" @click="authMenuOpen = false" :class="{ active: isActive('/similar-patients') }">相似患者</router-link>
        <router-link to="/community" @click="authMenuOpen = false" :class="{ active: isActive('/community') }">社区</router-link>
        <router-link to="/solutions" @click="authMenuOpen = false" :class="{ active: isActive('/solutions') }">治疗方案</router-link>
      </nav>
      <div v-if="!userStore.isLoggedIn" class="drawer-actions">
        <router-link to="/login" class="drawer-btn drawer-btn-ghost" @click="authMenuOpen = false">登录</router-link>
        <router-link to="/register" class="drawer-btn drawer-btn-primary" @click="authMenuOpen = false">立即加入</router-link>
      </div>
    </el-drawer>

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
            <router-link :to="{ path: '/forgot-password', query: $route.query }">忘记密码？</router-link>
            <span class="links-sep">|</span>
            还没有账号？
            <router-link :to="{ path: '/register', query: $route.query }">立即注册</router-link>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authAPI } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 菜单选中：当前路径或 redirect 参数匹配时高亮
const isActive = (path) => {
  if (path === '/login') return route.path === '/login'
  const target = route.query.redirect || route.path
  if (path === '/') return target === '/'
  if (path === '/dashboard') return target === '/dashboard'
  return target.startsWith(path)
}
const formRef = ref(null)
const loading = ref(false)
const authMenuOpen = ref(false)

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
    router.push(route.query.redirect || '/dashboard')
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
  background: var(--pc-surface);
  box-shadow: 0 1px 0 rgba(196, 30, 58, 0.06);
  position: sticky;
  top: 0;
  z-index: 100;
}

.auth-header .logo {
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.auth-header .logo-img {
  height: 42px;
  width: 42px;
  object-fit: contain;
  flex-shrink: 0;
}

.auth-header .logo-text-wrap {
  display: flex;
  flex-direction: column;
}

.auth-header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  gap: 32px;
  width: 100%;
}

.auth-header .nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.auth-header .nav-links a {
  padding: 8px 16px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  color: var(--pc-cool-muted);
  border-radius: 8px;
  transition: color 0.2s, background 0.2s;
}

.auth-header .nav-links a:hover {
  color: var(--pc-primary);
  background: var(--pc-warm);
}

.auth-header .nav-links a.active {
  color: var(--pc-primary);
  background: var(--pc-warm);
}

.auth-header .nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.auth-header .nav-actions .btn {
  padding: 8px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.auth-header .nav-actions .btn-ghost {
  color: var(--pc-cool);
  border: 1px solid #e2e8f0;
}

.auth-header .nav-actions .btn-ghost:hover {
  border-color: var(--pc-primary);
  color: var(--pc-primary);
}

.auth-header .nav-actions .btn-primary {
  background: var(--pc-primary);
  color: white;
  border: none;
}

.auth-header .nav-actions .btn-primary:hover {
  background: var(--pc-primary-dark);
  color: white;
}

@media (max-width: 900px) {
  .auth-header .nav-links {
    display: none !important;
  }
  .auth-header .nav-actions .btn-ghost,
  .auth-header .nav-actions .btn-primary {
    display: none;
  }
}

.nav-menu-btn {
  display: none;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  padding: 0;
  padding-left: 0;
  padding-right: 0;
  margin-left: auto;
  margin-right: 8px;
  border: none;
  background: transparent;
  color: var(--pc-cool);
  border-radius: 8px;
  cursor: pointer;
}

.nav-menu-btn:hover {
  background: var(--pc-warm);
  color: var(--pc-primary);
}

@media (max-width: 900px) {
  .nav-menu-btn {
    display: flex;
  }
}

.drawer-nav {
  display: flex;
  flex-direction: column;
  padding: 24px 0;
}

.drawer-nav a {
  padding: 14px 24px;
  font-size: 16px;
  color: var(--pc-cool);
  text-decoration: none;
  border-left: 3px solid transparent;
}

.drawer-nav a:hover,
.drawer-nav a.active {
  background: var(--pc-warm);
  color: var(--pc-primary);
  border-left-color: var(--pc-primary);
}

.drawer-actions {
  padding: 16px 24px;
  border-top: 1px solid var(--pc-warm);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.drawer-btn {
  display: block;
  text-align: center;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.drawer-btn-ghost {
  color: var(--pc-cool);
  border: 1px solid #e2e8f0;
}

.drawer-btn-ghost:hover {
  border-color: var(--pc-primary);
  color: var(--pc-primary);
}

.drawer-btn-primary {
  background: var(--pc-primary);
  color: white;
  border: none;
}

.drawer-btn-primary:hover {
  background: var(--pc-primary-dark);
  color: white;
}

.auth-nav-drawer :deep(.el-drawer__body) {
  padding: 0;
  overflow: auto;
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

.links-sep {
  margin: 0 10px;
  color: #cbd5e1;
}
</style>
