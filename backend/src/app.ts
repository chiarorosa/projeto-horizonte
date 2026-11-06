import express from "express";
import swaggerUi from "swagger-ui-express";
import { rotaNaoEncontrada, tratarErro } from "./erros.js";
import { openapi } from "./openapi.js";

export function createApp() {
  const app = express();
  app.use(express.json());

  app.get("/health", (_req, res) => {
    res.json({ status: "ok" });
  });

  app.get("/docs/openapi.json", (_req, res) => {
    res.json(openapi);
  });
  app.use("/docs", swaggerUi.serve, swaggerUi.setup(openapi));

  // Sempre por último: rotas inexistentes e erros no formato comum.
  app.use(rotaNaoEncontrada);
  app.use(tratarErro);

  return app;
}
