import { Link } from "react-router";

export function NaoEncontrada() {
  return (
    <section>
      <h1>Página não encontrada</h1>
      <p>O endereço não existe ou mudou.</p>
      <Link to="/">Voltar para a visão geral</Link>
    </section>
  );
}
