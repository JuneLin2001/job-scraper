"use client";

import { useState } from "react";
import { useJobStore } from "@/store/useJobStore";
import MultipleSelector from "@/components/ui/multiple-selector";
import useFetchLabels from "@/hooks/useFetchLabels";

const Searchbar = () => {
  const { setSearchWord, handleLabelsSearch } = useJobStore();
  const { allLabels } = useFetchLabels();
  const [keyword, setKeyword] = useState("");
  const [labels, setLabels] = useState<string[]>([]);

  const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSearchWord(keyword);
    handleLabelsSearch(labels.join(","));
  };

  return (
    <form onSubmit={handleSearchSubmit} className="flex items-center gap-2">
      <input
        type="text"
        placeholder="請輸入關鍵字..."
        className="rounded border px-2 py-1"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
      />
      <MultipleSelector
        defaultOptions={allLabels.map((label) => ({ label, value: label }))}
        placeholder="標籤"
        emptyIndicator={
          <p className="text-center leading-10 text-gray-600 dark:text-gray-400">
            no results found.
          </p>
        }
        value={labels.map((label) => ({ label, value: label }))}
        onChange={(selectedOptions) =>
          setLabels(selectedOptions.map((o) => o.value))
        }
      />
      <button
        type="submit"
        className="rounded bg-blue-600 px-4 py-1 text-white hover:bg-blue-700"
      >
        搜尋
      </button>
    </form>
  );
};

export default Searchbar;
