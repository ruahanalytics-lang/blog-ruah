"""
daemon.py — roda em segundo plano e executa o pipeline todo dia às 08:00.
Inicia automaticamente com o Windows via pasta Startup.
"""
import schedule
import time
import subprocess
import sys
import logging
from pathlib import Path

ROOT = Path(__file__).parent
LOG = ROOT / "daemon.log"

logging.basicConfig(
    filename=str(LOG),
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def rodar_pipeline():
    logging.info("Iniciando pipeline...")
    result = subprocess.run(
        [sys.executable, str(ROOT / "pipeline.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        logging.info("Pipeline concluído com sucesso.")
    else:
        logging.error(f"Pipeline falhou:\n{result.stderr}")


schedule.every().day.at("08:00").do(rodar_pipeline)

logging.info("Daemon iniciado. Pipeline agendado para 08:00 diariamente.")

while True:
    schedule.run_pending()
    time.sleep(30)
