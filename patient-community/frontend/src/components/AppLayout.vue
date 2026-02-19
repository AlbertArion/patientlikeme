<template>
  <div class="app-layout">
    <header class="top-nav">
      <div class="nav-inner container-wide">
        <router-link to="/" class="logo">
          <span class="logo-text">患者社区</span>
          <span class="logo-tagline">找到和你一样的人</span>
        </router-link>
        <nav class="nav-links">
          <router-link to="/dashboard" :class="{ active: isActive('/dashboard') }">控制台</router-link>
          <router-link to="/records" :class="{ active: isActive('/records') }">我的病历</router-link>
          <router-link to="/similar-patients" :class="{ active: isActive('/similar-patients') }">相似患者</router-link>
          <router-link to="/community" :class="{ active: isActive('/community') }">社区</router-link>
          <router-link to="/solutions" :class="{ active: isActive('/solutions') }">治疗方案</router-link>
        </nav>
        <div class="nav-actions">
          <template v-if="!userStore.isLoggedIn">
            <router-link to="/login" class="btn btn-ghost">登录</router-link>
            <router-link to="/register" class="btn btn-primary">立即加入</router-link>
          </template>
          <template v-else>
            <el-dropdown trigger="click" @command="handleCommand">
              <span class="user-trigger">
                <el-avatar :size="36" class="avatar">{{ userStore.userInfo?.username?.charAt(0) }}</el-avatar>
                <span class="username">{{ userStore.userInfo?.username }}</span>
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                  <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </div>
      </div>
    </header>
    <main class="layout-main">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isActive = (path) => {
  if (path === '/dashboard') return route.path === '/dashboard'
  return route.path.startsWith(path)
}

const handleCommand = (cmd) => {
  if (cmd === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.logout()
      ElMessage.success('已退出登录')
      router.push('/')
    })
  } else if (cmd === 'profile') {
    router.push('/profile')
  }
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  background: #f8fafc;
}

.top-nav {
  background: var(--pc-surface);
  box-shadow: 0 1px 0 rgba(196, 30, 58, 0.06);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  gap: 32px;
}

.logo {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: var(--pc-cool);
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

.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-links a {
  padding: 8px 16px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  color: var(--pc-cool-muted);
  border-radius: 8px;
  transition: color 0.2s, background 0.2s;
}

.nav-links a:hover {
  color: var(--pc-primary);
  background: var(--pc-warm);
}

.nav-links a.active {
  color: var(--pc-primary);
  background: var(--pc-warm);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn {
  padding: 8px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-ghost {
  color: var(--pc-cool);
  border: 1px solid #e2e8f0;
}

.btn-ghost:hover {
  border-color: var(--pc-primary);
  color: var(--pc-primary);
}

.btn-primary {
  background: var(--pc-primary);
  color: white;
  border: none;
}

.btn-primary:hover {
  background: var(--pc-primary-dark);
  color: white;
}

.user-trigger {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s;
}

.user-trigger:hover {
  background: var(--pc-warm);
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: var(--pc-cool);
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.avatar {
  background: linear-gradient(135deg, var(--pc-primary) 0%, var(--pc-primary-dark) 100%);
}

.layout-main {
  padding: 24px 0 48px;
}
</style>
