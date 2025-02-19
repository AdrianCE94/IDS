#!/usr/bin/env python3

import os
import requests
from datetime import datetime
import time
from pathlib import Path
import logging

# Configuración de logging con emojis
class EmojiFormatter(logging.Formatter):
    def format(self, record):
        # Añadir emojis según el nivel del mensaje
        if record.levelno == logging.INFO:
            record.msg = f"🔍 {record.msg}"
        elif record.levelno == logging.ERROR:
            record.msg = f"❌ {record.msg}"
        elif record.levelno == logging.WARNING:
            record.msg = f"⚠️ {record.msg}"
        return super().format(record)

# Configurar logging
logger = logging.getLogger('SuricataMonitor')
logger.setLevel(logging.INFO)

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(EmojiFormatter('%(message)s'))
logger.addHandler(console_handler)

# Configuración básica
RUTA_LOG = Path("/var/log/suricata/fast.log")
RUTA_BACKUP = Path("/var/log/suricata/backups")
RUTA_BACKUP.mkdir(parents=True, exist_ok=True)

# Configuración de Telegram
TOKEN = "TU_TOKEN_AQUI"
CHAT_ID = "TU_CHAT_ID_AQUI"
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendDocument"

def leer_alertas():
    """Lee el archivo de log de Suricata"""
    try:
        if RUTA_LOG.exists() and RUTA_LOG.stat().st_size > 0:
            with open(RUTA_LOG, "r") as f:
                return f.readlines()
        return []
    except Exception as e:
        logger.error(f"Error leyendo alertas: {e}")
        return []

def enviar_telegram(alertas):
    """Envía alertas a Telegram"""
    try:
        # Crear archivo temporal con timestamp
        nombre_archivo = f"alerta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        ruta_alerta = RUTA_BACKUP / nombre_archivo

        # Guardar alertas
        with open(ruta_alerta, "w") as f:
            f.writelines(alertas)

        # Enviar a Telegram
        with open(ruta_alerta, "rb") as f:
            respuesta = requests.post(
                TELEGRAM_URL,
                data={"chat_id": CHAT_ID, "caption": "🚨 Nuevas alertas de Suricata"},
                files={"document": f}
            )

        if respuesta.status_code == 200:
            logger.info("Alerta enviada correctamente")
        else:
            logger.error(f"Error enviando alerta: {respuesta.status_code}")

    except Exception as e:
        logger.error(f"Error en el envío: {e}")

def hacer_backup():
    """Realiza backup del log y lo limpia"""
    try:
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_backup = RUTA_BACKUP / f"backup_{fecha}.log"

        # Copiar contenido
        with open(RUTA_LOG, "r") as origen, open(archivo_backup, "w") as destino:
            destino.write(origen.read())

        # Limpiar archivo original
        open(RUTA_LOG, "w").close()
        logger.info(f"✅ Backup realizado: {archivo_backup}")

    except Exception as e:
        logger.error(f"Error en backup: {e}")

def main():
    logger.info("🚀 Iniciando monitor de Suricata...")

    while True:
        try:
            logger.info("Buscando nuevas alertas...")
            alertas = leer_alertas()

            if alertas:
                logger.info(f"🚨 {len(alertas)} nuevas alertas encontradas")
                enviar_telegram(alertas)
                hacer_backup()
            else:
                logger.info("Sin alertas nuevas")

            time.sleep(60)

        except KeyboardInterrupt:
            logger.info("👋 Deteniendo monitor...")
            break
        except Exception as e:
            logger.error(f"Error en ciclo principal: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
