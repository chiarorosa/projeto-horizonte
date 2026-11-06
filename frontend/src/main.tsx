import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { VisaoGeral } from "./paginas/VisaoGeral";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <VisaoGeral />
  </StrictMode>,
);
