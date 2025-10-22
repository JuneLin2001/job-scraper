import {
  Pagination,
  PaginationContent,
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
              onClick={() => handlePageChange(index + 1)}
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

export default DefaultPagination;
