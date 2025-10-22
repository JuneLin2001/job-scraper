import JobPagination from "@/components/Pagination/JobPagination";
import ShowJobs from "./ShowJobs";

const Jobs = () => {
  return (
    <div className="flex flex-col items-center gap-6 py-8">
      <ShowJobs />
      <JobPagination />
    </div>
  );
};

export default Jobs;
