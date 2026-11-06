import { useEffect, useState } from "react";
import { ErroApi, usarDadosSimulados } from "../api/cliente";
import { obterSaude } from "../api/saude";

// Mostra se a API do backend responde (GET /health). Útil para conferir a configuração.
export function StatusApi() {
  const [texto, setTexto] = useState("Verificando a API…");

  useEffect(() => {
    obterSaude()
      .then(() => setTexto(usarDadosSimulados() ? "API no ar (dados simulados)" : "API no ar"))
      .catch((erro: unknown) => setTexto(`API fora do ar: ${erro instanceof ErroApi ? erro.message : "erro inesperado"}`));
  }, []);

  return (
    <p role="status" className="status-api">
      {texto}
    </p>
  );
}
