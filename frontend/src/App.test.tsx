import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { Rotas } from "./App";

function renderizarEm(caminho: string) {
  return render(
    <MemoryRouter initialEntries={[caminho]}>
      <Rotas />
    </MemoryRouter>,
  );
}

describe("navegação", () => {
  it("mostra o menu lateral do Figma", () => {
    renderizarEm("/");

    const menu = screen.getByRole("navigation", { name: "Menu principal" });
    for (const item of ["Visão geral", "Minha trilha", "Assistente IA", "Conquistas", "Central de ajuda"]) {
      expect(menu).toHaveTextContent(item);
    }
  });

  it("troca de página pelo menu e marca o item ativo", async () => {
    renderizarEm("/");

    await userEvent.click(screen.getByRole("link", { name: "Assistente IA" }));

    expect(screen.getByRole("heading", { level: 1, name: "Assistente IA" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Assistente IA" })).toHaveAttribute("aria-current", "page");
  });

  it("mostra a página não encontrada para rota inexistente", () => {
    renderizarEm("/nao-existe");

    expect(screen.getByRole("heading", { name: "Página não encontrada" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Voltar para a visão geral" })).toHaveAttribute("href", "/");
  });
});
