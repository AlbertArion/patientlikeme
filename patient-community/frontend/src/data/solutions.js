/** 治疗方案静态数据，列表页与详情页共用 */
export const solutionsList = [
  {
    id: 1,
    disease_name: '糖尿病',
    title: '综合管理方案',
    description: '包括饮食控制、运动疗法和药物治疗的综合方案，通过科学的血糖管理和生活方式调整，有效控制糖尿病进展。',
    success_rate: '85%',
    user_count: 150
  },
  {
    id: 2,
    disease_name: '高血压',
    title: '降压治疗方案',
    description: '通过药物和生活方式调整控制血压，包括合理用药、低盐饮食、适量运动等综合措施。',
    success_rate: '90%',
    user_count: 200
  },
  {
    id: 3,
    disease_name: '慢性肾病',
    title: '肾功能保护方案',
    description: '延缓肾功能衰退的综合治疗方案，包括药物治疗、饮食管理和定期监测。',
    success_rate: '75%',
    user_count: 80
  },
  {
    id: 4,
    disease_name: '冠心病',
    title: '心血管康复方案',
    description: '通过药物治疗、运动康复和心理干预，改善心血管功能，预防心血管事件。',
    success_rate: '82%',
    user_count: 120
  },
  {
    id: 5,
    disease_name: '类风湿关节炎',
    title: '关节保护方案',
    description: '综合运用药物治疗、物理治疗和功能锻炼，减轻关节炎症，保护关节功能。',
    success_rate: '78%',
    user_count: 95
  },
  {
    id: 6,
    disease_name: '哮喘',
    title: '呼吸管理方案',
    description: '通过规范化的药物治疗和环境控制，有效控制哮喘症状，提高生活质量。',
    success_rate: '88%',
    user_count: 160
  }
]

export function getSolutionById(id) {
  const numId = typeof id === 'string' ? parseInt(id, 10) : id
  return solutionsList.find(s => s.id === numId) ?? null
}
