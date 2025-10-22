"use client";

import { useJobStore } from "@/store/useJobStore";
import DefaultPagination from "./DefaultPagination";
import { useSearchParams, useRouter } from "next/navigation";

const JobPagination = () => {
  const searchParams = useSearchParams();
  const currentPage = Number(searchParams.get("page") || 1);
  const router = useRouter();

  const { totalPages, handleCurrentPageChange } = useJobStore();

  const handlePageChange = (page: number) => {
    handleCurrentPageChange(page);
    router.push(`?page=${page}`);
  };

  const handlePagePrevious = () => {
    if (currentPage > 1) {
      handleCurrentPageChange(currentPage - 1);
      router.push(`?page=${currentPage - 1}`);
    }
  };

  const handlePageNext = () => {
    if (currentPage < totalPages) {
      handleCurrentPageChange(currentPage + 1);
      router.push(`?page=${currentPage + 1}`);
    }
  };

  return (
    <DefaultPagination
      currentPage={currentPage}
      totalPages={totalPages}
      handlePageChange={handlePageChange}
      handlePagePrevious={handlePagePrevious}
      handlePageNext={handlePageNext}
    />
  );
};

export default JobPagination;
