from fastapi import FastAPI

from app.erros import registrar_tratadores


def create_app() -> FastAPI:
    app = FastAPI(title="Projeto Horizonte — IA", version="0.1.0")
    registrar_tratadores(app)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
