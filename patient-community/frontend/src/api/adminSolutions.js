import request from '@/utils/request'

function getAdminHeaders() {
  const adminKey = localStorage.getItem('pc_admin_key') || ''
  return { 'X-Admin-Key': adminKey }
}

export const adminSolutionsAPI = {
  /** 运营：方案列表，可选 status=pending|approved|rejected */
  getList(params = {}) {
    return request.get('/admin/solutions', { params, headers: getAdminHeaders() })
  },

  getDetail(id) {
    return request.get(`/admin/solutions/${id}`, { headers: getAdminHeaders() })
  },

  update(id, data) {
    return request.put(`/admin/solutions/${id}`, data, { headers: getAdminHeaders() })
  },

  /** 审核：approve | reject，拒绝时可传 reject_reason */
  review(id, { action, reject_reason }) {
    return request.post(`/admin/solutions/${id}/review`, { action, reject_reason }, { headers: getAdminHeaders() })
  }
}
