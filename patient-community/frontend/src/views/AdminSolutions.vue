<template>
  <AppLayout>
    <div class="admin-solutions-page">
      <div class="container-wide">
        <section class="admin-header">
          <h1>治疗方案 · 运营管理</h1>
          <div v-if="!adminKeySet" class="admin-login">
            <el-input
              v-model="adminKeyInput"
              type="password"
              placeholder="请输入管理密钥 (X-Admin-Key)"
              style="width: 260px; margin-right: 8px"
              show-password
              @keyup.enter="setAdminKey"
            />
            <el-button type="primary" @click="setAdminKey">进入</el-button>
          </div>
          <div v-else class="admin-actions">
            <el-radio-group v-model="statusFilter" size="small" @change="loadList">
              <el-radio-button value="">全部</el-radio-button>
              <el-radio-button value="pending">待审核</el-radio-button>
              <el-radio-button value="approved">已通过</el-radio-button>
              <el-radio-button value="rejected">已拒绝</el-radio-button>
            </el-radio-group>
            <el-button size="small" @click="clearAdminKey">退出管理</el-button>
          </div>
        </section>

        <template v-if="adminKeySet">
          <el-table v-loading="loading" :data="list" stripe class="admin-table">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="title" label="方案名称" min-width="160" />
            <el-table-column prop="disease_name" label="疾病类型" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.status === 'pending'" type="warning">待审核</el-tag>
                <el-tag v-else-if="row.status === 'approved'" type="success">已通过</el-tag>
                <el-tag v-else type="info">已拒绝</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="success_rate" label="感知有效性" width="90" />
            <el-table-column prop="user_count" label="使用人数" width="90" />
            <el-table-column prop="created_at" label="创建时间" width="170">
              <template #default="{ row }">
                {{ row.created_at ? formatDate(row.created_at) : '-' }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="220" fixed="right">
              <template #default="{ row }">
                <el-button v-if="row.status === 'pending'" type="success" link size="small" @click="approve(row)">通过</el-button>
                <el-button v-if="row.status === 'pending'" type="danger" link size="small" @click="reject(row)">拒绝</el-button>
                <el-button type="primary" link size="small" @click="openEdit(row)">编辑</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-if="!loading && list.length === 0" description="暂无数据" />
        </template>
      </div>

      <!-- 编辑弹窗 -->
      <el-dialog v-model="editVisible" title="编辑方案" width="520px" destroy-on-close @close="editFormRef?.resetFields()">
        <el-form ref="editFormRef" :model="editForm" :rules="editRules" label-width="90px">
          <el-form-item label="方案名称" prop="title">
            <el-input v-model="editForm.title" maxlength="200" show-word-limit />
          </el-form-item>
          <el-form-item label="疾病类型" prop="disease_name">
            <el-input v-model="editForm.disease_name" maxlength="100" show-word-limit />
          </el-form-item>
          <el-form-item label="方案描述" prop="description">
            <el-input v-model="editForm.description" type="textarea" :rows="4" maxlength="2000" show-word-limit />
          </el-form-item>
          <el-form-item label="感知有效性" prop="success_rate">
            <el-input v-model="editForm.success_rate" maxlength="20" placeholder="如：85%" />
          </el-form-item>
          <el-form-item label="使用人数" prop="user_count">
            <el-input-number v-model="editForm.user_count" :min="0" style="width: 160px" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="editVisible = false">取消</el-button>
          <el-button type="primary" :loading="editSaving" @click="saveEdit">保存</el-button>
        </template>
      </el-dialog>

      <!-- 拒绝原因弹窗 -->
      <el-dialog v-model="rejectVisible" title="拒绝原因" width="400px">
        <el-input v-model="rejectReason" type="textarea" :rows="3" placeholder="选填，填写拒绝原因" maxlength="500" show-word-limit />
        <template #footer>
          <el-button @click="rejectVisible = false">取消</el-button>
          <el-button type="danger" :loading="rejecting" @click="confirmReject">确认拒绝</el-button>
        </template>
      </el-dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import AppLayout from '@/components/AppLayout.vue'
import { adminSolutionsAPI } from '@/api/adminSolutions'

const ADMIN_KEY_STORAGE = 'pc_admin_key'

const adminKeyInput = ref('')
const adminKeySet = ref(!!localStorage.getItem(ADMIN_KEY_STORAGE))
const statusFilter = ref('')
const list = ref([])
const loading = ref(false)
const editVisible = ref(false)
const editFormRef = ref(null)
const editForm = reactive({
  id: null,
  title: '',
  disease_name: '',
  description: '',
  success_rate: '',
  user_count: 0
})
const editRules = {
  title: [{ required: true, message: '请输入方案名称', trigger: 'blur' }],
  disease_name: [{ required: true, message: '请输入疾病类型', trigger: 'blur' }]
}
const editSaving = ref(false)
const rejectVisible = ref(false)
const rejectReason = ref('')
const rejecting = ref(false)
const rejectTarget = ref(null)

function setAdminKey() {
  const key = adminKeyInput.value?.trim()
  if (!key) {
    ElMessage.warning('请输入管理密钥')
    return
  }
  localStorage.setItem(ADMIN_KEY_STORAGE, key)
  adminKeySet.value = true
  adminKeyInput.value = ''
  loadList()
}

function clearAdminKey() {
  localStorage.removeItem(ADMIN_KEY_STORAGE)
  adminKeySet.value = false
  list.value = []
}

function formatDate(val) {
  if (!val) return '-'
  const d = new Date(val)
  return d.toLocaleString('zh-CN')
}

async function loadList() {
  loading.value = true
  try {
    const params = statusFilter.value ? { status_filter: statusFilter.value } : {}
    list.value = await adminSolutionsAPI.getList(params)
  } catch (e) {
    if (e?.response?.status === 403) {
      ElMessage.error('管理密钥无效')
      localStorage.removeItem(ADMIN_KEY_STORAGE)
      adminKeySet.value = false
      list.value = []
    } else {
      ElMessage.error(e?.response?.data?.detail || '加载失败')
    }
    list.value = []
  } finally {
    loading.value = false
  }
}

async function approve(row) {
  try {
    await adminSolutionsAPI.review(row.id, { action: 'approve' })
    ElMessage.success('已通过')
    loadList()
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '操作失败')
  }
}

