<template>
  <el-dialog
    v-model="visible"
    title="个人资料构建器"
    width="560px"
    :close-on-click-modal="false"
    :show-close="false"
    class="profile-builder-dialog"
    @closed="handleClosed"
  >
    <el-tabs v-model="activeTab" class="profile-builder-tabs">
      <el-tab-pane label="关于我" name="about">
        <p class="dialog-hint">请补充联系方式，以便我们与您建立有益的联系</p>
        <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" class="profile-form">
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
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="条件权益" name="conditions">
        <p class="dialog-hint">添加您关注的健康状况，可帮助个性化您的体验、推荐相关治疗方案</p>
        <el-checkbox-group v-model="form.interested_conditions" class="conditions-group">
          <el-checkbox
            v-for="item in DISEASE_OPTIONS"
            :key="item"
            :label="item"
            class="condition-checkbox"
          >
            {{ item }}
          </el-checkbox>
        </el-checkbox-group>
      </el-tab-pane>
    </el-tabs>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleSkip">稍后再说</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">
          保存
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { authAPI } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  modelValue: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue', 'complete', 'skip'])

const userStore = useUserStore()
const formRef = ref(null)
const saving = ref(false)

const visible = ref(props.modelValue)

watch(() => props.modelValue, (v) => { visible.value = v })
watch(visible, (v) => { emit('update:modelValue', v) })

const DISEASE_OPTIONS = ['糖尿病', '高血压', '慢性肾病', '冠心病', '类风湿关节炎', '哮喘']

const activeTab = ref('about')
const form = reactive({
  email: '',
  phone: '',
  interested_conditions: []
})

const rules = {
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$|^$/, message: '请输入正确的手机号或留空', trigger: 'blur' }
  ]
}

function initForm() {
  const u = userStore.userInfo
  form.email = u?.email ?? ''
  form.phone = u?.phone ?? ''
  form.interested_conditions = Array.isArray(u?.interested_conditions)
    ? [...u.interested_conditions]
    : []
}

function handleSave() {
  formRef.value?.validate().then(async () => {
    saving.value = true
    try {
      const data = await authAPI.updateProfile({
        email: form.email || null,
        phone: form.phone || null,
        interested_conditions: form.interested_conditions?.length ? form.interested_conditions : null
      })
      userStore.setUserInfo(data)
      ElMessage.success('保存成功')
      visible.value = false
      emit('complete')
    } catch (e) {
      ElMessage.error(e.response?.data?.detail || '保存失败')
    } finally {
      saving.value = false
    }
  }).catch(() => {})
}

function handleSkip() {
  visible.value = false
  emit('skip')
}

function handleClosed() {
  formRef.value?.resetFields()
}

watch(visible, (v) => {
  if (v) initForm()
})
</script>

<style scoped>
.profile-builder-dialog :deep(.el-dialog__body) {
  padding-top: 8px;
}

.dialog-hint {
  font-size: 14px;
  color: var(--pc-cool-muted);
  margin-bottom: 20px;
}

.profile-form {
  margin-bottom: 8px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.conditions-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.condition-checkbox {
  margin-right: 0;
}

.profile-builder-tabs :deep(.el-tabs__content) {
  padding-top: 12px;
}
</style>
