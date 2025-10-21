<script setup lang="ts">
  interface Job {
    id: number;
    title: string;
    salary: string;
    company_name: string;
    location: string;
    link?: string;
    description?: string;
  }

  defineProps<{ job: Job }>();
</script>

<template>
  <div class="card-body">
    <h2 class="card-title">{{ job.title }}</h2>
    <p class="text-sm text-gray-600">
      {{ job.company_name }} - {{ job.location }}
    </p>
    <p>{{ job.salary }}</p>
    <a
      v-if="job.link"
      :href="job.link"
      target="_blank"
      class="btn btn-primary mt-2"
      >查看</a
    >
  </div>
</template>

<style scoped>
  .read-the-docs {
    color: #888;
  }
</style>
