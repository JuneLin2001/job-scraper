"use client";

import { useEffect, useCallback } from "react";
import { useLabelStore } from "@/store/useLabelStore";

const useFetchLabels = () => {
  const { allLabels, setAllLabels } = useLabelStore();

  const fetchAllLabels = useCallback(async () => {
    try {
      const response = await fetch("http://localhost:8000/api/jobs/labels");
      const data = await response.json();
      setAllLabels(data.labels || []);
    } catch (error) {
      console.error("Error fetching labels:", error);
    }
  }, [setAllLabels]);

  useEffect(() => {
    fetchAllLabels();
  }, [fetchAllLabels]);

  return { allLabels };
};

export default useFetchLabels;
