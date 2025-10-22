import { create } from "zustand";
import type { Job, JobSource } from "@/types/job";

interface JobStore {
  source: JobSource | "";
  jobData: Job[];
  currentPage: number;
  totalPages: number;
  viewMode: "card" | "list";
  searchWord: string;
  labels: string;
  setViewMode: (viewMode: "card" | "list") => void;
  setSearchWord: (searchWord: string) => void;
  setSource: (source: JobSource | "") => void;
  handleLabelsSearch: (labels: string) => void;
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
  labels: "",
  handleLabelsSearch: (labels: string) => {
    set({ labels, currentPage: 1 });
    get().fetchJobs();
  },
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
    const { source, currentPage, searchWord, labels } = get();
    try {
      const response = await fetch(
        `http://localhost:8000/api/jobs/?source=${source}&page=${currentPage}&pagesize=30&search=${searchWord}&labels=${labels}`,
      );
      const data = await response.json();
      set({ jobData: data.jobs, totalPages: data.total_pages });
    } catch (error) {
      console.error("Error fetching jobs:", error);
    }
  },

  fetchAllLabels: async () => {
    try {
      const response = await fetch("http://localhost:8000/api/jobs/labels");
      const data = await response.json();
      set({ labels: data.labels });
    } catch (error) {
      console.error("Error fetching labels:", error);
    }
  },
}));
