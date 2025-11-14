import BarChartClient from "./BarChartClient";
import type { labelsWithCount } from "@/types/label";

export default async function Page() {
  type apiData = {
    total: number;
    labels: labelsWithCount;
  };

  const response = await fetch(
    "http://localhost:3000/api/fetchLabelsWithCount",
  );

  const data: apiData = await response.json();

  return (
    <div>
      <h2>Total Jobs: {data.total}</h2>
      <BarChartClient labelsWithCount={data.labels} />
    </div>
  );
}
