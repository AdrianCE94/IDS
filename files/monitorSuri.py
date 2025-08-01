import os
import requests
from datetime import datetime
from pathlib import Path
import time

# 📌 Configuración
LOG_FILE = Path("/var/log/suricata/fast.log")
MENSAJE_LOG_DIR = Path("/var/log/suricata")
BACKUP_DIR = Path("/var/log/suricata/copias_fast")

TELEGRAM_BOT_TOKEN = "TOKEN_TELEGRAM_BOT"
CHAT_ID = "-CHAT_ID"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"

def obtener_ultimas_alertas():
    """Lee el contenido del log de Suricata"""
    try:
        with open(LOG_FILE, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"❌ Error: El archivo {LOG_FILE} no existe.")
        return []
    except Exception as e:
        print(f"❌ Error al leer el archivo {LOG_FILE}: {e}")
        return []

def enviar_alerta(mensaje):
    """Envía el mensaje a Telegram"""
    try:
        # Crear un archivo de alerta con un timestamp para evitar sobrescribir
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mensaje_log = MENSAJE_LOG_DIR / f"Alerta_{timestamp}.txt"

        with open(mensaje_log, "w") as f:
            f.writelines(mensaje)

        with open(mensaje_log, "rb") as file:
            response = requests.post(
                TELEGRAM_URL,
                data={"chat_id": CHAT_ID, "caption": "🚨 Nuevas alertas de Suricata"},
                files={"document": file}
            )
            if response.status_code == 200:
                print("✅ Alerta enviada correctamente a Telegram.")
            else:
                print(f"❌ Error al enviar la alerta a Telegram: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error al enviar la alerta: {e}")

def hacer_backup():
    """Copia el log y lo limpia"""
    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)  # Crear el directorio de backup si no existe
        # Usar timestamp completo para evitar sobrescribir backups anteriores
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        backup_file = BACKUP_DIR / f"copia.{fecha_actual}.log"

        # Copiar el archivo de log
        with open(LOG_FILE, "r") as origen, open(backup_file, "w") as destino:
            destino.write(origen.read())

        # Limpiar el archivo de log
        open(LOG_FILE, "w").close()
        print(f"✅ Backup realizado y log limpiado: {backup_file}")
    except Exception as e:
        print(f"❌ Error al hacer el backup: {e}")

def main():
    print("🔍 Iniciando monitorización del archivo .log...")
    while True:
        print("🔍 Buscando nuevas alertas...")
        alertas = obtener_ultimas_alertas()
        if alertas:
            print(f"🚨 Se encontraron {len(alertas)} nuevas alertas.")
            enviar_alerta(alertas)
            hacer_backup()
        else:
            print("🔍 No hay nuevas alertas.")
        time.sleep(60)  # Esperar 60 segundos antes de la siguiente verificación

if __name__ == "__main__":
    main()