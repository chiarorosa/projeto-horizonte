import react from "@vitejs/plugin-react";
import { loadEnv } from "vite";
import { defineConfig } from "vitest/config";

// As variáveis vêm do .env da raiz do repositório (só as com prefixo VITE_ chegam ao navegador).
const RAIZ = "..";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, RAIZ, "");
  return {
    plugins: [react()],
    envDir: RAIZ,
    server: {
      port: Number(env.FRONTEND_PORT || 3000),
      // O navegador chama /api/... no próprio frontend e o Vite repassa ao backend (API_BASE_URL).
      // Assim não há chamada para outro domínio (sem CORS) e nenhum endereço fica no código.
      proxy: {
        "/api": {
          target: env.API_BASE_URL || "http://localhost:8000",
          changeOrigin: true,
          rewrite: (caminho) => caminho.replace(/^\/api/, ""),
        },
      },
    },
    test: {
      environment: "jsdom",
      globals: true,
      setupFiles: ["./src/test/setup.ts"],
      include: ["src/**/*.test.{ts,tsx}"],
    },
  };
});
