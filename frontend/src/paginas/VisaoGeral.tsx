import { StatusApi } from "../componentes/StatusApi";

// Tela "03 · Boas-vindas" do Figma (Visão geral).
export function VisaoGeral() {
  return (
    <section>
      <div className="cartao">
        <h1>Seu próximo capítulo começa aqui.</h1>
        <p>Conheça a empresa, aprenda no seu ritmo e conte com um guia em cada etapa.</p>
      </div>
      <StatusApi />
    </section>
  );
}
