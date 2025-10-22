"use client";

import { Button } from "@/components/ui/button";
import { SquareKanban, Rows3 } from "lucide-react";
import { useJobStore } from "@/store/useJobStore";

const SwitchViewModeButton = () => {
  const { viewMode, setViewMode } = useJobStore();

  const handleSwitchViewMode = () => {
    if (viewMode === "card") {
      setViewMode("list");
    } else {
      setViewMode("card");
    }
  };

  return (
    <Button variant="ghost" size="icon" onClick={handleSwitchViewMode}>
      {viewMode === "card" ? <SquareKanban /> : <Rows3 />}
    </Button>
  );
};

export default SwitchViewModeButton;
