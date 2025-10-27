import { create } from "zustand";

interface LabelStore {
  allLabels: string[];
  setAllLabels: (labels: string[]) => void;
}

export const useLabelStore = create<LabelStore>((set) => ({
  allLabels: [],
  setAllLabels: (labels) => set({ allLabels: labels }),
}));
