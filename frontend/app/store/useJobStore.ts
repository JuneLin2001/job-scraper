import { create } from "zustand";
import type { Job, JobSource } from "@/types/job";

interface JobStore {
  source: JobSource | "";
  jobData: Job[];
  currentPage: number;
  totalPages: number;
  viewMode: "card" | "list";
  searchWord: string;
  setViewMode: (viewMode: "card" | "list") => void;
  setSearchWord: (searchWord: string) => void;
  setSource: (source: JobSource | "") => void;
  handleCurrentPageChange: (currentPage: number) => void;
  fetchJobs: () => Promise<void>;
}

export const useJobStore = create<JobStore>((set, get) => ({
  source: "",
  jobData: [],
  currentPage: 1,
  totalPages: 1,
  viewMode: "card",
  searchWord: "",
  setViewMode: (viewMode) => set({ viewMode }),
  setSearchWord: (searchWord: string) => {
    set({ searchWord, currentPage: 1 });
    get().fetchJobs();
  },
  setSource: (source) => {
    set({ source, currentPage: 1 });
    get().fetchJobs();
  },

  handleCurrentPageChange: (currentPage) => {
    set({ currentPage });
    get().fetchJobs();
  },

  fetchJobs: async () => {
    const { source, currentPage, searchWord } = get();
    try {
      const response = await fetch(
        `http://localhost:8000/api/jobs/?source=${source}&page=${currentPage}&pagesize=30&search=${searchWord}`,
      );
      const data = await response.json();
      set({ jobData: data.jobs, totalPages: data.total_pages });
    } catch (error) {
      console.error("Error fetching jobs:", error);
    }
  },
}));
