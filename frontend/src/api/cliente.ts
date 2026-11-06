// Cliente único da API do backend. Todas as chamadas passam por aqui.
// O frontend nunca chama o serviço de IA diretamente nem guarda chaves.

export class ErroApi extends Error {
  constructor(
    readonly status: number,
    readonly codigo: string,
    mensagem: string,
    readonly detalhes: Record<string, unknown> = {},
  ) {
    super(mensagem);
  }
}

// Lidas a cada chamada (e não uma vez só) para os testes poderem trocar com vi.stubEnv.
export function urlDaApi(): string {
  return import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
}

export function usarDadosSimulados(): boolean {
  return import.meta.env.VITE_USAR_DADOS_SIMULADOS === "true";
}

export async function requisitar<T>(caminho: string, opcoes: RequestInit = {}): Promise<T> {
  let resposta: Response;
  try {
    resposta = await fetch(`${urlDaApi()}${caminho}`, {
      ...opcoes,
      headers: { "Content-Type": "application/json", ...opcoes.headers },
    });
  } catch {
    throw new ErroApi(0, "SEM_CONEXAO", "Não foi possível falar com a API.");
  }

  const corpo = await resposta.json().catch(() => null);
  if (!resposta.ok) {
    // Formato de erro comum (backend/README.md, seção "Integração").
    const erro = corpo?.erro;
    throw new ErroApi(resposta.status, erro?.codigo ?? "ERRO_DESCONHECIDO", erro?.mensagem ?? "Erro na API.", erro?.detalhes);
  }
  return corpo as T;
}
