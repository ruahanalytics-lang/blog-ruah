"""
pipeline.py — executa gerar_artigo + publicar em sequência.
Este é o script chamado pelo agendador diário.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def run(script: str):
    result = subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=str(ROOT),
    )
    if result.returncode != 0:
        print(f"[ERRO] {script} falhou com código {result.returncode}")
        sys.exit(result.returncode)


if __name__ == "__main__":
    print("=" * 50)
    print("PIPELINE BLOG RUAH — iniciando")
    print("=" * 50)
    run("gerar_artigo.py")
    run("publicar.py")
    print("=" * 50)
    print("PIPELINE concluído com sucesso")
    print("=" * 50)
