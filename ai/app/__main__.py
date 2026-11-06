"""Sobe o serviço na porta AI_PORT: python -m app"""

import uvicorn

from app.config import get_settings

uvicorn.run("app.main:app", port=get_settings().ai_port, reload=True)
