import request from '@/utils/request'

export const matchAPI = {
  // 获取相似患者
  getSimilarPatients() {
    return request.get('/match/similar')
  },

  // 获取推荐方案
  getRecommendations() {
    return request.get('/match/recommendations')
  }
}
