<template>
  <div class="forgot-page">
    <header class="auth-header">
      <div class="auth-header-inner container-wide">
        <router-link to="/" class="logo">
          <img src="/favicon.png" alt="患者社区" class="logo-img" />
          <div class="logo-text-wrap">
            <span class="logo-text">患者社区</span>
            <span class="logo-tagline">找到和你一样的人</span>
          </div>
        </router-link>
        <button class="nav-menu-btn" aria-label="菜单" @click="authMenuOpen = true">
          <el-icon :size="24"><Operation /></el-icon>
        </button>
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
        <router-link to="/" @click="authMenuOpen = false">首页</router-link>
        <router-link to="/login" @click="authMenuOpen = false">登录</router-link>
        <router-link to="/register" @click="authMenuOpen = false">立即加入</router-link>
      </nav>
    </el-drawer>

    <div class="auth-body">
      <aside class="auth-brand">
        <div class="brand-inner">
          <h1>重置密码</h1>
          <p class="tagline">找回您的账号</p>
          <p class="desc">请输入注册时使用的手机号或邮箱，获取验证码后设置新密码。</p>
          <ul class="feature-list">
            <li>支持手机号 / 邮箱找回</li>
            <li>验证码 10 分钟内有效</li>
            <li>新密码至少 6 位</li>
          </ul>
        </div>
      </aside>

      <main class="auth-form-wrap">
        <div class="forgot-card">
          <h2>忘记密码</h2>
          <p class="card-hint">填写手机号或邮箱获取验证码</p>

          <!-- 步骤1：获取验证码 -->
          <el-form v-if="step === 1" :model="requestForm" :rules="requestRules" ref="requestFormRef" label-width="0" class="form">
            <el-form-item prop="account">
              <el-input
                v-model="requestForm.account"
                placeholder="手机号或邮箱"
                size="large"
                prefix-icon="Message"
              />
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                size="large"
                class="submit-btn"
                :loading="requesting"
                @click="handleRequestCode"
              >
                获取验证码
              </el-button>
            </el-form-item>
          </el-form>

          <!-- 步骤2：输入验证码和新密码 -->
          <el-form v-else :model="resetForm" :rules="resetRules" ref="resetFormRef" label-width="0" class="form">
            <el-form-item>
              <el-input v-model="accountDisplay" disabled size="large" />
            </el-form-item>
            <el-form-item prop="code">
              <el-input
                v-model="resetForm.code"
                placeholder="请输入验证码"
                size="large"
                maxlength="6"
                show-word-limit
              />
            </el-form-item>
            <el-form-item prop="newPassword">
              <el-input
                v-model="resetForm.newPassword"
                type="password"
                placeholder="新密码（至少6位）"
                size="large"
                prefix-icon="Lock"
                show-password
              />
            </el-form-item>
            <el-form-item prop="confirmPassword">
              <el-input
                v-model="resetForm.confirmPassword"
                type="password"
                placeholder="确认新密码"
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
                :loading="resetting"
                @click="handleReset"
              >
                重置密码
              </el-button>
            </el-form-item>
          </el-form>

          <div class="links">
            <router-link to="/login">返回登录</router-link>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authAPI } from '@/api/auth'

const router = useRouter()
const authMenuOpen = ref(false)
const step = ref(1)
const requesting = ref(false)
const resetting = ref(false)
const requestFormRef = ref(null)
const resetFormRef = ref(null)

const requestForm = reactive({
  account: ''
})

const requestRules = {
  account: [
    { required: true, message: '请输入手机号或邮箱', trigger: 'blur' }
  ]
}

