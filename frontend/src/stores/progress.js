import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { progressService } from '../services/progressService'

export const useProgressStore = defineStore('progress', () => {
  const totalLessons = ref(0)
  const completedLessons = ref(0)
  const overallPercentage = ref(0)
  const modules = ref([])
  const records = ref([])
  const loading = ref(false)
  const error = ref(null)

  const statusByLessonId = computed(() => {
    const map = {}
    for (const rec of records.value) {
      map[rec.lesson_id] = rec.status
    }
    return map
  })

  const moduleProgressById = computed(() => {
    const map = {}
    for (const mod of modules.value) {
      map[mod.module_id] = mod
    }
    return map
  })

  function getLessonStatus(lessonId) {
    return statusByLessonId.value[Number(lessonId)] || 'pending'
  }

  function getModuleSummary(moduleId) {
    return (
      moduleProgressById.value[Number(moduleId)] || {
        status: 'pending',
        percentage: 0,
        completed_lessons: 0,
        total_lessons: 0,
      }
    )
  }

  async function fetchMyProgress() {
    loading.value = true
    error.value = null
    try {
      const data = await progressService.getMyProgress()
      totalLessons.value = data.total_lessons || 0
      completedLessons.value = data.completed_lessons || 0
      overallPercentage.value = data.overall_percentage || 0
      modules.value = data.modules || []
      records.value = data.records || []
      return data
    } catch (err) {
      error.value = err.response?.data?.message || 'No se pudo cargar el progreso.'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateLessonProgress(lessonId, status) {
    const updatedRecord = await progressService.upsertProgress(Number(lessonId), status)
    await fetchMyProgress()
    return updatedRecord
  }

  function resetProgressState() {
    totalLessons.value = 0
    completedLessons.value = 0
    overallPercentage.value = 0
    modules.value = []
    records.value = []
    error.value = null
  }

  return {
    totalLessons,
    completedLessons,
    overallPercentage,
    modules,
    records,
    loading,
    error,
    statusByLessonId,
    moduleProgressById,
    getLessonStatus,
    getModuleSummary,
    fetchMyProgress,
    updateLessonProgress,
    resetProgressState,
  }
})

