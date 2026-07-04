#!/usr/bin/env python3
# build.py - ОПТИМИЗИРОВАННАЯ СБОРКА ДЛЯ Chitalka-pisalka

import os
import sys
import subprocess
import shutil
import json


def clean_build():
    """Очистка старых файлов сборки"""
    dirs_to_clean = [
        'build', 'Chitalka-pisalka.dist', 'Chitalka-pisalka.onefile-build',
        '__pycache__', 'Chitalka-pisalka.build'
    ]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🗑 Удаляем {dir_name}...")
            try:
                shutil.rmtree(dir_name)
            except Exception as e:
                print(f"   Не удалось удалить {dir_name}: {e}")

    for file in ['Chitalka-pisalka.exe', 'Chitalka-pisalka.debug.exe']:
        if os.path.exists(file):
            print(f"🗑 Удаляем {file}...")
            try:
                os.remove(file)
            except Exception as e:
                print(f"   Не удалось удалить {file}: {e}")

    print("✅ Очистка завершена\n")


def check_dependencies():
    """Проверка установленных зависимостей"""
    required = {
        'PyQt6': 'PyQt6',
        'requests': 'requests',
        'packaging': 'packaging',
    }

    optional = {
        'docx': 'python-docx',
        'PyPDF2': 'PyPDF2',
        'PIL': 'Pillow',
        'lxml': 'lxml',
        'PyQt6.QtPdf': 'PyQt6-Pdf',
        'PyQt6.QtPdfWidgets': 'PyQt6-Pdf',
    }

    print("📦 Проверка зависимостей:")
    print("  Обязательные:")
    for module, package in required.items():
        try:
            __import__(module)
            print(f"    ✅ {package}")
        except ImportError:
            print(f"    ❌ {package} - НЕ УСТАНОВЛЕН!")
            return False

    print("  Опциональные (для расширенных функций):")
    for module, package in optional.items():
        try:
            __import__(module)
            print(f"    ✅ {package}")
        except ImportError:
            print(f"    ⚠️  {package} - не установлен (некоторые функции будут ограничены)")

    print()
    return True


