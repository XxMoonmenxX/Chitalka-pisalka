# updater.py
import requests
import json
import threading
from packaging.version import Version, InvalidVersion
from PyQt6.QtCore import QObject, pyqtSignal


class UpdateChecker(QObject):
    update_found = pyqtSignal(str, str)

    def __init__(self, current_version="1.2"):
        super().__init__()
        self.current_version = current_version
        self._stop = False

    def check_async(self):
        thread = threading.Thread(target=self._check, daemon=True)
        thread.start()

    def _check(self):
        try:
            print(f"[Updater] Проверка для версии {self.current_version}")

            url = "https://api.github.com/repos/XxMoonmenxX/Chitalka-pisalka/releases/latest"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("tag_name", "").lstrip('v')
                download_url = data.get("html_url", "")

                print(f"[Updater] Получена версия: {latest_version}")

                if self._is_newer(latest_version):
                    print("[Updater] Есть обновление!")
                    self.update_found.emit(latest_version, download_url)
                else:
                    print("[Updater] Обновление не требуется")

            else:
                print(f"[Updater] Ошибка GitHub API: {response.status_code}")

                # Fallback: пробуем получить все релизы
                print("[Updater] Fallback: пробуем список релизов...")
                url_all = "https://api.github.com/repos/XxMoonmenxX/Chitalka-pisalka/releases"
                resp2 = requests.get(url_all, timeout=5)
                if resp2.status_code == 200:
                    releases = resp2.json()
                    if releases:
                        latest = releases[0]
                        latest_version = latest.get("tag_name", "").lstrip('v')
                        download_url = latest.get("html_url", "")
                        print(f"[Updater] Fallback: {latest_version}")
                        if self._is_newer(latest_version):
                            print("[Updater] Fallback: есть обновление!")
                            self.update_found.emit(latest_version, download_url)
                        else:
                            print("[Updater] Fallback: обновление не требуется")

        except Exception as e:
            print(f"[Updater] Ошибка: {e}")
            import traceback
            traceback.print_exc()

    def _is_newer(self, latest: str) -> bool:
        try:
            clean_latest = latest.lstrip('v')
            clean_current = self.current_version.lstrip('v')
            print(f"[Updater] Сравнение: {clean_current} vs {clean_latest}")
            return Version(clean_latest) > Version(clean_current)
        except InvalidVersion as e:
            print(f"[Updater] Ошибка версии: {e}")
            return False
