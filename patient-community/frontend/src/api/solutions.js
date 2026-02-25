import request from '@/utils/request'

export const solutionsAPI = {
  /** 用户侧：仅已通过审核的列表，可按疾病筛选 */
  getList(params = {}) {
    return request.get('/solutions', { params })
  },

  /** 用户侧：方案详情（仅已通过） */
  getDetail(id) {
    return request.get(`/solutions/${id}`)
  },

  /** 患者：新建方案（待审核） */
  create(data) {
    return request.post('/solutions', data)
  }
}
