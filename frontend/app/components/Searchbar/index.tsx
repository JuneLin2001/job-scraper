"use client";

const Searchbar = () => {
  const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
  };

  return (
    <form onSubmit={handleSearchSubmit}>
      <input type="text" placeholder="Search..." />
    </form>
  );
};

export default Searchbar;
