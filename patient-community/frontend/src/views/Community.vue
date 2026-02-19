<template>
  <AppLayout>
    <div class="community-page">
      <div class="container-wide">
        <section class="page-hero">
          <h1>找到你的社区</h1>
          <p class="hero-tagline">
            在理解、支持与真实交流中管理健康。参与讨论、提出问题、从同路人那里获得启发。
          </p>
          <div class="hero-search">
            <el-input
              v-model="searchKeyword"
              placeholder="输入关键词搜索社区"
              size="large"
              clearable
              class="search-input"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </section>

        <div class="layout-with-sidebar">
          <aside class="communities-sidebar">
            <div class="sidebar-card">
              <h3>疾病社区</h3>
              <div class="community-list">
                <button
                  v-for="community in communities"
                  :key="community.id"
                  class="community-item"
                  :class="{ active: selectedCommunity === community.id }"
                  @click="selectCommunity(community.id)"
                >
                  <span class="name">{{ community.name }}</span>
                  <span class="count">{{ community.member_count }} 成员</span>
                </button>
              </div>
            </div>
          </aside>

          <main class="posts-main">
            <div class="posts-header">
              <h2>社区帖子</h2>
              <el-button type="primary" @click="showPostDialog = true">
                <el-icon><EditPen /></el-icon>
                发布帖子
              </el-button>
            </div>

            <el-card class="posts-card">
              <el-empty v-if="posts.length === 0" description="暂无帖子，来发第一条吧" />

              <div v-else class="posts-list">
                <article v-for="post in posts" :key="post.id" class="post-item">
                  <h3 class="post-title">{{ post.title }}</h3>
                  <p class="post-content">{{ post.content }}</p>
                  <div class="post-meta">
                    <span><el-icon><User /></el-icon> 用户{{ post.user_id }}</span>
                    <span><el-icon><ChatDotRound /></el-icon> {{ post.comments_count }} 评论</span>
                    <span><el-icon><Star /></el-icon> {{ post.likes_count }} 点赞</span>
                  </div>
                  <div class="post-actions">
                    <el-button size="small" @click="likePost(post.id)">点赞</el-button>
                    <el-button size="small">评论</el-button>
                  </div>
                </article>
              </div>
            </el-card>
          </main>
        </div>
      </div>

      <el-dialog v-model="showPostDialog" title="发布帖子" width="560px" class="post-dialog">
        <el-form :model="postForm" label-width="80px">
          <el-form-item label="标题">
            <el-input v-model="postForm.title" placeholder="请输入帖子标题" />
          </el-form-item>
          <el-form-item label="内容">
            <el-input
              v-model="postForm.content"
              type="textarea"
              :rows="6"
              placeholder="分享你的经历或想法…"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="showPostDialog = false">取消</el-button>
          <el-button type="primary" @click="submitPost" :loading="submitting">发布</el-button>
        </template>
      </el-dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { communityAPI } from '@/api/community'
import AppLayout from '@/components/AppLayout.vue'

const communities = ref([])
const selectedCommunity = ref(null)
const posts = ref([])
const showPostDialog = ref(false)
const submitting = ref(false)
const searchKeyword = ref('')

const postForm = reactive({
  title: '',
  content: ''
})

const loadCommunities = async () => {
  try {
    communities.value = await communityAPI.getList()
    if (communities.value.length > 0) {
      selectCommunity(communities.value[0].id)
    }
  } catch (error) {
    ElMessage.error('加载社区失败')
  }
}

const selectCommunity = async (communityId) => {
  selectedCommunity.value = communityId
  try {
    posts.value = await communityAPI.getPosts(communityId)
  } catch (error) {
    ElMessage.error('加载帖子失败')
  }
}

const submitPost = async () => {
  if (!postForm.title || !postForm.content) {
    ElMessage.warning('请填写完整信息')
    return
  }
  submitting.value = true
  try {
    await communityAPI.createPost({
      community_id: selectedCommunity.value,
      title: postForm.title,
      content: postForm.content
    })
    ElMessage.success('发布成功')
    showPostDialog.value = false
    postForm.title = ''
    postForm.content = ''
    selectCommunity(selectedCommunity.value)
  } catch (error) {
    ElMessage.error('发布失败')
  } finally {
    submitting.value = false
  }
}

const likePost = async (postId) => {
  try {
    await communityAPI.likePost(postId)
    ElMessage.success('点赞成功')
    const post = posts.value.find(p => p.id === postId)
    if (post) post.likes_count++
  } catch (error) {
    ElMessage.error('点赞失败')
  }
}

onMounted(() => {
  loadCommunities()
})
</script>

<style scoped>
.community-page {
  min-height: 60vh;
}

.page-hero {
  margin-bottom: 40px;
}

.page-hero h1 {
  font-size: 32px;
  font-weight: 700;
  color: var(--pc-cool);
  margin-bottom: 12px;
  letter-spacing: -0.02em;
}

.hero-tagline {
  font-size: 16px;
  color: var(--pc-cool-muted);
  line-height: 1.6;
  margin-bottom: 24px;
  max-width: 560px;
}

.hero-search {
  max-width: 400px;
}

.search-input {
  border-radius: 10px;
}

.layout-with-sidebar {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 32px;
}

@media (max-width: 900px) {
  .layout-with-sidebar {
    grid-template-columns: 1fr;
  }
  .communities-sidebar {
    order: 2;
  }
}

.communities-sidebar {
  position: sticky;
  top: 88px;
  height: fit-content;
}

.sidebar-card {
  background: white;
  border-radius: var(--pc-radius-lg);
  padding: 20px;
  box-shadow: var(--pc-shadow);
  border: 1px solid #f1f5f9;
}

.sidebar-card h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--pc-cool);
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--pc-warm);
}

.community-list {
  max-height: 400px;
  overflow-y: auto;
}

.community-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  padding: 12px 14px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  text-align: left;
  transition: background 0.2s;
  margin-bottom: 4px;
}

.community-item:hover {
  background: var(--pc-warm);
}

.community-item.active {
  background: var(--pc-warm);
  color: var(--pc-primary);
  font-weight: 500;
}

.community-item .name {
  font-size: 14px;
  color: inherit;
}

.community-item .count {
  font-size: 12px;
  color: var(--pc-cool-muted);
  margin-top: 4px;
}

.community-item.active .count {
  color: var(--pc-primary);
  opacity: 0.9;
}

.posts-main {
  min-width: 0;
}

.posts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.posts-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--pc-cool);
}

.posts-card {
  border-radius: var(--pc-radius-lg);
  box-shadow: var(--pc-shadow);
  border: 1px solid #f1f5f9;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.post-item {
  padding: 24px;
  border-bottom: 1px solid #f1f5f9;
}

.post-item:last-child {
  border-bottom: none;
}

.post-title {
  margin: 0 0 10px 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--pc-cool);
}

.post-content {
  color: var(--pc-cool-muted);
  line-height: 1.6;
  margin-bottom: 16px;
  font-size: 15px;
}

.post-meta {
  display: flex;
  gap: 20px;
  color: var(--pc-cool-muted);
  font-size: 13px;
  margin-bottom: 12px;
}

.post-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.post-actions {
  display: flex;
  gap: 10px;
}
</style>
