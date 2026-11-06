import { render, screen } from "@testing-library/react";
import { VisaoGeral } from "./VisaoGeral";

describe("Visão geral", () => {
  it("dá as boas-vindas ao colaborador", () => {
    render(<VisaoGeral />);

    expect(screen.getByRole("heading", { name: "Seu próximo capítulo começa aqui." })).toBeInTheDocument();
  });
});
