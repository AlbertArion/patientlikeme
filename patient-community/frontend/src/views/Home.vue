<template>
  <div class="home">
    <header class="hero">
      <div class="hero-bg">
        <div class="hero-pattern"></div>
        <div class="hero-gradient"></div>
      </div>
      <div class="container-wide">
        <nav class="navbar">
          <router-link to="/" class="logo">
            <img src="/favicon.png" alt="患者社区" class="logo-img" />
            <div class="logo-text-wrap">
              <span class="logo-text">患者社区</span>
              <span class="logo-tagline">找到和你一样的人</span>
            </div>
          </router-link>
          <div class="nav-links">
            <router-link to="/community">社区</router-link>
            <router-link to="/solutions">治疗方案</router-link>
            <router-link to="/login" v-if="!userStore.isLoggedIn">登录</router-link>
            <router-link to="/dashboard" v-else>控制台</router-link>
            <router-link to="/register" v-if="!userStore.isLoggedIn" class="btn-join">立即加入</router-link>
          </div>
          <button class="nav-menu-btn" aria-label="菜单" @click="homeMenuOpen = true">
            <el-icon :size="24"><Operation /></el-icon>
          </button>
        </nav>
        <el-drawer
          v-model="homeMenuOpen"
          direction="rtl"
          size="280px"
          :with-header="false"
          class="home-nav-drawer"
        >
          <nav class="drawer-nav">
            <router-link to="/" @click="homeMenuOpen = false" :class="{ active: route.path === '/' }">首页</router-link>
            <router-link to="/dashboard" @click="homeMenuOpen = false">控制台</router-link>
            <router-link to="/records" @click="homeMenuOpen = false">我的病历</router-link>
            <router-link to="/similar-patients" @click="homeMenuOpen = false">相似患者</router-link>
            <router-link to="/community" @click="homeMenuOpen = false">社区</router-link>
            <router-link to="/solutions" @click="homeMenuOpen = false">治疗方案</router-link>
          </nav>
          <div v-if="!userStore.isLoggedIn" class="drawer-actions">
            <router-link to="/login" class="drawer-btn drawer-btn-ghost" @click="homeMenuOpen = false">登录</router-link>
            <router-link to="/register" class="drawer-btn drawer-btn-primary" @click="homeMenuOpen = false">立即加入</router-link>
          </div>
        </el-drawer>

        <div class="hero-content">
          <div class="hero-text">
            <h1>找到你的社区<br />找到你的力量</h1>
            <p class="subtitle">
              与超过数千名病友一起，用真实经历与健康洞察，在理解与支持中更好地生活。
            </p>
            <div class="cta-buttons">
              <button class="btn btn-primary" @click="handleJoin">立即加入</button>
              <button class="btn btn-outline" @click="handleLearnMore">了解更多</button>
            </div>
          </div>
          <div class="hero-visual">
            <div class="hex-network">
              <div class="hex hex-1"></div>
              <div class="hex hex-2"></div>
              <div class="hex hex-3"></div>
              <div class="hex hex-4"></div>
              <div class="hex hex-5"></div>
              <div class="hex hex-6"></div>
              <div class="hex hex-center"></div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <section class="section features">
      <div class="container-wide">
        <h2 class="section-title">为什么选择患者社区</h2>
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon"><el-icon :size="40"><Upload /></el-icon></div>
            <h3>病历管理</h3>
            <p>便捷上传病历，AI 智能提取关键信息，一目了然</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon"><el-icon :size="40"><User /></el-icon></div>
            <h3>相似患者</h3>
            <p>根据病历匹配相似病友与治疗方案，少走弯路</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon"><el-icon :size="40"><ChatDotRound /></el-icon></div>
            <h3>社区交流</h3>
            <p>加入疾病社区，分享经验、获得支持与共鸣</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon"><el-icon :size="40"><Collection /></el-icon></div>
            <h3>治疗方案库</h3>
            <p>查看真实效果反馈与感知有效性，辅助决策</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section steps-section">
      <div class="container-wide">
        <h2 class="section-title">如何开始</h2>
        <div class="steps">
          <div class="step">
            <div class="step-num">1</div>
            <h3>注册账号</h3>
            <p>快速注册，创建个人健康档案</p>
          </div>
          <div class="step">
            <div class="step-num">2</div>
            <h3>上传病历</h3>
            <p>上传病历文件，AI 自动提取关键信息</p>
          </div>
          <div class="step">
            <div class="step-num">3</div>
            <h3>找到相似患者</h3>
            <p>系统为您匹配相似病情的病友与方案</p>
          </div>
          <div class="step">
            <div class="step-num">4</div>
            <h3>参与社区</h3>
            <p>加入讨论、分享经验、获得支持</p>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="container-wide">
        <p>&copy; 2026 患者社区 · 基于真实经历，与你同行</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const homeMenuOpen = ref(false)

