import request from '@/utils/request'

export const recordsAPI = {
  // 上传病历
  upload(formData) {
    return request.post('/records/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 获取病历列表
  getList() {
    return request.get('/records')
  },

  // 获取病历详情
  getDetail(id) {
    return request.get(`/records/${id}`)
  },

  // 删除病历
  delete(id) {
    return request.delete(`/records/${id}`)
  },

  // 处理病历（AI提取）
  process(id) {
    return request.post(`/records/${id}/process`)
  }
}
