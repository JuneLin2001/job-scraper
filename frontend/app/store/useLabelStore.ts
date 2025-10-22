import { create } from "zustand";
import type { Job, JobSource } from "@/types/job";

interface LabelStore {
  allLabels: string[];
  fetchAllLabels: () => Promise<void>;
}

export const useLabelStore = create<LabelStore>((set, get) => ({
  allLabels: [],
  fetchAllLabels: async () => {
    try {
      const response = await fetch("http://localhost:8000/api/jobs/labels");
      const data = await response.json();
      set({ allLabels: data.labels });
    } catch (error) {
      console.error("Error fetching labels:", error);
    }
  },
}));
