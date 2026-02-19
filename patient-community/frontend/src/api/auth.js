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
  }
}
