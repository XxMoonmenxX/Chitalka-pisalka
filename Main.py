"""
📚 Писалка-читалка - PYQT6 EDITION
Версия: 1.2
"""

import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import os

from utils import find_icon, excepthook, ICON_PATH
from u_i import MainWindow
from config import Config

# === Обработчик исключений ===
sys.excepthook = excepthook

# === ЗАПУСК ===
if __name__ == '__main__':
    # Ищем иконку сразу
    find_icon()

    app = QApplication(sys.argv)
    app.setApplicationName("Читалка-писалка Pro")
    app.setOrganizationName("ChitalkaPisalka")

    # === УСТАНОВКА ИКОНКИ ===
    icon_loaded = False

    # Способ 1: Используем найденный путь
    if ICON_PATH and os.path.exists(ICON_PATH):
        app.setWindowIcon(QIcon(ICON_PATH))
        icon_loaded = True
        print(f"DEBUG: Icon loaded from ICON_PATH: {ICON_PATH}")

    # Способ 2: Пробуем загрузить из ресурсов Qt
    if not icon_loaded:
        try:
            icon = QIcon(":/icon.ico")  # Qt resource system
            if not icon.isNull():
                app.setWindowIcon(icon)
                icon_loaded = True
                print("DEBUG: Icon loaded from Qt resources")
        except:
            pass

    # Способ 3: Пробуем из текущей директории
    if not icon_loaded:
        local_icon = os.path.join(os.getcwd(), "icon.ico")
        if os.path.exists(local_icon):
            app.setWindowIcon(QIcon(local_icon))
            icon_loaded = True
            print(f"DEBUG: Icon loaded from current dir: {local_icon}")

    # Для Windows: устанавливаем ID приложения
    if sys.platform == 'win32':
        try:
            myappid = 'chitalkapisalka.pro.writer.1.1'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            print("DEBUG: AppUserModelID set")
        except Exception as e:
            print(f"DEBUG: Failed to set AppUserModelID: {e}")

    if not icon_loaded:
        print("DEBUG: WARNING - Icon not loaded!")

    window = MainWindow(Config)

    # Устанавливаем иконку для окна ещё раз
    if icon_loaded and ICON_PATH:
        window.setWindowIcon(QIcon(ICON_PATH))

    window.show()
    sys.exit(app.exec())
