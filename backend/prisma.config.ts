import { existsSync } from "node:fs";
import { defineConfig } from "prisma/config";

// O Prisma não lê o .env sozinho; usamos o .env da raiz do repositório.
if (existsSync("../.env")) process.loadEnvFile("../.env");

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
  },
  datasource: {
    url: process.env["DATABASE_URL"],
  },
});
