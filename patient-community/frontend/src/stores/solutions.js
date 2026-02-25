import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const STORAGE_KEY = 'pc_using_solution_ids'

function loadIds() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    const arr = JSON.parse(raw)
    return Array.isArray(arr) ? arr : []
  } catch {
    return []
  }
}

function saveIds(ids) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(ids))
}

export const useSolutionsStore = defineStore('solutions', () => {
  const usingIds = ref(loadIds())

  const usingSet = computed(() => new Set(usingIds.value))

  function isUsing(id) {
    return usingSet.value.has(Number(id))
  }

  function addUsing(id) {
    const numId = Number(id)
    if (usingIds.value.includes(numId)) return
    usingIds.value = [...usingIds.value, numId]
    saveIds(usingIds.value)
  }

  return {
    usingIds,
    isUsing,
    addUsing
  }
})
