<script setup lang="ts">
import { ref, onMounted } from "vue";
import Card from "@/components/Card.vue";
import type { Job } from "@/types/job";

const jobs = ref<Job[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const source = ref("104");

const fetchJobs = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await fetch(
      `http://localhost:8000/api/jobs/?source=${source.value}`,
    );
    if (!res.ok) throw new Error("Failed to fetch jobs");
    const data = await res.json();
    jobs.value = data.jobs;
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchJobs();
});
</script>

<template>
  <h1 class="mb-4 text-3xl font-bold underline">Job List</h1>
  <div v-if="loading">Loading...</div>
  <div v-if="error" class="text-red-500">{{ error }}</div>
  <select v-model="source" @change="fetchJobs" class="mb-4 rounded border p-2">
    <option value="104">104</option>
    <option value="1111">1111</option>
  </select>
  <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
    <div
      v-for="job in jobs"
      :key="job.id"
      class="card bg-base-100 w-full shadow-md"
    >
      <Card :job="job" />
    </div>
  </div>
</template>
