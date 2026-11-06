import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { Rotas } from "./App";

// Teste de fumaça: a aplicação abre com o menu do Figma, usa os dados simulados e navega.
it("abre a visão geral e navega pelo menu", async () => {
  vi.stubEnv("VITE_USAR_DADOS_SIMULADOS", "true");
  render(
    <MemoryRouter>
      <Rotas />
    </MemoryRouter>,
  );

  expect(await screen.findByText("API no ar (dados simulados)")).toBeInTheDocument();

  await userEvent.click(screen.getByRole("link", { name: "Assistente IA" }));

  expect(screen.getByRole("heading", { level: 1, name: "Assistente IA" })).toBeInTheDocument();
});
