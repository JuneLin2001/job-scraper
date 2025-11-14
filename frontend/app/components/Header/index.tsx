import SourceSelecter from "./SourceSelecter";
import Searchbar from "../Searchbar";
import SwitchViewModeButton from "./SwitchViewModeButton";

export default async function Header() {
  const response = await fetch("http://localhost:3000/api/labels");
  const data = await response.json();

  return (
    <header className="ml-64 flex items-center justify-between border-b p-4">
      <SourceSelecter />
      <SwitchViewModeButton />
      <Searchbar allLabels={data} />
    </header>
  );
}
