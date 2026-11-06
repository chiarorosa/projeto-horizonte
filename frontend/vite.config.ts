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
    server: { port: Number(env.FRONTEND_PORT || 3000) },
    test: {
      environment: "jsdom",
      globals: true,
      setupFiles: ["./src/test/setup.ts"],
      include: ["src/**/*.test.{ts,tsx}"],
    },
  };
});
