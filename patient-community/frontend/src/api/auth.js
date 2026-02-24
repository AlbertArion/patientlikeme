import request from '@/utils/request'

export const authAPI = {
  // 用户注册
  register(data) {
    return request.post('/auth/register', data)
  },

  // 用户登录
  login(data) {
    return request.post('/auth/login', data)
  },

  // 获取用户信息
  getProfile() {
    return request.get('/auth/profile')
  },

  // 更新用户信息
  updateProfile(data) {
    return request.put('/auth/profile', data)
  },

  // 忘记密码 - 请求验证码
  forgotPasswordRequest(data) {
    return request.post('/auth/forgot-password/request', data)
  },

  // 忘记密码 - 重置
  forgotPasswordReset(data) {
    return request.post('/auth/forgot-password/reset', data)
  }
}
