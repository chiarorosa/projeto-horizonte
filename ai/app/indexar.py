"""Indexa um documento de texto no pgvector.

Uso: python -m app.indexar exemplos/politica-de-senhas.md --id doc-politica-senhas --titulo "Política de Senhas"
"""

import argparse
from pathlib import Path

from app.config import get_settings
from app.provedores import criar_indice
from app.rag import indexar


def main() -> None:
    args = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    args.add_argument("arquivo", type=Path, help="arquivo .md ou .txt (só documentos autorizados, sintéticos ou anonimizados)")
    args.add_argument("--id", required=True, help="documento_id, o mesmo usado pelo Backend")
    args.add_argument("--titulo", required=True)
    a = args.parse_args()

    if a.arquivo.suffix.lower() not in {".md", ".txt"}:
        args.error("por enquanto só arquivos .md e .txt")
    chunks = indexar(criar_indice(get_settings()), a.arquivo.read_text(encoding="utf-8"), a.id, a.titulo)
    print(f"{a.id}: {chunks} chunk(s) indexado(s).")


if __name__ == "__main__":
    main()
