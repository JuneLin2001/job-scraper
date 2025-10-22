import SourceSelecter from "./SourceSelecter";
import Searchbar from "../Searchbar";
import SwitchViewModeButton from "./SwitchViewModeButton";

export function Header() {
  return (
    <header className="ml-64 flex items-center justify-between border-b p-4">
      <SourceSelecter />
      <SwitchViewModeButton />
      <Searchbar />
    </header>
  );
}
