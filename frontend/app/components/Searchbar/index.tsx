"use client";

import { useState } from "react";
import { useJobStore } from "@/store/useJobStore";

const Searchbar = () => {
  const { setSearchWord } = useJobStore();
  const [keyword, setKeyword] = useState("");

  const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSearchWord(keyword);
  };

  return (
    <form onSubmit={handleSearchSubmit} className="flex gap-2">
      <input
        type="text"
        placeholder="搜尋職缺或公司..."
        className="rounded border px-2 py-1"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
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
