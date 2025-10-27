import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";

interface DefaultPaginationProps {
  currentPage: number;
  totalPages: number;
  handlePageChange: (page: number) => void;
  handlePagePrevious: () => void;
  handlePageNext: () => void;
}

const DefaultPagination: React.FC<DefaultPaginationProps> = ({
  currentPage,
  totalPages,
  handlePageChange,
  handlePagePrevious,
  handlePageNext,
}) => {
  // 每次最多顯示 10 個頁碼
  const maxVisiblePages = 10;
  const startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
  const endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

  const pages = Array.from(
    { length: endPage - startPage + 1 },
    (_, i) => startPage + i,
  );

  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious onClick={handlePagePrevious} />
        </PaginationItem>

        {startPage > 1 && (
          <>
            <PaginationItem>
              <PaginationLink onClick={() => handlePageChange(1)}>
                1
              </PaginationLink>
            </PaginationItem>
            <PaginationEllipsis />
          </>
        )}

        {pages.map((page) => (
          <PaginationItem key={page}>
            <PaginationLink
              isActive={page === currentPage}
              onClick={() => handlePageChange(page)}
            >
              {page}
            </PaginationLink>
          </PaginationItem>
        ))}

        {endPage < totalPages && (
          <>
            <PaginationEllipsis />
            <PaginationItem>
              <PaginationLink onClick={() => handlePageChange(totalPages)}>
                {totalPages}
              </PaginationLink>
            </PaginationItem>
          </>
        )}

        <PaginationItem>
          <PaginationNext onClick={handlePageNext} />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  );
};

export default DefaultPagination;
