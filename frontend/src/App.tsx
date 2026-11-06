import { Route, Routes } from "react-router";
import { Layout } from "./componentes/Layout";
import { EmConstrucao } from "./paginas/EmConstrucao";
import { NaoEncontrada } from "./paginas/NaoEncontrada";
import { VisaoGeral } from "./paginas/VisaoGeral";

// Rotas da aplicação. Cada tela nova entra aqui e no MENU de componentes/Layout.tsx.
export function Rotas() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<VisaoGeral />} />
        <Route path="trilha" element={<EmConstrucao titulo="Minha trilha" tela="09 · Minha trilha" />} />
        <Route path="assistente" element={<EmConstrucao titulo="Assistente IA" tela="19 · IA — resposta com fonte" />} />
        <Route path="conquistas" element={<EmConstrucao titulo="Conquistas" tela="17 · Conquistas" />} />
        <Route path="ajuda" element={<EmConstrucao titulo="Central de ajuda" tela="25 · Central de ajuda" />} />
        <Route path="*" element={<NaoEncontrada />} />
      </Route>
    </Routes>
  );
}
