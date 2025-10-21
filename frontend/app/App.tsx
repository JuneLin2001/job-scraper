"use client";

import { useState, useEffect } from "react";
import JobCard from "@/components/Card/JobCard";
import type { Job } from "@/types/job";

const App = () => {
  const [source, setSource] = useState("104");
  const [jobData, setJobData] = useState([]);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/jobs/?source=${source}`,
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setJobData(data.jobs);
      } catch (error) {
        console.error("Error fetching jobs:", error);
      }
    };

    fetchJobs();
  }, [source]);

  return (
    <div className="flex flex-col items-center gap-6 py-8">
      <select value={source} onChange={(e) => setSource(e.target.value)}>
        <option value="104">104</option>
        <option value="1111">1111</option>
      </select>
      <div className="container flex w-full justify-center px-6">
        <div className="grid w-full max-w-6xl grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {jobData.map((job: Job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;
