import { create } from "zustand";
import type { JobSource } from "@/types/job";

interface JobStore {
  source: JobSource | "";
  jobData: any[];
  currentPage: number;
  totalPages: number;
  setSource: (source: JobSource | "") => void;
  handleCurrentPageChange: (currentPage: number) => void;
  fetchJobs: () => Promise<void>;
}

export const useJobStore = create<JobStore>((set, get) => ({
  source: "",
  jobData: [],
  currentPage: 1,
  totalPages: 1,

  setSource: (source) => {
    set({ source, currentPage: 1 });
    get().fetchJobs();
  },

  handleCurrentPageChange: (currentPage) => {
    set({ currentPage });
    get().fetchJobs();
  },

  fetchJobs: async () => {
    const { source, currentPage } = get();
    try {
      const response = await fetch(
        `http://localhost:8000/api/jobs/?source=${source}&currentPage=${currentPage}&pagesize=30`,
      );
      const data = await response.json();
      set({ jobData: data.jobs, totalPages: data.total_pages });
    } catch (error) {
      console.error("Error fetching jobs:", error);
    }
  },
}));