const handleJoin = () => {
  if (userStore.isLoggedIn) router.push('/dashboard')
  else router.push('/register')
}

const handleLearnMore = () => router.push('/community')
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.hero {
  position: relative;
  padding: 0 0 100px;
  overflow: hidden;
}

@media (max-width: 768px) {
  .hero {
    padding: 0 0 48px;
  }
}

.hero-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #fef2f2 0%, #fff5f5 50%, #fef2f2 100%);
}

.hero-pattern {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle at 20% 80%, rgba(196, 30, 58, 0.06) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(196, 30, 58, 0.04) 0%, transparent 50%);
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(255, 255, 255, 0.8) 100%);
}

.navbar {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0 40px;
}

@media (max-width: 768px) {
  .navbar {
    padding: 12px 0 24px;
  }
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.logo-img {
  height: 42px;
  width: 42px;
  object-fit: contain;
  flex-shrink: 0;
}

.logo-text-wrap {
  display: flex;
  flex-direction: column;
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  color: var(--pc-primary);
  letter-spacing: -0.02em;
}

.logo-tagline {
  display: block;
  font-size: 11px;
  color: var(--pc-cool-muted);
  margin-top: 2px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
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
  .nav-links {
    display: none !important;
  }
  .nav-menu-btn {
    display: flex;
  }
}

@media (max-width: 480px) {
  .logo-tagline {
    display: none;
  }
}

.nav-links a {
  color: var(--pc-cool);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  transition: color 0.2s, background 0.2s;
}

.nav-links a:hover {
  color: var(--pc-primary);
  background: var(--pc-warm);
}

.btn-join {
  background: var(--pc-primary) !important;
  color: white !important;
}

.btn-join:hover {
  background: var(--pc-primary-dark) !important;
  color: white !important;
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

.home-nav-drawer :deep(.el-drawer__body) {
  padding: 0;
  overflow: auto;
}

.hero-content {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  padding: 20px 0 60px;
}

@media (max-width: 900px) {
  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 16px 0 40px;
  }
  .hero-visual {
    order: -1;
  }
  .subtitle {
    margin-left: auto;
    margin-right: auto;
  }
  .cta-buttons {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .hero-text h1 {
    font-size: 28px;
    margin-bottom: 16px;
  }
  .subtitle {
    font-size: 15px;
    margin-bottom: 24px;
  }
  .cta-buttons {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
  }
  .cta-buttons .btn {
    width: auto;
    min-width: 120px;
    max-width: 160px;
    padding: 12px 20px;
    font-size: 15px;
  }
  .hex-network {
    width: 200px;
    height: 200px;
  }
  .hex {
    width: 40px;
    height: 40px;
  }
  .hex-center {
    width: 52px;
    height: 52px;
  }
  .hex-1 { left: 0; top: 18%; }
  .hex-2 { right: 5%; top: 0; }
  .hex-3 { right: 0; top: 42%; }
  .hex-4 { right: 5%; bottom: 5%; }
  .hex-5 { left: 10%; bottom: 0; }
  .hex-6 { left: 0; top: 48%; }
}

@media (max-width: 480px) {
  .hero-text h1 {
    font-size: 24px;
  }
  .subtitle {
    font-size: 14px;
  }
}

.hero-text h1 {
  font-size: 42px;
  font-weight: 800;
  line-height: 1.2;
  color: var(--pc-cool);
  letter-spacing: -0.03em;
  margin-bottom: 20px;
}

.subtitle {
  font-size: 18px;
  color: var(--pc-cool-muted);
  line-height: 1.6;
  margin-bottom: 32px;
  max-width: 480px;
}

.cta-buttons {
  display: flex;
  gap: 16px;
}

.btn {
  padding: 14px 28px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: var(--pc-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--pc-primary-dark);
  transform: translateY(-1px);
}

.btn-outline {
  background: transparent;
  color: var(--pc-primary);
  border: 2px solid var(--pc-primary);
}

.btn-outline:hover {
  background: var(--pc-warm);
}

.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.hex-network {
  position: relative;
  width: 280px;
  height: 280px;
}

.hex {
  position: absolute;
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid rgba(196, 30, 58, 0.2);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(196, 30, 58, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
}

.hex-center {
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, var(--pc-primary) 0%, var(--pc-primary-dark) 100%);
  border: none;
  box-shadow: 0 8px 24px rgba(196, 30, 58, 0.25);
}

.hex-1 { left: 0; top: 20%; }
.hex-2 { right: 10%; top: 0; }
.hex-3 { right: 0; top: 45%; }
.hex-4 { right: 10%; bottom: 10%; }
.hex-5 { left: 15%; bottom: 0; }
.hex-6 { left: 0; top: 50%; }

.section {
  padding: 80px 0;
}

@media (max-width: 768px) {
  .section {
    padding: 40px 0;
  }
}

.section-title {
  text-align: center;
  font-size: 32px;
  font-weight: 700;
  color: var(--pc-cool);
  margin-bottom: 48px;
  letter-spacing: -0.02em;
}

@media (max-width: 768px) {
  .section-title {
    font-size: 24px;
    margin-bottom: 28px;
  }
}

.features {
  background: white;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

@media (max-width: 1000px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 560px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
}

.feature-card {
  text-align: center;
  padding: 32px 24px;
  border-radius: var(--pc-radius-lg);
  background: #fafafa;
  border: 1px solid #f1f5f9;
  transition: all 0.3s;
}

@media (max-width: 768px) {
  .feature-card {
    padding: 24px 16px;
  }
  .feature-icon {
    width: 56px;
    height: 56px;
    margin-bottom: 16px;
  }
  .feature-card h3 {
    font-size: 16px;
  }
  .feature-card p {
    font-size: 13px;
  }
}

.feature-card:hover {
  background: var(--pc-warm-bg);
  border-color: var(--pc-border);
  box-shadow: var(--pc-shadow);
  transform: translateY(-4px);
}

.feature-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, var(--pc-primary) 0%, var(--pc-primary-dark) 100%);
  color: white;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--pc-cool);
  margin-bottom: 10px;
}

.feature-card p {
  font-size: 14px;
  color: var(--pc-cool-muted);
  line-height: 1.6;
}

.steps-section {
  background: #f8fafc;
}

.steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
}

@media (max-width: 900px) {
  .steps {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 500px) {
  .steps {
    grid-template-columns: 1fr;
  }
}

.step {
  text-align: center;
}

.step-num {
  width: 56px;
  height: 56px;
  margin: 0 auto 20px;
  background: var(--pc-primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
}

.step h3 {
  font-size: 17px;
  font-weight: 600;
  color: var(--pc-cool);
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .steps {
    gap: 24px;
  }
  .step-num {
    width: 48px;
    height: 48px;
    font-size: 18px;
  }
  .step h3 {
    font-size: 16px;
  }
}

.step p {
  font-size: 14px;
  color: var(--pc-cool-muted);
  line-height: 1.5;
}

.footer {
  background: var(--pc-cool);
  color: rgba(255, 255, 255, 0.8);
  padding: 24px 0;
  text-align: center;
  font-size: 14px;
}

@media (max-width: 480px) {
  .footer {
    padding: 20px 16px;
    font-size: 13px;
  }
}
</style>
