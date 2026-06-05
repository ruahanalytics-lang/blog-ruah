import subprocess
import sys
from datetime import datetime


def run(cmd: list, check=True):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"[ERRO] {' '.join(cmd)}")
        print(result.stderr)
        sys.exit(1)
    return result


def publicar():
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    print("[+] Adicionando arquivos ao git...")
    run(["git", "add", "."])

    status = run(["git", "status", "--porcelain"], check=False)
    if not status.stdout.strip():
        print("[!] Nenhuma alteração para publicar.")
        return

    print("[+] Criando commit...")
    run(["git", "commit", "-m", f"blog: novo artigo {data}"])

    print("[+] Publicando no GitHub Pages...")
    run(["git", "push", "origin", "main"])

    print(f"\n✓ Publicado em https://blog.ruahanalytics.com")


if __name__ == "__main__":
    publicar()
