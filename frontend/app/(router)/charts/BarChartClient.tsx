"use client";

import { Tooltip, BarChart, Bar, XAxis, YAxis } from "recharts";
import type { labelsWithCount } from "@/types/label";

interface BarChartClientProps {
  labelsWithCount: labelsWithCount;
}

const BarChartClient: React.FC<BarChartClientProps> = ({ labelsWithCount }) => {
  return (
    <BarChart width={800} height={300} data={labelsWithCount}>
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="count" />
    </BarChart>
  );
};

export default BarChartClient;
