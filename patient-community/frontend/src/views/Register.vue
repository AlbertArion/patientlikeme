<template>
  <div class="register-page">
    <header class="auth-header">
      <router-link to="/" class="logo">患者社区</router-link>
    </header>
    <div class="register-container">
      <div class="register-card">
        <h2>注册</h2>
        <el-form :model="form" :rules="rules" ref="formRef" label-width="0">
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="用户名"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>
          <el-form-item prop="email">
            <el-input
              v-model="form.email"
              placeholder="邮箱"
              size="large"
              prefix-icon="Message"
            />
          </el-form-item>
          <el-form-item prop="phone">
            <el-input
              v-model="form.phone"
              placeholder="手机号"
              size="large"
              prefix-icon="Phone"
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
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="确认密码"
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
              @click="handleRegister"
            >
              注册
            </el-button>
          </el-form-item>
        </el-form>
        <div class="links">
          <router-link to="/login">已有账号？立即登录</router-link>
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

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在3-20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    
    await authAPI.register({
      username: form.username,
      email: form.email,
      phone: form.phone,
      password: form.password
    })
    
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    if (error.response) {
      ElMessage.error(error.response.data.detail || '注册失败')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
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

.register-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
  flex: 1;
  display: flex;
  align-items: center;
}

.register-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.register-card h2 {
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
