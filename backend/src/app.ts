import express from "express";
import { rotaNaoEncontrada, tratarErro } from "./erros.js";

export function createApp() {
  const app = express();
  app.use(express.json());

  app.get("/health", (_req, res) => {
    res.json({ status: "ok" });
  });

  // Sempre por último: rotas inexistentes e erros no formato comum.
  app.use(rotaNaoEncontrada);
  app.use(tratarErro);

  return app;
}
