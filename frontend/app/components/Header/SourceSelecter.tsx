"use client";

import type { JobSource } from "@/types/job";
import { useJobStore } from "@/store/useJobStore";

const SourceSelecter = () => {
  const { source, setSource } = useJobStore();

  return (
    <select
      value={source}
      onChange={(e) => setSource(e.target.value as JobSource)}
    >
      <option value="">All</option>
      <option value="104">104</option>
      <option value="1111">1111</option>
    </select>
  );
};

export default SourceSelecter;
