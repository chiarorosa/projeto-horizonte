import { requisitar, usarDadosSimulados } from "./cliente";

// Formato de GET /health (backend/README.md, seção "Integração").
export type Saude = { status: string };

// Cada endpoint tem sua função aqui em src/api/, com a versão simulada ao lado,
// no mesmo formato do template de integração do backend.
export async function obterSaude(): Promise<Saude> {
  if (usarDadosSimulados()) return { status: "ok" };
  return requisitar<Saude>("/health");
}
