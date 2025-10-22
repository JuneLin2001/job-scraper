import JobPagination from "@/components/Pagination/JobPagination";
import JobCards from "@/components/Card/JobCards";

const App = () => {
  return (
    <div className="flex flex-col items-center gap-6 py-8">
      <div className="container flex w-full justify-center px-6">
        <JobCards />
      </div>
      <JobPagination />
    </div>
  );
};

export default App;
