# updater.py
import requests
import json
import threading
from packaging.version import Version, InvalidVersion
from PyQt6.QtCore import QObject, pyqtSignal


class UpdateChecker(QObject):
    update_found = pyqtSignal(str, str)  # version, url

    def __init__(self, current_version="1.2"):
        super().__init__()
        self.current_version = current_version
        self._stop = False

    def check_async(self):
        """Запуск проверки в фоновом потоке"""
        thread = threading.Thread(target=self._check, daemon=True)
        thread.start()

    def _check(self):
        try:
            # Используем GitHub API без токена (60 запросов в час)
            url = "https://api.github.com/repos/XxMoonmenxX/Chitalka-pisalka/releases/latest"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("tag_name", "").lstrip('v')
                download_url = data.get("html_url", "")

                if self._is_newer(latest_version):
                    self.update_found.emit(latest_version, download_url)

        except (requests.ConnectionError, requests.Timeout, json.JSONDecodeError):
            # Тихая ошибка - просто игнорируем
            pass
        except Exception as e:
            # Логируем если надо
            print(f"[Updater] Error: {e}")

    def _is_newer(self, latest: str) -> bool:
        try:
            return Version(latest) > Version(self.current_version)
        except InvalidVersion:
            return False
