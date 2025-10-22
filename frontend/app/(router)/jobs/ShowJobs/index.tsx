"use client";

import JobCards from "@/components/Card/JobCards";
import JobList from "@/components/List/JobList";
import { useJobStore } from "@/store/useJobStore";

const ShowJobs = () => {
  const { viewMode } = useJobStore();

  return (
    <>
      <div className="container flex w-full justify-center px-6">
        {viewMode === "card" ? <JobCards /> : <JobList />}
      </div>
    </>
  );
};

export default ShowJobs;
