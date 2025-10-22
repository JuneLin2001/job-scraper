"use client";

import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { useJobStore } from "@/store/useJobStore";

const JobPagination = () => {
  const { currentPage, totalPages, handleCurrentPageChange } = useJobStore();

  const handlePagePrevious = () => {
    if (currentPage > 1) {
      handleCurrentPageChange(currentPage - 1);
    }
  };

  const handlePageNext = () => {
    if (currentPage < totalPages) {
      handleCurrentPageChange(currentPage + 1);
    }
  };

  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious onClick={handlePagePrevious} />
        </PaginationItem>
        {Array.from({ length: totalPages }, (_, index) => (
          <PaginationItem key={index}>
            <PaginationLink
              isActive={index + 1 === currentPage}
              onClick={handlePagePrevious}
            >
              {index + 1}
            </PaginationLink>
          </PaginationItem>
        ))}

        <PaginationItem>
          <PaginationNext onClick={handlePageNext} />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  );
};

export default JobPagination;
