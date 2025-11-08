"use client";

import { Pie, PieChart, Tooltip } from "recharts";
import { TooltipIndex } from "recharts/types/state/tooltipSlice";
import RenderActiveShape from "./RenderActiveShape";

// #region Sample data
const data = [
  { name: "Group A", value: 900 },
  { name: "Group B", value: 300 },
  { name: "Group C", value: 300 },
  { name: "Group D", value: 200 },
];

interface CustomActiveShapePieChartProps {
  isAnimationActive?: boolean;
  defaultIndex?: TooltipIndex;
}

const CustomActiveShapePieChart: React.FC<CustomActiveShapePieChartProps> = ({
  isAnimationActive = true,
  defaultIndex = undefined,
}) => {
  return (
    <div className="w-screen">
      <PieChart
        style={{
          width: "100%",
          maxWidth: "500px",
          maxHeight: "80vh",
          aspectRatio: 1,
        }}
        responsive
        margin={{
          top: 50,
          right: 120,
          bottom: 0,
          left: 120,
        }}
      >
        <Pie
          activeShape={RenderActiveShape}
          data={data}
          cx="50%"
          cy="50%"
          innerRadius="60%"
          outerRadius="80%"
          fill="#8884d8"
          dataKey="value"
          isAnimationActive={isAnimationActive}
        />
        <Tooltip content={() => null} defaultIndex={defaultIndex} />
      </PieChart>
    </div>
  );
};

export default CustomActiveShapePieChart;
