import type { ErrorRequestHandler, RequestHandler } from "express";
import { z } from "zod";

// Formato de erro comum (backend/README.md, seção "Integração").
type CorpoErro = {
  erro: { codigo: string; mensagem: string; detalhes: Record<string, unknown> };
};

// Erro esperado de negócio: lance `new AppError(404, "TRILHA_NAO_ENCONTRADA", "...")`.
export class AppError extends Error {
  constructor(
    readonly status: number,
    readonly codigo: string,
    mensagem: string,
    readonly detalhes: Record<string, unknown> = {},
  ) {
    super(mensagem);
  }
}

function corpo(codigo: string, mensagem: string, detalhes: Record<string, unknown> = {}): CorpoErro {
  return { erro: { codigo, mensagem, detalhes } };
}

export const rotaNaoEncontrada: RequestHandler = (req, res) => {
  res.status(404).json(corpo("ROTA_NAO_ENCONTRADA", `Rota não encontrada: ${req.method} ${req.path}`));
};

export const tratarErro: ErrorRequestHandler = (err, _req, res, _next) => {
  if (err instanceof AppError) {
    res.status(err.status).json(corpo(err.codigo, err.message, err.detalhes));
    return;
  }
  if (err instanceof z.ZodError) {
    res.status(400).json(corpo("REQUISICAO_INVALIDA", "Dados inválidos.", { campos: z.flattenError(err).fieldErrors }));
    return;
  }
  // Corpo JSON malformado (lançado pelo express.json()).
  if (err?.type === "entity.parse.failed") {
    res.status(400).json(corpo("REQUISICAO_INVALIDA", "JSON inválido no corpo da requisição."));
    return;
  }
  console.error(err);
  res.status(500).json(corpo("ERRO_INTERNO", "Erro interno do servidor."));
};
