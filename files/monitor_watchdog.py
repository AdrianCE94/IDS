#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import yaml
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

CONFIG_PATH = Path(__file__).resolve().parent.parent / 'config.yaml'


def load_config(path=CONFIG_PATH):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def leer_alertas(log_file):
    if log_file.exists() and log_file.stat().st_size > 0:
        with open(log_file, 'r') as f:
            return f.readlines()
    return []


def enviar_telegram(alertas, token, chat_id):
    telegram_url = f"https://api.telegram.org/bot{token}/sendDocument"
    nombre = f"alerta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    tmp_path = Path('/tmp') / nombre
    with open(tmp_path, 'w') as f:
        f.writelines(alertas)
    with open(tmp_path, 'rb') as f:
        requests.post(
            telegram_url,
            data={'chat_id': chat_id, 'caption': '🚨 Nuevas alertas de Suricata'},
            files={'document': f},
            timeout=10,
        )
    tmp_path.unlink(missing_ok=True)


def hacer_backup(log_file, backup_dir):
    backup_dir.mkdir(parents=True, exist_ok=True)
    fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f"backup_{fecha}.log"
    with open(log_file, 'r') as src, open(backup_file, 'w') as dst:
        dst.write(src.read())
    open(log_file, 'w').close()
    return backup_file




class LogHandler(FileSystemEventHandler):
    def __init__(self, log_file, token, chat_id, backup_dir):
        super().__init__()
        self.log_file = log_file
        self.token = token
        self.chat_id = chat_id
        self.backup_dir = backup_dir

    def on_modified(self, event):
        if Path(event.src_path) == self.log_file:
            alertas = leer_alertas(self.log_file)
            if alertas:
                enviar_telegram(alertas, self.token, self.chat_id)
                hacer_backup(self.log_file, self.backup_dir)


def main():
    cfg = load_config()
    log_file = Path(cfg['log_file'])
    backup_dir = Path(cfg['backup_dir'])
    token = cfg['telegram_token']
    chat_id = cfg['chat_id']

    handler = LogHandler(log_file, token, chat_id, backup_dir)
    observer = Observer()
    observer.schedule(handler, log_file.parent.as_posix(), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