def ensure_icon():
    """Проверяем наличие иконки"""
    icon_paths = [
        "icon.ico",
        os.path.join(os.path.dirname(__file__), "icon.ico"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico"),
        os.path.join(os.getcwd(), "icon.ico")
    ]

    for path in icon_paths:
        if os.path.exists(path):
            print(f"✅ Иконка найдена: {path}")
            return path

    print("❌ Иконка не найдена! Убедитесь, что icon.ico есть в папке проекта.")
    return None


def build_optimized():
    """Максимально оптимизированная сборка для Chitalka-pisalka"""

    print("=" * 70)
    print("🚀 СБОРКА Chitalka-pisalka Pro (Nuitka Optimized)")
    print("=" * 70)
    print()

    # Проверяем зависимости
    if not check_dependencies():
        print("\n⚠️  Установите недостающие зависимости:")
        print("   pip install -r requirements.txt")
        return False

    # Проверяем иконку
    icon_path = ensure_icon()
    if not icon_path:
        print("\n⚠️  Сборка будет выполнена без иконки")

    cpu_count = os.cpu_count() or 4
    print(f"💻 Обнаружено ядер CPU: {cpu_count}")
    print()

    # Базовые параметры
    cmd = [
        sys.executable, "-m", "nuitka",

        # === Базовые настройки ===
        "--standalone",
        "--onefile",
        "--enable-plugin=pyqt6",

        # === ОПТИМИЗАЦИЯ ПРОИЗВОДИТЕЛЬНОСТИ ===
        "--lto=yes",
        "--jobs=" + str(cpu_count),
        "--python-flag=no_warnings",
        "--python-flag=no_asserts",

        # === ОПТИМИЗАЦИЯ РАЗМЕРА ===
        "--remove-output",
        "--no-debug",

        # === НАСТРОЙКИ Windows ===
        "--windows-console-mode=disable",
        "--windows-file-version=1.3.0",
        "--windows-product-version=1.3.0",
        "--file-description=Chitalka-pisalka Professional",
        "--product-name=Chitalka-pisalka",

        # === МЕТАДАННЫЕ ===
        "--copyright=Copyright 2024 XxMoonmenxX",
        "--company-name=MoonmenStudio",

        # === ИКОНКА ===
        f"--windows-icon-from-ico={icon_path}" if icon_path else "",

        # === ВКЛЮЧАЕМ НЕОБХОДИМЫЕ МОДУЛИ ===
        "--include-package=PyQt6",
        "--include-package=PyQt6.QtCore",
        "--include-package=PyQt6.QtGui",
        "--include-package=PyQt6.QtWidgets",
        "--include-package=PyQt6.QtPrintSupport",
        "--include-module=xml.etree.ElementTree",
        "--include-module=xml.dom.minidom",
        "--include-module=requests",
        "--include-module=packaging",

        # === ОПЦИОНАЛЬНЫЕ МОДУЛИ (если установлены) ===
        "--include-module=docx" if _module_installed('docx') else "",
        "--include-module=PyPDF2" if _module_installed('PyPDF2') else "",
        "--include-module=PIL" if _module_installed('PIL') else "",
        "--include-module=lxml" if _module_installed('lxml') else "",
        "--include-module=PyQt6.QtPdf" if _module_installed('PyQt6.QtPdf') else "",
        "--include-module=PyQt6.QtPdfWidgets" if _module_installed('PyQt6.QtPdfWidgets') else "",

        # === ВЫКЛЮЧАЕМ НЕНУЖНОЕ ===
        "--nofollow-import-to=unittest",
        "--nofollow-import-to=pdb",
        "--nofollow-import-to=doctest",
        "--nofollow-import-to=tkinter",
        "--nofollow-import-to=ctypes",
        "--nofollow-import-to=multiprocessing",

        # === ВИЗУАЛИЗАЦИЯ ===
        "--show-progress",

        # === ВЫХОДНОЙ ФАЙЛ ===
        "--output-filename=Chitalka-pisalka.exe",

        "Polet_Fantasij.py"
    ]

    # Убираем пустые аргументы
    cmd = [arg for arg in cmd if arg]

    print("📦 Параметры оптимизации:")
    print("   • LTO (Link Time Optimization): Включена")
    print(f"   • Параллельная сборка: {cpu_count} потоков")
    print("   • Ассерты: Выключены")
    print("   • Предупреждения: Выключены")
    print("   • Отладка: Выключена")
    if icon_path:
        print("   • Иконка: Включена")
    print()
    print("⏳ Начинаю компиляцию...")
    print("   (Обычно 10-20 минут, в зависимости от мощности)")
    print()

    try:
        result = subprocess.run(cmd, check=False)

        if result.returncode == 0:
            print()
            print("=" * 70)
            print("✅ СБОРКА УСПЕШНО ЗАВЕРШЕНА!")
            print("=" * 70)
            print()

            if os.path.exists('Chitalka-pisalka.exe'):
                size = os.path.getsize('Chitalka-pisalka.exe')
                size_mb = size / (1024 * 1024)
                print(f"📁 Файл: {os.path.abspath('Chitalka-pisalka.exe')}")
                print(f"📏 Размер: {size_mb:.2f} MB")
                print()
                print("🎉 Программа готова! Просто запустите Chitalka-pisalka.exe")
                return True
            else:
                print("❌ Файл не найден после сборки!")
                return False

        else:
            print(f"❌ Ошибка сборки с кодом: {result.returncode}")
            print("\nПробуем совместимую сборку...")
            return build_compatibility()

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return build_compatibility()


def _module_installed(module_name: str) -> bool:
    """Проверка установки модуля"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def build_compatibility():
    """Совместимая сборка (без LTO и агрессивной оптимизации)"""

    print("🔧 СОВМЕСТИМАЯ СБОРКА")
    print()

    icon_path = ensure_icon()

    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=pyqt6",
        "--windows-console-mode=disable",
        "--jobs=" + str(os.cpu_count() or 4),
        "--include-package=PyQt6",
        "--include-module=requests",
        "--include-module=packaging",
        f"--windows-icon-from-ico={icon_path}" if icon_path else "",
        "--output-filename=Chitalka-pisalka.exe",
        "Polet_Fantasij.py"
    ]

    cmd = [arg for arg in cmd if arg]
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n✅ Совместимая сборка завершена!")
        return True
    return False


def build_fast():
    """Быстрая сборка (для тестирования)"""

    print("⚡ БЫСТРАЯ СБОРКА (для тестирования)")
    print()

    icon_path = ensure_icon()

    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=pyqt6",
        "--windows-console-mode=disable",
        "--jobs=" + str(os.cpu_count() or 4),
        "--include-package=PyQt6",
        f"--windows-icon-from-ico={icon_path}" if icon_path else "",
        "--output-filename=Chitalka-pisalka.exe",
        "Polet_Fantasij.py"
    ]

    cmd = [arg for arg in cmd if arg]
    subprocess.run(cmd)


def create_requirements():
    """Создает requirements.txt если его нет"""
    requirements = """PyQt6>=6.4.0
PyQt6-Pdf>=6.4.0
Pillow>=9.0.0
lxml>=4.9.0
python-docx>=0.8.11
PyPDF2>=3.0.0
requests>=2.28.0
packaging>=21.3
nuitka>=2.0.0
zstandard>=0.19.0
"""
    if not os.path.exists('requirements.txt'):
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write(requirements)
        print("✅ Создан requirements.txt")
    else:
        print("ℹ️  requirements.txt уже существует")


def show_version():
    """Показывает версию программы"""
    print("📚 Chitalka-pisalka Pro v1.3")
    print("Сборщик для Nuitka")
    print()


if __name__ == "__main__":
    print()
    print("🎮 СБОРЩИК Chitalka-pisalka Pro (Nuitka)")
    print()

    # Проверяем наличие requirements.txt
    create_requirements()
    print()

    print("Выберите режим сборки:")
    print("1. 🚀 МАКСИМАЛЬНАЯ ОПТИМИЗАЦИЯ (рекомендуется)")
    print("2. ⚡ Быстрая сборка (для тестирования)")
    print("3. 🔧 Совместимая сборка (если другие не работают)")
    print("4. 🧹 Только очистка")
    print("5. 📦 Установить зависимости")
    print("6. ℹ️  Информация о версии")
    print()

    choice = input("Ваш выбор (1-6) [по умолчанию 1]: ").strip()

    if choice == "2":
        clean_build()
        build_fast()
    elif choice == "3":
        clean_build()
        build_compatibility()
    elif choice == "4":
        clean_build()
    elif choice == "5":
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
    elif choice == "6":
        show_version()
    else:
        clean_build()
        build_optimized()
