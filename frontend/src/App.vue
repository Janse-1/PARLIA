<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MainLayout from './layouts/MainLayout.vue'
import AuthLayout from './layouts/AuthLayout.vue'

const route = useRoute()
const layoutType = computed(() => route.meta.layout || 'main')
</script>

<template>
  <router-view v-if="layoutType === 'landing'" />
  <AuthLayout v-else-if="layoutType === 'auth'">
    <router-view />
  </AuthLayout>
  <MainLayout v-else>
    <router-view />
  </MainLayout>
</template>
