"use client";

import { useEffect } from "react";
import { useJobStore } from "@/store/useJobStore";
import JobCard from "./JobCard";
import type { Job } from "@/types/job";

const JobCards = () => {
  const { jobData, fetchJobs } = useJobStore();

  useEffect(() => {
    fetchJobs();
  }, []);

  return (
    <div className="grid w-full max-w-6xl grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {jobData.map((job: Job) => (
        <JobCard key={job.id} job={job} />
      ))}
    </div>
  );
};

export default JobCards;
