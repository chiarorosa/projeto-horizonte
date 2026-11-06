import { StatusApi } from "../componentes/StatusApi";
import { EmConstrucao } from "./EmConstrucao";

export function VisaoGeral() {
  return (
    <>
      <EmConstrucao titulo="Visão geral" tela="03 · Boas-vindas" />
      <StatusApi />
    </>
  );
}
