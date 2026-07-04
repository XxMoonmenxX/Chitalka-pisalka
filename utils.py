import sys
import os

# Глобальная переменная для пути к иконке
ICON_PATH = None

def resource_path(relative_path):
    """Получить абсолютный путь к ресурсу"""
    try:
        # PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        try:
            # Nuitka
            base_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            # Обычный запуск
            base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)

    # Отладка
    print(
        f"DEBUG resource_path: base={base_path}, relative={relative_path}, full={full_path}, exists={os.path.exists(full_path)}")

    return full_path


def find_icon():
    """Поиск иконки в разных местах"""
    global ICON_PATH

    # Возможные пути к иконке (используем resource_path!)
    possible_paths = [
        resource_path("icon.ico"),  # Основной способ через resource_path
        "icon.ico",  # Текущая директория
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico"),  # Рядом со скриптом
        os.path.join(os.path.dirname(sys.executable), "icon.ico"),  # Рядом с exe
    ]

    # Добавляем PyInstaller путь если есть
    if hasattr(sys, '_MEIPASS'):
        possible_paths.append(os.path.join(sys._MEIPASS, "icon.ico"))

    for path in possible_paths:
        if path and os.path.exists(path):
            ICON_PATH = path
            print(f"DEBUG: Icon found at: {path}")
            return path

    print("DEBUG: Icon NOT FOUND in any location!")
    print(f"DEBUG: Searched paths: {possible_paths}")
    return None

def excepthook(exc_type, exc_value, exc_traceback):
    """Глобальный обработчик исключений"""
    from traceback import print_exception
    print_exception(exc_type, exc_value, exc_traceback)
    sys.__excepthook__(exc_type, exc_value, exc_traceback)
