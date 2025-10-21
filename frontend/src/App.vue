<script setup lang="ts">
  import { ref, onMounted } from "vue";
  import Card from "./components/Card.vue";

  interface Job {
    id: number;
    title: string;
    salary: string;
    company_name: string;
    location: string;
    link?: string;
    description?: string;
  }

  const jobs = ref<Job[]>([]);
  const loading = ref(true);
  const error = ref<string | null>(null);

  const fetchJobs = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/jobs/");
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
  <h1 class="text-3xl font-bold underline mb-4">Job List</h1>
  <div v-if="loading">Loading...</div>
  <div v-if="error" class="text-red-500">{{ error }}</div>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <div
      v-for="job in jobs"
      :key="job.id"
      class="card w-full bg-base-100 shadow-md"
    >
      <Card :job="job" />
    </div>
  </div>
</template>
