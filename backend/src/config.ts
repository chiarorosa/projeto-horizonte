import { z } from "zod";

// Variáveis de ambiente validadas na inicialização: se faltar ou estiver
// errada, o servidor não sobe e a mensagem diz qual variável corrigir.
const esquema = z.object({
  BACKEND_PORT: z.coerce.number().int().positive().default(8000),
});

export const config = esquema.parse(process.env);
