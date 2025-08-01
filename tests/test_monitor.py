import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tempfile
import builtins
import types

import pytest

from files.monitor_watchdog import leer_alertas, hacer_backup, enviar_telegram


class DummyResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code

    def json(self):
        return {}


def test_leer_alertas(tmp_path):
    log = tmp_path / "fast.log"
    log.write_text("alert1\nalert2")
    lines = leer_alertas(log)
    assert lines == ["alert1\n", "alert2"]


def test_hacer_backup(tmp_path):
    log = tmp_path / "fast.log"
    log.write_text("line")
    backup_dir = tmp_path / "bk"
    backup_file = hacer_backup(log, backup_dir)
    assert backup_file.exists()
    assert backup_file.read_text() == "line"
    assert log.read_text() == ""


def test_enviar_telegram(monkeypatch, tmp_path):
    recorded = {}

    def fake_post(url, data=None, files=None, timeout=None):
        recorded['url'] = url
        recorded['data'] = data
        recorded['files'] = files
        return DummyResponse()

    monkeypatch.setattr('requests.post', fake_post)
    log_content = ["alert"]
    enviar_telegram(log_content, 'token', 'chat')

    assert recorded['data']['chat_id'] == 'chat'
    assert 'https://api.telegram.org/bottoken/sendDocument' == recorded['url']