function reject(row) {
  rejectTarget.value = row
  rejectReason.value = ''
  rejectVisible.value = true
}

async function confirmReject() {
  const row = rejectTarget.value
  if (!row) return
  rejecting.value = true
  try {
    await adminSolutionsAPI.review(row.id, {
      action: 'reject',
      reject_reason: rejectReason.value?.trim() || undefined
    })
    ElMessage.success('已拒绝')
    rejectVisible.value = false
    rejectTarget.value = null
    loadList()
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '操作失败')
  } finally {
    rejecting.value = false
  }
}

function openEdit(row) {
  editForm.id = row.id
  editForm.title = row.title
  editForm.disease_name = row.disease_name
  editForm.description = row.description || ''
  editForm.success_rate = row.success_rate || ''
  editForm.user_count = row.user_count ?? 0
  editVisible.value = true
}

async function saveEdit() {
  await editFormRef.value?.validate().catch(() => {})
  editSaving.value = true
  try {
    await adminSolutionsAPI.update(editForm.id, {
      title: editForm.title.trim(),
      disease_name: editForm.disease_name.trim(),
      description: editForm.description?.trim() || '',
      success_rate: editForm.success_rate?.trim() || null,
      user_count: editForm.user_count ?? 0
    })
    ElMessage.success('已保存')
    editVisible.value = false
    loadList()
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '保存失败')
  } finally {
    editSaving.value = false
  }
}

onMounted(() => {
  if (adminKeySet.value) loadList()
})
</script>

<style scoped>
.admin-solutions-page {
  min-height: 60vh;
  padding: 24px 0 48px;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.admin-header h1 {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  color: var(--pc-cool);
}

.admin-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.admin-table {
  margin-top: 8px;
}
</style>
