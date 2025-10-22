import SourceSelecter from "./SourceSelecter";

export function Header() {
  return (
    <header className="ml-64 flex items-center justify-between border-b p-4">
      <SourceSelecter />
    </header>
  );
}
