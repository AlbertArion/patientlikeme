import request from '@/utils/request'

export const communityAPI = {
  // 获取社区列表
  getList() {
    return request.get('/communities')
  },

  // 获取社区帖子
  getPosts(communityId) {
    return request.get(`/communities/${communityId}/posts`)
  },

  // 发布帖子
  createPost(data) {
    return request.post('/posts', data)
  },

  // 发表评论
  createComment(postId, content) {
    return request.post(`/posts/${postId}/comments`, { content })
  },

  // 点赞
  likePost(postId) {
    return request.post(`/posts/${postId}/like`)
  }
}
