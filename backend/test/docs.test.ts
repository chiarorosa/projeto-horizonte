import request from "supertest";
import { describe, expect, it } from "vitest";
import { createApp } from "../src/app.js";

describe("documentação da API", () => {
  it("publica o OpenAPI com o GET /health", async () => {
    const res = await request(createApp()).get("/docs/openapi.json");

    expect(res.status).toBe(200);
    expect(res.body.openapi).toMatch(/^3\./);
    expect(res.body.paths["/health"]).toHaveProperty("get");
  });

  it("serve a interface do Swagger em /docs", async () => {
    const res = await request(createApp()).get("/docs/").redirects(1);

    expect(res.status).toBe(200);
    expect(res.text).toContain("swagger-ui");
  });
});