const resetForm = reactive({
  code: '',
  newPassword: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== resetForm.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const resetRules = {
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位数字', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const accountType = ref('phone') // 'phone' | 'email'
const accountValue = ref('')

const accountDisplay = computed(() => {
  if (accountType.value === 'phone') return `手机号：${accountValue.value}`
  return `邮箱：${accountValue.value}`
})

const isPhone = (s) => /^1\d{10}$/.test(s)
const isEmail = (s) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s)

const handleRequestCode = async () => {
  try {
    await requestFormRef.value.validate()
    const account = requestForm.account.trim()
    if (isPhone(account)) {
      accountType.value = 'phone'
      accountValue.value = account
    } else if (isEmail(account)) {
      accountType.value = 'email'
      accountValue.value = account
    } else {
      ElMessage.warning('请输入正确的手机号或邮箱')
      return
    }

    requesting.value = true
    const res = await authAPI.forgotPasswordRequest(
      accountType.value === 'phone' ? { phone: account } : { email: account }
    )
    if (res.data?.code) {
      ElMessage.success(`验证码已发送：${res.data.code}（演示环境，生产环境将通过短信/邮件发送）`)
    } else {
      ElMessage.success(res.data?.message || '验证码已发送')
    }
    step.value = 2
    resetForm.code = ''
    resetForm.newPassword = ''
    resetForm.confirmPassword = ''
  } catch (error) {
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    }
  } finally {
    requesting.value = false
  }
}

const handleReset = async () => {
  try {
    await resetFormRef.value.validate()
    resetting.value = true
    const payload = {
      code: resetForm.code,
      new_password: resetForm.newPassword
    }
    if (accountType.value === 'phone') {
      payload.phone = accountValue.value
    } else {
      payload.email = accountValue.value
    }
    await authAPI.forgotPasswordReset(payload)
    ElMessage.success('密码重置成功，请使用新密码登录')
    router.push('/login')
  } catch (error) {
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    }
  } finally {
    resetting.value = false
  }
}
</script>

<style scoped>
.forgot-page {
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
  justify-content: space-between;
  padding: 0 24px;
  background: var(--pc-surface);
  box-shadow: 0 1px 0 rgba(196, 30, 58, 0.06);
  position: sticky;
  top: 0;
  z-index: 100;
}

.auth-header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.auth-header .logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.auth-header .logo-img {
  height: 42px;
  width: 42px;
  object-fit: contain;
}

.logo-text-wrap {
  display: flex;
  flex-direction: column;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: var(--pc-primary);
}

.logo-tagline {
  font-size: 11px;
  color: var(--pc-cool-muted);
}

.nav-menu-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  padding: 0;
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

.auth-body {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: calc(100vh - 64px);
  align-items: center;
}

@media (max-width: 900px) {
  .auth-body {
    grid-template-columns: 1fr;
  }
}

.auth-brand {
  padding: 48px;
}

.brand-inner h1 {
  font-size: 32px;
  font-weight: 700;
  color: var(--pc-cool);
  margin-bottom: 12px;
}

.tagline {
  font-size: 18px;
  color: var(--pc-primary);
  margin-bottom: 16px;
}

.desc {
  font-size: 16px;
  color: var(--pc-cool-muted);
  line-height: 1.6;
  margin-bottom: 24px;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  padding: 8px 0;
  color: var(--pc-cool-muted);
  font-size: 15px;
  position: relative;
  padding-left: 20px;
}

.feature-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--pc-primary);
  font-weight: bold;
}

.auth-form-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
}

.forgot-card {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}

.forgot-card h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--pc-cool);
  margin-bottom: 8px;
}

.card-hint {
  font-size: 14px;
  color: var(--pc-cool-muted);
  margin-bottom: 28px;
}

.submit-btn {
  width: 100%;
}

.links {
  margin-top: 24px;
  text-align: center;
}

.links a {
  color: var(--pc-primary);
  text-decoration: none;
  font-size: 14px;
}

.links a:hover {
  text-decoration: underline;
}

.drawer-nav a {
  padding: 14px 24px;
  font-size: 16px;
  color: var(--pc-cool);
  text-decoration: none;
}

.drawer-nav a:hover {
  background: var(--pc-warm);
  color: var(--pc-primary);
}

.auth-nav-drawer :deep(.el-drawer__body) {
  padding: 0;
}
</style>
