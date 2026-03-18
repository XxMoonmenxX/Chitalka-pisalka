"""
📚 Писалка-читалка - PYQT6 EDITION
Версия: 1.0
"""

import sys
import os
import json
import uuid
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import xml.dom.minidom
import base64

# === PyQt6 импорты ===
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtCore import pyqtSignal

# === Обработчик исключений ===
def excepthook(exc_type, exc_value, exc_traceback):
    """Глобальный обработчик исключений"""
    from traceback import print_exception
    print_exception(exc_type, exc_value, exc_traceback)
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = excepthook

# === КОНФИГУРАЦИЯ ===
class Config:
    APP_DIR = os.path.join(os.path.expanduser('~'), '.chitalkapisalka')
    PROJECTS_DIR = os.path.join(APP_DIR, 'projects')
    BACKUP_DIR = os.path.join(APP_DIR, 'backups')
    TEMPLATES_DIR = os.path.join(APP_DIR, 'templates')
    PLUGINS_DIR = os.path.join(APP_DIR, 'plugins')
    CONFIG_FILE = os.path.join(APP_DIR, 'config.json')
    RECENT_FILE = os.path.join(APP_DIR, 'recent.json')
    COVERS_DIR = os.path.join(APP_DIR, 'covers')  # Новая директория для кэша обложек

    @classmethod
    def init_dirs(cls):
        for d in [cls.APP_DIR, cls.PROJECTS_DIR, cls.BACKUP_DIR,
                  cls.TEMPLATES_DIR, cls.PLUGINS_DIR, cls.COVERS_DIR]:
            try:
                os.makedirs(d, exist_ok=True)
            except Exception as e:
                print(f"Ошибка создания директории {d}: {e}")

    @classmethod
    def sanitize_folder_name(cls, name: str) -> str:
        """Очищает имя папки от недопустимых символов"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        name = name.rstrip('.')
        name = name.strip()
        if not name or name == '.' * len(name):
            name = 'Новый_проект'
        return name

# === СИСТЕМА ТЕМ ===
class Theme:
    """Класс для работы с темами оформления"""
    # ... (весь класс Theme остается без изменений)
    THEMES = {
        'dark': {
            'name': 'Тёмная',
            'window_bg': '#2b2b2b',
            'window_fg': '#ffffff',
            'menu_bg': '#3c3c3c',
            'menu_fg': '#ffffff',
            'menu_selected': '#505050',
            'toolbar_bg': '#3c3c3c',
            'dock_bg': '#2b2b2b',
            'dock_title_bg': '#3c3c3c',
            'dock_title_fg': '#ffffff',
            'tree_bg': '#2b2b2b',
            'tree_fg': '#ffffff',
            'tree_alternate': '#323232',
            'list_bg': '#2b2b2b',
            'list_fg': '#ffffff',
            'list_alternate': '#323232',
            'editor_bg': '#1e1e1e',
            'editor_fg': '#d4d4d4',
            'editor_selection': '#264f78',
            'editor_line_highlight': '#2a2d2e',
            'button_bg': '#505050',
            'button_fg': '#ffffff',
            'button_hover': '#606060',
            'button_pressed': '#404040',
            'input_bg': '#3c3c3c',
            'input_fg': '#ffffff',
            'input_border': '#505050',
            'input_focus_border': '#0078d4',
            'status_bar_bg': '#007acc',
            'status_bar_fg': '#ffffff',
            'scrollbar_bg': '#3c3c3c',
            'scrollbar_handle': '#606060',
            'scrollbar_handle_hover': '#707070',
            'border_color': '#505050',
            'separator_color': '#404040',
            'highlight_color': '#0078d4',
            'error_color': '#f48771',
            'success_color': '#6a9955',
            'warning_color': '#dcdcaa'
        },
        'light': {
            'name': 'Светлая',
            'window_bg': '#f0f0f0',
            'window_fg': '#000000',
            'menu_bg': '#ffffff',
            'menu_fg': '#000000',
            'menu_selected': '#e5f3ff',
            'toolbar_bg': '#ffffff',
            'dock_bg': '#f0f0f0',
            'dock_title_bg': '#ffffff',
            'dock_title_fg': '#000000',
            'tree_bg': '#ffffff',
            'tree_fg': '#000000',
            'tree_alternate': '#f5f5f5',
            'list_bg': '#ffffff',
            'list_fg': '#000000',
            'list_alternate': '#f5f5f5',
            'editor_bg': '#ffffff',
            'editor_fg': '#000000',
            'editor_selection': '#add6ff',
            'editor_line_highlight': '#f0f0f0',
            'button_bg': '#ffffff',
            'button_fg': '#000000',
            'button_hover': '#f0f0f0',
            'button_pressed': '#e0e0e0',
            'input_bg': '#ffffff',
            'input_fg': '#000000',
            'input_border': '#cccccc',
            'input_focus_border': '#0078d4',
            'status_bar_bg': '#0078d4',
            'status_bar_fg': '#ffffff',
            'scrollbar_bg': '#f0f0f0',
            'scrollbar_handle': '#c0c0c0',
            'scrollbar_handle_hover': '#a0a0a0',
            'border_color': '#cccccc',
            'separator_color': '#e0e0e0',
            'highlight_color': '#0078d4',
            'error_color': '#f44336',
            'success_color': '#4caf50',
            'warning_color': '#ff9800'
        },
        'sepia': {
            'name': 'Сепия',
            'window_bg': '#fbf0d9',
            'window_fg': '#5f4b3b',
            'menu_bg': '#f5e6d3',
            'menu_fg': '#5f4b3b',
            'menu_selected': '#e6d7c0',
            'toolbar_bg': '#f5e6d3',
            'dock_bg': '#fbf0d9',
            'dock_title_bg': '#f5e6d3',
            'dock_title_fg': '#5f4b3b',
            'tree_bg': '#fbf0d9',
            'tree_fg': '#5f4b3b',
            'tree_alternate': '#f5e6d3',
            'list_bg': '#fbf0d9',
            'list_fg': '#5f4b3b',
            'list_alternate': '#f5e6d3',
            'editor_bg': '#fbf0d9',
            'editor_fg': '#5f4b3b',
            'editor_selection': '#e6d7c0',
            'editor_line_highlight': '#f5e6d3',
            'button_bg': '#e6d7c0',
            'button_fg': '#5f4b3b',
            'button_hover': '#d6c7b0',
            'button_pressed': '#c6b7a0',
            'input_bg': '#ffffff',
            'input_fg': '#5f4b3b',
            'input_border': '#d6c7b0',
            'input_focus_border': '#8b6b4f',
            'status_bar_bg': '#8b6b4f',
            'status_bar_fg': '#ffffff',
            'scrollbar_bg': '#f5e6d3',
            'scrollbar_handle': '#c6b7a0',
            'scrollbar_handle_hover': '#b6a790',
            'border_color': '#d6c7b0',
            'separator_color': '#e6d7c0',
            'highlight_color': '#8b6b4f',
            'error_color': '#b34a4a',
            'success_color': '#5f8b5f',
            'warning_color': '#cc8b4a'
        },
        'dracula': {
            'name': 'Дракула',
            'window_bg': '#282a36',
            'window_fg': '#f8f8f2',
            'menu_bg': '#44475a',
            'menu_fg': '#f8f8f2',
            'menu_selected': '#6272a4',
            'toolbar_bg': '#44475a',
            'dock_bg': '#282a36',
            'dock_title_bg': '#44475a',
            'dock_title_fg': '#f8f8f2',
            'tree_bg': '#282a36',
            'tree_fg': '#f8f8f2',
            'tree_alternate': '#343746',
            'list_bg': '#282a36',
            'list_fg': '#f8f8f2',
            'list_alternate': '#343746',
            'editor_bg': '#282a36',
            'editor_fg': '#f8f8f2',
            'editor_selection': '#44475a',
            'editor_line_highlight': '#343746',
            'button_bg': '#44475a',
            'button_fg': '#f8f8f2',
            'button_hover': '#6272a4',
            'button_pressed': '#50fa7b',
            'input_bg': '#44475a',
            'input_fg': '#f8f8f2',
            'input_border': '#6272a4',
            'input_focus_border': '#bd93f9',
            'status_bar_bg': '#bd93f9',
            'status_bar_fg': '#282a36',
            'scrollbar_bg': '#44475a',
            'scrollbar_handle': '#6272a4',
            'scrollbar_handle_hover': '#ff79c6',
            'border_color': '#6272a4',
            'separator_color': '#44475a',
            'highlight_color': '#bd93f9',
            'error_color': '#ff5555',
            'success_color': '#50fa7b',
            'warning_color': '#ffb86c'
        },
        'monokai': {
            'name': 'Monokai',
            'window_bg': '#272822',
            'window_fg': '#f8f8f2',
            'menu_bg': '#3e3d32',
            'menu_fg': '#f8f8f2',
            'menu_selected': '#75715e',
            'toolbar_bg': '#3e3d32',
            'dock_bg': '#272822',
            'dock_title_bg': '#3e3d32',
            'dock_title_fg': '#f8f8f2',
            'tree_bg': '#272822',
            'tree_fg': '#f8f8f2',
            'tree_alternate': '#2d2e27',
            'list_bg': '#272822',
            'list_fg': '#f8f8f2',
            'list_alternate': '#2d2e27',
            'editor_bg': '#272822',
            'editor_fg': '#f8f8f2',
            'editor_selection': '#49483e',
            'editor_line_highlight': '#2d2e27',
            'button_bg': '#49483e',
            'button_fg': '#f8f8f2',
            'button_hover': '#75715e',
            'button_pressed': '#a6e22e',
            'input_bg': '#3e3d32',
            'input_fg': '#f8f8f2',
            'input_border': '#75715e',
            'input_focus_border': '#66d9ef',
            'status_bar_bg': '#66d9ef',
            'status_bar_fg': '#272822',
            'scrollbar_bg': '#3e3d32',
            'scrollbar_handle': '#75715e',
            'scrollbar_handle_hover': '#f92672',
            'border_color': '#75715e',
            'separator_color': '#49483e',
            'highlight_color': '#a6e22e',
            'error_color': '#f92672',
            'success_color': '#a6e22e',
            'warning_color': '#fd971f'
        }
    }

    def __init__(self, theme_name='dark'):
        self.current_theme = theme_name
        self.colors = self.THEMES.get(theme_name, self.THEMES['dark']).copy()
        self.custom_colors = {}

    def get(self, key, default=''):
        """Получить значение цвета"""
        if key in self.custom_colors:
            return self.custom_colors[key]
        return self.colors.get(key, default)

    def set_custom(self, key, value):
        """Установить пользовательский цвет"""
        self.custom_colors[key] = value

    def to_dict(self):
        """Для сохранения в настройки"""
        return {
            'current_theme': self.current_theme,
            'custom_colors': self.custom_colors
        }

    @classmethod
    def from_dict(cls, data):
        """Загрузить из настроек"""
        theme = cls(data.get('current_theme', 'dark'))
        theme.custom_colors = data.get('custom_colors', {})
        return theme

    def get_stylesheet(self):
        """Сгенерировать стиль для приложения"""
        c = self.colors

        return f"""
            QMainWindow {{
                background-color: {c['window_bg']};
                color: {c['window_fg']};
            }}
            QMenuBar {{
                background-color: {c['menu_bg']};
                color: {c['menu_fg']};
                border-bottom: 1px solid {c['border_color']};
            }}
            QMenuBar::item:selected {{
                background-color: {c['menu_selected']};
            }}
            QMenu {{
                background-color: {c['menu_bg']};
                color: {c['menu_fg']};
                border: 1px solid {c['border_color']};
            }}
            QMenu::item:selected {{
                background-color: {c['menu_selected']};
            }}
            QToolBar {{
                background-color: {c['toolbar_bg']};
                border: none;
                border-bottom: 1px solid {c['border_color']};
            }}
            QDockWidget {{
                color: {c['window_fg']};
            }}
            QDockWidget::title {{
                background-color: {c['dock_title_bg']};
                color: {c['dock_title_fg']};
                padding: 5px;
                border: 1px solid {c['border_color']};
            }}
            QTreeWidget, QListWidget {{
                background-color: {c['tree_bg']};
                color: {c['tree_fg']};
                border: 1px solid {c['border_color']};
                alternate-background-color: {c['tree_alternate']};
            }}
            QTreeWidget::item:selected, QListWidget::item:selected {{
                background-color: {c['highlight_color']};
            }}
            QPlainTextEdit {{
                background-color: {c['editor_bg']};
                color: {c['editor_fg']};
                border: 1px solid {c['border_color']};
                selection-background-color: {c['editor_selection']};
            }}
            QPushButton {{
                background-color: {c['button_bg']};
                color: {c['button_fg']};
                border: 1px solid {c['border_color']};
                padding: 5px 10px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {c['button_hover']};
            }}
            QPushButton:pressed {{
                background-color: {c['button_pressed']};
            }}
            QLineEdit, QTextEdit, QComboBox, QSpinBox {{
                background-color: {c['input_bg']};
                color: {c['input_fg']};
                border: 1px solid {c['input_border']};
                padding: 3px;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 2px solid {c['input_focus_border']};
            }}
            QStatusBar {{
                background-color: {c['status_bar_bg']};
                color: {c['status_bar_fg']};
            }}
            QScrollBar:vertical {{
                background-color: {c['scrollbar_bg']};
                width: 14px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {c['scrollbar_handle']};
                min-height: 20px;
                border-radius: 7px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {c['scrollbar_handle_hover']};
            }}
            QTabBar::tab {{
                background-color: {c['menu_bg']};
                color: {c['menu_fg']};
                padding: 5px 10px;
                border: 1px solid {c['border_color']};
            }}
            QTabBar::tab:selected {{
                background-color: {c['window_bg']};
            }}
            QDialog {{
                background-color: {c['window_bg']};
                color: {c['window_fg']};
            }}
            QGroupBox {{
                border: 1px solid {c['border_color']};
                border-radius: 3px;
                margin-top: 10px;
                padding-top: 10px;
                color: {c['window_fg']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """

# === МОДЕЛЬ ДАННЫХ ===
class Chapter:
    """Глава проекта"""
    # ... (класс Chapter остается без изменений)
    def __init__(self, title: str = "", content: str = ""):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.order = 0
        self.created = datetime.now()
        self.modified = datetime.now()
        self.status = "draft"
        self.tags = []
        self.notes = ""

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'order': self.order,
            'created': self.created.isoformat(),
            'modified': self.modified.isoformat(),
            'status': self.status,
            'tags': self.tags,
            'notes': self.notes
        }

    @classmethod
    def from_dict(cls, data):
        chapter = cls(data['title'], "")
        chapter.id = data['id']
        chapter.order = data['order']
        chapter.created = datetime.fromisoformat(data['created'])
        chapter.modified = datetime.fromisoformat(data['modified'])
        chapter.status = data.get('status', 'draft')
        chapter.tags = data.get('tags', [])
        chapter.notes = data.get('notes', '')
        return chapter

    def word_count(self) -> int:
        return len(re.findall(r'\b\w+\b', self.content))

    def char_count(self) -> int:
        return len(self.content)

class Project:
    """Проект с поддержкой обложки"""

    def __init__(self, name: str, path: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.path = path
        self.chapters: List[Chapter] = []
        self.settings = {
            'author': 'Автор',
            'language': 'ru',
            'theme': 'dark',
            'auto_save': 30,
            'backup_enabled': True,
            'vim_mode': True,
            'font_size': 12,
            'font_family': 'Consolas'
        }
        self.created = datetime.now()
        self.modified = datetime.now()
        self.tags = []
        self.annotation = ""
        self.cover_path = None  # Путь к файлу обложки
        self.cover_data = None  # Данные обложки для встраивания в FB2

    def set_cover(self, image_path: str) -> bool:
        """Установить обложку из файла"""
        try:
            if not os.path.exists(image_path):
                return False

            # Создаем директорию для обложек в проекте
            covers_dir = os.path.join(self.path, 'covers')
            os.makedirs(covers_dir, exist_ok=True)

            # Копируем файл с уникальным именем
            ext = os.path.splitext(image_path)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                return False

            new_cover_name = f"cover_{uuid.uuid4().hex}{ext}"
            new_cover_path = os.path.join(covers_dir, new_cover_name)

            shutil.copy2(image_path, new_cover_path)

            # Удаляем старую обложку, если есть
            if self.cover_path and os.path.exists(self.cover_path):
                try:
                    os.remove(self.cover_path)
                except:
                    pass

            self.cover_path = new_cover_path

            # Загружаем данные обложки для FB2
            with open(self.cover_path, 'rb') as f:
                self.cover_data = base64.b64encode(f.read()).decode('utf-8')

            self.modified = datetime.now()
            return True
        except Exception as e:
            print(f"Ошибка установки обложки: {e}")
            return False

    def remove_cover(self):
        """Удалить обложку"""
        try:
            if self.cover_path and os.path.exists(self.cover_path):
                os.remove(self.cover_path)

            covers_dir = os.path.join(self.path, 'covers')
            if os.path.exists(covers_dir) and not os.listdir(covers_dir):
                os.rmdir(covers_dir)

            self.cover_path = None
            self.cover_data = None
            self.modified = datetime.now()
        except Exception as e:
            print(f"Ошибка удаления обложки: {e}")

    def get_cover_pixmap(self, max_width: int = 200, max_height: int = 300) -> Optional[QPixmap]:
        """Получить QPixmap обложки для отображения"""
        if not self.cover_path or not os.path.exists(self.cover_path):
            return None

        try:
            pixmap = QPixmap(self.cover_path)
            if not pixmap.isNull():
                return pixmap.scaled(
                    max_width, max_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
        except Exception as e:
            print(f"Ошибка загрузки обложки: {e}")
        return None

    def add_chapter(self, title: str = None, content: str = "") -> Chapter:
        """Добавить главу"""
        if not title:
            title = f"Глава {len(self.chapters) + 1}"

        chapter = Chapter(title, content)
        chapter.order = len(self.chapters)
        self.chapters.append(chapter)
        self.modified = datetime.now()
        return chapter

    def delete_chapter(self, chapter_id: str):
        """Удалить главу"""
        self.chapters = [c for c in self.chapters if c.id != chapter_id]
        for i, c in enumerate(self.chapters):
            c.order = i
        self.modified = datetime.now()

    def get_chapter(self, chapter_id: str) -> Optional[Chapter]:
        """Получить главу"""
        for c in self.chapters:
            if c.id == chapter_id:
                return c
        return None

    def update_chapter_title(self, chapter_id: str, new_title: str):
        """Обновить название главы"""
        chapter = self.get_chapter(chapter_id)
        if chapter:
            chapter.title = new_title
            chapter.modified = datetime.now()
            self.modified = datetime.now()
            return True
        return False

    def move_chapter(self, chapter_id: str, new_order: int):
        """Переместить главу"""
        chapter = self.get_chapter(chapter_id)
        if not chapter:
            return

        self.chapters.remove(chapter)
        self.chapters.insert(new_order, chapter)

        for i, c in enumerate(self.chapters):
            c.order = i

        self.modified = datetime.now()

    def save(self):
        """Сохранить проект"""
        try:
            os.makedirs(self.path, exist_ok=True)

            meta_path = os.path.join(self.path, 'project.json')
            with open(meta_path, 'w', encoding='utf-8') as f:
                # Сохраняем только относительный путь к обложке
                cover_rel_path = None
                if self.cover_path:
                    cover_rel_path = os.path.relpath(self.cover_path, self.path)

                json.dump({
                    'id': self.id,
                    'name': self.name,
                    'chapters': [c.to_dict() for c in self.chapters],
                    'settings': self.settings,
                    'created': self.created.isoformat(),
                    'modified': self.modified.isoformat(),
                    'tags': self.tags,
                    'annotation': self.annotation,
                    'cover_path': cover_rel_path  # Сохраняем относительный путь
                }, f, ensure_ascii=False, indent=2)

            chapters_dir = os.path.join(self.path, 'chapters')
            os.makedirs(chapters_dir, exist_ok=True)

            for chapter in self.chapters:
                chapter_path = os.path.join(chapters_dir, f"{chapter.id}.txt")
                with open(chapter_path, 'w', encoding='utf-8') as f:
                    f.write(chapter.content)

            if self.settings.get('backup_enabled'):
                self.create_backup()

            return True
        except Exception as e:
            print(f"Ошибка сохранения проекта: {e}")
            return False

    @classmethod
    def load(cls, path: str) -> Optional['Project']:
        """Загрузить проект"""
        try:
            meta_path = os.path.join(path, 'project.json')

            if not os.path.exists(meta_path):
                raise FileNotFoundError(f"Файл проекта не найден: {meta_path}")

            with open(meta_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            project = cls(data['name'], path)
            project.id = data['id']
            project.settings.update(data.get('settings', {}))
            project.created = datetime.fromisoformat(data['created'])
            project.modified = datetime.fromisoformat(data['modified'])
            project.tags = data.get('tags', [])
            project.annotation = data.get('annotation', '')

            # Загружаем обложку
            cover_rel_path = data.get('cover_path')
            if cover_rel_path:
                cover_full_path = os.path.join(path, cover_rel_path)
                if os.path.exists(cover_full_path):
                    project.cover_path = cover_full_path
                    # Загружаем данные для FB2
                    with open(cover_full_path, 'rb') as f:
                        project.cover_data = base64.b64encode(f.read()).decode('utf-8')

            chapters_dir = os.path.join(path, 'chapters')
            for chapter_data in data['chapters']:
                chapter = Chapter.from_dict(chapter_data)

                chapter_path = os.path.join(chapters_dir, f"{chapter.id}.txt")
                if os.path.exists(chapter_path):
                    with open(chapter_path, 'r', encoding='utf-8') as f:
                        chapter.content = f.read()

                project.chapters.append(chapter)

            project.chapters.sort(key=lambda c: c.order)

            return project
        except Exception as e:
            print(f"Ошибка загрузки проекта: {e}")
            return None

    def create_backup(self):
        """Создать бэкап"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{Config.sanitize_folder_name(self.name)}_{timestamp}.zip"
            backup_path = os.path.join(Config.BACKUP_DIR, backup_name)

            with ZipFile(backup_path, 'w') as zipf:
                for root, dirs, files in os.walk(self.path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, self.path)
                        zipf.write(file_path, arcname)

            backups = sorted([f for f in os.listdir(Config.BACKUP_DIR)
                             if f.startswith(Config.sanitize_folder_name(self.name))])
            for old in backups[:-10]:
                try:
                    os.remove(os.path.join(Config.BACKUP_DIR, old))
                except:
                    pass
        except Exception as e:
            print(f"Ошибка создания бэкапа: {e}")

    def get_stats(self) -> Dict:
        """Получить статистику"""
        total_words = sum(c.word_count() for c in self.chapters)
        total_chars = sum(c.char_count() for c in self.chapters)

        return {
            'chapters': len(self.chapters),
            'words': total_words,
            'chars': total_chars,
            'drafts': len([c for c in self.chapters if c.status == 'draft']),
            'review': len([c for c in self.chapters if c.status == 'review']),
            'done': len([c for c in self.chapters if c.status == 'done']),
            'created': self.created.strftime('%d.%m.%Y %H:%M'),
            'modified': self.modified.strftime('%d.%m.%Y %H:%M'),
            'has_cover': self.cover_path is not None  # Добавляем информацию о наличии обложки
        }

# === ДИАЛОГ ОБЛОЖКИ ===
class CoverDialog(QDialog):
    """Диалог для управления обложкой"""

    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.project = project
        self.setWindowTitle("Обложка книги")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel(f"Проект: {project.name}")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)

        # Область отображения обложки
        self.cover_label = QLabel()
        self.cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover_label.setMinimumHeight(300)
        self.cover_label.setStyleSheet("border: 2px dashed gray; margin: 10px;")

        # Загружаем текущую обложку
        self.update_cover_display()

        layout.addWidget(self.cover_label)

        # Информация о текущей обложке
        self.info_label = QLabel()
        self.update_info_label()
        layout.addWidget(self.info_label)

        # Кнопки
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("📷 Добавить обложку")
        self.add_btn.clicked.connect(self.add_cover)

        self.remove_btn = QPushButton("🗑 Удалить обложку")
        self.remove_btn.clicked.connect(self.remove_cover)
        self.remove_btn.setEnabled(self.project.cover_path is not None)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)

        layout.addLayout(btn_layout)

        # Кнопки диалога
        dialog_buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)
        layout.addWidget(dialog_buttons)

        self.setLayout(layout)

    def update_cover_display(self):
        """Обновить отображение обложки"""
        pixmap = self.project.get_cover_pixmap(300, 400)
        if pixmap:
            self.cover_label.setPixmap(pixmap)
        else:
            self.cover_label.setText("📖\n\nНет обложки\n\nНажмите 'Добавить обложку' для загрузки")
            self.cover_label.setStyleSheet("border: 2px dashed gray; margin: 10px; font-size: 16px;")

    def update_info_label(self):
        """Обновить информацию об обложке"""
        if self.project.cover_path and os.path.exists(self.project.cover_path):
            size = os.path.getsize(self.project.cover_path)
            name = os.path.basename(self.project.cover_path)
            self.info_label.setText(f"Текущая обложка: {name} ({size:,} байт)")
            self.info_label.setStyleSheet("color: green; margin: 5px;")
        else:
            self.info_label.setText("Обложка не установлена")
            self.info_label.setStyleSheet("color: gray; margin: 5px;")

    def add_cover(self):
        """Добавить обложку"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение для обложки",
            os.path.expanduser("~"),
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path:
            if self.project.set_cover(file_path):
                self.project.save()
                self.update_cover_display()
                self.update_info_label()
                self.remove_btn.setEnabled(True)
                QMessageBox.information(self, "Успех", "Обложка успешно добавлена!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось установить обложку. Проверьте формат файла.")

    def remove_cover(self):
        """Удалить обложку"""
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить обложку?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.project.remove_cover()
            self.project.save()
            self.update_cover_display()
            self.update_info_label()
            self.remove_btn.setEnabled(False)
            QMessageBox.information(self, "Успех", "Обложка удалена")

# === КАСТОМНЫЕ ВИДЖЕТЫ ===
class ChapterTreeItem(QTreeWidgetItem):
    """Элемент дерева глав"""
    # ... (класс ChapterTreeItem остается без изменений)
    def __init__(self, chapter: Chapter):
        super().__init__()
        self.chapter = chapter
        self.update_display()

    def update_display(self):
        """Обновить отображение"""
        self.setText(0, f"{self.chapter.order + 1}. {self.chapter.title}")
        self.setIcon(0, self.get_status_icon())
        self.setToolTip(0, f"Слов: {self.chapter.word_count()}\nСтатус: {self.chapter.status}")

    def get_status_icon(self):
        """Иконка статуса"""
        if self.chapter.status == 'done':
            return QIcon.fromTheme('emblem-default')
        elif self.chapter.status == 'review':
            return QIcon.fromTheme('emblem-important')
        else:
            return QIcon.fromTheme('document-new')

class ChapterTitleEditor(QWidget):
    """Виджет для редактирования названия главы"""
    # ... (класс ChapterTitleEditor остается без изменений)
    title_changed = pyqtSignal(str)

    def __init__(self, chapter: Chapter, parent=None):
        super().__init__(parent)
        self.chapter = chapter

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.title_edit = QLineEdit(chapter.title)
        self.title_edit.editingFinished.connect(self.on_title_changed)

        layout.addWidget(self.title_edit)
        self.setLayout(layout)

    def on_title_changed(self):
        """Когда название изменено"""
        new_title = self.title_edit.text().strip()
        if new_title and new_title != self.chapter.title:
            self.title_changed.emit(new_title)

class CodeEditor(QPlainTextEdit):
    """Редактор кода с подсветкой и Vim-режимом"""
    # ... (класс CodeEditor остается без изменений)
    def __init__(self, parent=None):
        super().__init__(parent)

        font = QFont('Consolas', 12)
        if not QFontInfo(font).fixedPitch():
            font = QFont('Courier New', 12)
        self.setFont(font)

        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

        self.tab_size = 4
        self.vim_mode = True
        self.mode = 'insert'

        self.status_label = QLabel("-- ВСТАВКА --")
        self.status_label.setStyleSheet("color: gray; padding: 2px;")

        self.highlight_current_line()

    def highlight_current_line(self):
        """Подсветка текущей строки"""
        try:
            extra_selections = []

            if not self.isReadOnly():
                selection = QTextEdit.ExtraSelection()
                line_color = QColor(Qt.GlobalColor.yellow).lighter(180)
                selection.format.setBackground(line_color)
                selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
                selection.cursor = self.textCursor()
                selection.cursor.clearSelection()
                extra_selections.append(selection)

            self.setExtraSelections(extra_selections)
        except:
            pass

    def keyPressEvent(self, event):
        """Обработка клавиш"""
        try:
            if not self.vim_mode:
                super().keyPressEvent(event)
                return

            if self.mode == 'normal':
                key = event.key()

                if key == Qt.Key.Key_I:
                    self.mode = 'insert'
                    self.status_label.setText("-- ВСТАВКА --")
                elif key == Qt.Key.Key_H:
                    self.moveCursor(QTextCursor.MoveOperation.Left)
                elif key == Qt.Key.Key_J:
                    self.moveCursor(QTextCursor.MoveOperation.Down)
                elif key == Qt.Key.Key_K:
                    self.moveCursor(QTextCursor.MoveOperation.Up)
                elif key == Qt.Key.Key_L:
                    self.moveCursor(QTextCursor.MoveOperation.Right)
                elif key == Qt.Key.Key_X:
                    self.textCursor().deleteChar()
                elif key == Qt.Key.Key_U and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    self.undo()

            elif self.mode == 'insert':
                if event.key() == Qt.Key.Key_Escape:
                    self.mode = 'normal'
                    self.status_label.setText("-- НОРМАЛЬНЫЙ --")
                else:
                    super().keyPressEvent(event)

            self.highlight_current_line()
        except:
            super().keyPressEvent(event)

# === ДИАЛОГ НАСТРОЕК ===
class SettingsDialog(QDialog):
    """Диалог настроек приложения"""
    # ... (класс SettingsDialog остается без изменений, но нужно добавить импорт Theme)
    theme_changed = pyqtSignal(str)

    def __init__(self, settings: 'Settings', parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Настройки")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        layout = QVBoxLayout()

        # Создаем вкладки
        tabs = QTabWidget()

        # Вкладка "Общие"
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "Общие")

        # Вкладка "Темы"
        theme_tab = self.create_theme_tab()
        tabs.addTab(theme_tab, "Оформление")

        # Вкладка "Редактор"
        editor_tab = self.create_editor_tab()
        tabs.addTab(editor_tab, "Редактор")

        layout.addWidget(tabs)

        # Кнопки
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        apply_btn = QPushButton("Применить")
        apply_btn.clicked.connect(self.apply_settings)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def create_general_tab(self) -> QWidget:
        """Создать вкладку общих настроек"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Автосохранение
        auto_save_group = QGroupBox("Автосохранение")
        auto_save_layout = QVBoxLayout()

        self.auto_save_check = QCheckBox("Включить автосохранение")
        self.auto_save_check.setChecked(self.settings.config.get('auto_save_enabled', True))

        auto_save_interval_layout = QHBoxLayout()
        auto_save_interval_layout.addWidget(QLabel("Интервал (секунд):"))
        self.auto_save_interval = QSpinBox()
        self.auto_save_interval.setRange(10, 300)
        self.auto_save_interval.setValue(self.settings.config.get('auto_save', 30))
        auto_save_interval_layout.addWidget(self.auto_save_interval)
        auto_save_interval_layout.addStretch()

        auto_save_layout.addWidget(self.auto_save_check)
        auto_save_layout.addLayout(auto_save_interval_layout)
        auto_save_group.setLayout(auto_save_layout)
        layout.addWidget(auto_save_group)

        # Резервное копирование
        backup_group = QGroupBox("Резервное копирование")
        backup_layout = QVBoxLayout()

        self.backup_check = QCheckBox("Создавать резервные копии")
        self.backup_check.setChecked(self.settings.config.get('backup_enabled', True))

        backup_count_layout = QHBoxLayout()
        backup_count_layout.addWidget(QLabel("Хранить копий:"))
        self.backup_count = QSpinBox()
        self.backup_count.setRange(1, 50)
        self.backup_count.setValue(self.settings.config.get('backup_count', 10))
        backup_count_layout.addWidget(self.backup_count)
        backup_count_layout.addStretch()

        backup_layout.addWidget(self.backup_check)
        backup_layout.addLayout(backup_count_layout)
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)

        # Недавние проекты
        recent_group = QGroupBox("Недавние проекты")
        recent_layout = QHBoxLayout()
        recent_layout.addWidget(QLabel("Максимум проектов:"))
        self.max_recent = QSpinBox()
        self.max_recent.setRange(3, 30)
        self.max_recent.setValue(self.settings.config.get('max_recent', 10))
        recent_layout.addWidget(self.max_recent)
        recent_layout.addStretch()
        recent_group.setLayout(recent_layout)
        layout.addWidget(recent_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_theme_tab(self) -> QWidget:
        """Создать вкладку настроек темы"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Выбор темы
        theme_group = QGroupBox("Тема оформления")
        theme_layout = QVBoxLayout()

        # Список тем
        theme_selection_layout = QHBoxLayout()
        theme_selection_layout.addWidget(QLabel("Тема:"))

        self.theme_combo = QComboBox()
        for theme_id, theme_data in Theme.THEMES.items():
            self.theme_combo.addItem(theme_data['name'], theme_id)

        current_theme = self.settings.config.get('theme', 'dark')
        index = self.theme_combo.findData(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)
        theme_selection_layout.addWidget(self.theme_combo)
        theme_selection_layout.addStretch()

        theme_layout.addLayout(theme_selection_layout)

        # Предпросмотр темы
        preview_label = QLabel("Предпросмотр:")
        theme_layout.addWidget(preview_label)

        preview_frame = QFrame()
        preview_frame.setFrameStyle(QFrame.Shape.Box)
        preview_frame.setMinimumHeight(100)

        preview_layout = QHBoxLayout()

        preview_btn = QPushButton("Кнопка")
        preview_layout.addWidget(preview_btn)

        preview_input = QLineEdit()
        preview_input.setText("Текст")
        preview_layout.addWidget(preview_input)

        preview_check = QCheckBox("Чекбокс")
        preview_layout.addWidget(preview_check)

        preview_layout.addStretch()
        preview_frame.setLayout(preview_layout)
        theme_layout.addWidget(preview_frame)

        # Обновляем стиль предпросмотра при смене темы
        self.preview_frame = preview_frame
        self.update_preview_style(current_theme)

        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # Пользовательские цвета
        colors_group = QGroupBox("Пользовательские цвета")
        colors_layout = QVBoxLayout()
        colors_layout.addWidget(QLabel("В разработке..."))
        colors_group.setLayout(colors_layout)
        layout.addWidget(colors_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_editor_tab(self) -> QWidget:
        """Создать вкладку настроек редактора"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Шрифт
        font_group = QGroupBox("Шрифт")
        font_layout = QGridLayout()

        font_layout.addWidget(QLabel("Семейство:"), 0, 0)
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont(self.settings.config.get('font_family', 'Consolas')))
        font_layout.addWidget(self.font_combo, 0, 1)

        font_layout.addWidget(QLabel("Размер:"), 1, 0)
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 72)
        self.font_size.setValue(self.settings.config.get('font_size', 12))
        font_layout.addWidget(self.font_size, 1, 1)

        font_group.setLayout(font_layout)
        layout.addWidget(font_group)

        # Режимы
        mode_group = QGroupBox("Режимы")
        mode_layout = QVBoxLayout()

        self.vim_mode_check = QCheckBox("Vim-режим")
        self.vim_mode_check.setChecked(self.settings.config.get('vim_mode', True))
        mode_layout.addWidget(self.vim_mode_check)

        self.word_wrap_check = QCheckBox("Перенос слов")
        self.word_wrap_check.setChecked(self.settings.config.get('word_wrap', True))
        mode_layout.addWidget(self.word_wrap_check)

        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Табуляция
        tab_group = QGroupBox("Табуляция")
        tab_layout = QHBoxLayout()
        tab_layout.addWidget(QLabel("Размер табуляции:"))
        self.tab_size = QSpinBox()
        self.tab_size.setRange(2, 8)
        self.tab_size.setValue(self.settings.config.get('tab_size', 4))
        tab_layout.addWidget(self.tab_size)
        tab_layout.addStretch()
        tab_group.setLayout(tab_layout)
        layout.addWidget(tab_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def on_theme_changed(self, index: int):
        """При смене темы в комбобоксе"""
        theme_id = self.theme_combo.currentData()
        self.update_preview_style(theme_id)

    def update_preview_style(self, theme_id: str):
        """Обновить стиль предпросмотра"""
        theme = Theme(theme_id)
        self.preview_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {theme.get('window_bg')};
                border: 1px solid {theme.get('border_color')};
            }}
            QPushButton {{
                background-color: {theme.get('button_bg')};
                color: {theme.get('button_fg')};
                border: 1px solid {theme.get('border_color')};
                padding: 5px;
            }}
            QLineEdit {{
                background-color: {theme.get('input_bg')};
                color: {theme.get('input_fg')};
                border: 1px solid {theme.get('input_border')};
                padding: 3px;
            }}
            QCheckBox {{
                color: {theme.get('window_fg')};
            }}
        """)

    def save_settings(self):
        """Сохранить настройки"""
        self.apply_settings()
        self.settings.save_config()
        self.accept()

    def apply_settings(self):
        """Применить настройки"""
        # Общие
        self.settings.config['auto_save_enabled'] = self.auto_save_check.isChecked()
        self.settings.config['auto_save'] = self.auto_save_interval.value()
        self.settings.config['backup_enabled'] = self.backup_check.isChecked()
        self.settings.config['backup_count'] = self.backup_count.value()
        self.settings.config['max_recent'] = self.max_recent.value()

        # Тема
        old_theme = self.settings.config.get('theme')
        new_theme = self.theme_combo.currentData()
        self.settings.config['theme'] = new_theme

        # Редактор
        self.settings.config['font_family'] = self.font_combo.currentFont().family()
        self.settings.config['font_size'] = self.font_size.value()
        self.settings.config['vim_mode'] = self.vim_mode_check.isChecked()
        self.settings.config['word_wrap'] = self.word_wrap_check.isChecked()
        self.settings.config['tab_size'] = self.tab_size.value()

        # Сигнал о смене темы
        if old_theme != new_theme:
            self.theme_changed.emit(new_theme)

class Settings:
    """Настройки приложения"""
    # ... (класс Settings остается без изменений)
    def __init__(self):
        self.config = self.load_config()
        self.recent_projects = self.load_recent()
        self.theme = Theme(self.config.get('theme', 'dark'))

    def load_config(self) -> dict:
        """Загрузить конфигурацию"""
        default_config = {
            'theme': 'dark',
            'auto_save': 30,
            'auto_save_enabled': True,
            'backup_enabled': True,
            'backup_count': 10,
            'vim_mode': True,
            'word_wrap': True,
            'tab_size': 4,
            'font_size': 12,
            'font_family': 'Consolas',
            'max_recent': 10,
            'last_project': None
        }

        if os.path.exists(Config.CONFIG_FILE):
            try:
                with open(Config.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    default_config.update(config)
            except:
                pass

        return default_config

    def save_config(self):
        """Сохранить конфигурацию"""
        try:
            with open(Config.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения конфига: {e}")

    def load_recent(self) -> List[Dict]:
        """Загрузить список недавних проектов"""
        if os.path.exists(Config.RECENT_FILE):
            try:
                with open(Config.RECENT_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []

    def save_recent(self):
        """Сохранить список недавних проектов"""
        try:
            with open(Config.RECENT_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.recent_projects, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения недавних проектов: {e}")

    def add_recent_project(self, path: str, name: str):
        """Добавить проект в недавние"""
        self.recent_projects = [p for p in self.recent_projects if p['path'] != path]

        self.recent_projects.insert(0, {
            'path': path,
            'name': name,
            'last_opened': datetime.now().isoformat()
        })

        max_recent = self.config.get('max_recent', 10)
        self.recent_projects = self.recent_projects[:max_recent]

        self.save_recent()

    def get_recent_projects(self) -> List[Dict]:
        """Получить список недавних проектов"""
        return self.recent_projects

    def update_theme(self, theme_name: str):
        """Обновить тему"""
        self.config['theme'] = theme_name
        self.theme = Theme(theme_name)
        self.save_config()

# === ОСНОВНЫЕ ОКНА ===
class ChapterEditor(QWidget):
    """Редактор главы"""
    # ... (класс ChapterEditor остается без изменений)
    chapter_title_changed = pyqtSignal(str, str)  # chapter_id, new_title

    def __init__(self, project: Project, chapter: Chapter, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.project = project
        self.chapter = chapter

        self.setWindowTitle(f"{chapter.title} - {project.name}")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Верхняя панель
        toolbar = QToolBar()
        toolbar.setMovable(False)

        save_btn = QAction(QIcon.fromTheme('document-save'), 'Сохранить', self)
        save_btn.triggered.connect(self.save_chapter)
        toolbar.addAction(save_btn)

        toolbar.addSeparator()

        # Редактор названия
        toolbar.addWidget(QLabel("Название:"))
        self.title_editor = ChapterTitleEditor(chapter)
        self.title_editor.title_changed.connect(self.on_title_changed)
        toolbar.addWidget(self.title_editor)

        toolbar.addSeparator()

        # Статус
        self.status_combo = QComboBox()
        self.status_combo.addItems(['draft', 'review', 'done'])
        self.status_combo.setCurrentText(chapter.status)
        self.status_combo.currentTextChanged.connect(self.change_status)
        toolbar.addWidget(QLabel("Статус:"))
        toolbar.addWidget(self.status_combo)

        toolbar.addSeparator()

        # Статистика
        self.stats_label = QLabel()
        self.update_stats()
        toolbar.addWidget(self.stats_label)

        toolbar_widget = QWidget()
        toolbar_widget.setLayout(QHBoxLayout())
        toolbar_widget.layout().addWidget(toolbar)
        toolbar_widget.layout().addStretch()
        layout.addWidget(toolbar_widget)

        # Редактор
        self.editor = CodeEditor()
        self.editor.setPlainText(chapter.content)
        self.editor.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.editor)

        # Vim статус
        layout.addWidget(self.editor.status_label)

        self.setLayout(layout)

    def on_title_changed(self, new_title: str):
        """Когда изменено название главы"""
        self.chapter.title = new_title
        self.setWindowTitle(f"{new_title} - {self.project.name}")
        self.chapter_title_changed.emit(self.chapter.id, new_title)
        self.save_chapter()

    def save_chapter(self):
        """Сохранить главу"""
        try:
            self.chapter.content = self.editor.toPlainText()
            self.chapter.modified = datetime.now()
            if self.project.save():
                self.update_stats()
                if self.main_window and hasattr(self.main_window, 'statusBar'):
                    self.main_window.statusBar().showMessage("Сохранено", 2000)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def on_text_changed(self):
        """При изменении текста"""
        self.update_stats()
        if hasattr(self.editor, 'document'):
            self.editor.document().setModified(True)

    def update_stats(self):
        """Обновить статистику"""
        try:
            words = len(re.findall(r'\b\w+\b', self.editor.toPlainText()))
            chars = len(self.editor.toPlainText())
            self.stats_label.setText(f"Слов: {words} | Символов: {chars}")
        except:
            pass

    def change_status(self, status):
        """Изменить статус"""
        try:
            self.chapter.status = status
            self.project.save()
        except Exception as e:
            print(f"Ошибка изменения статуса: {e}")

class MainWindow(QMainWindow):
    """Главное окно"""

    def __init__(self):
        super().__init__()
        self.current_project: Optional[Project] = None
        self.editors = {}  # chapter_id -> editor widget
        self.settings = Settings()

        Config.init_dirs()

        self.setWindowTitle("Читалка-писалка Pro")
        self.setGeometry(100, 100, 1400, 900)

        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        self.create_menu()
        self.create_toolbar()
        self.create_dock_widgets()

        self.statusBar().showMessage("Готов")

        # Применяем сохраненную тему
        self.apply_theme(self.settings.config.get('theme', 'dark'))

        QTimer.singleShot(100, self.show_start_page)

    def create_menu(self):
        """Создать меню"""
        menubar = self.menuBar()
        menubar.clear()

        # Файл
        file_menu = menubar.addMenu("&Файл")

        new_project = QAction(QIcon.fromTheme('document-new'), "&Новый проект", self)
        new_project.setShortcut("Ctrl+N")
        new_project.triggered.connect(self.new_project)
        file_menu.addAction(new_project)

        open_project_action = QAction(QIcon.fromTheme('document-open'), "&Открыть проект...", self)
        open_project_action.setShortcut("Ctrl+O")
        open_project_action.triggered.connect(self.open_project_dialog)
        file_menu.addAction(open_project_action)

        self.recent_menu = file_menu.addMenu("&Недавние проекты")
        self.update_recent_menu()

        file_menu.addSeparator()

        save_all = QAction(QIcon.fromTheme('document-save-all'), "&Сохранить всё", self)
        save_all.setShortcut("Ctrl+Shift+S")
        save_all.triggered.connect(self.save_all)
        file_menu.addAction(save_all)

        file_menu.addSeparator()

        # НОВОЕ: Подменю для обложки
        cover_menu = file_menu.addMenu("📷 &Обложка")

        add_cover_action = QAction("Добавить/Изменить обложку", self)
        add_cover_action.triggered.connect(self.manage_cover)
        cover_menu.addAction(add_cover_action)

        remove_cover_action = QAction("Удалить обложку", self)
        remove_cover_action.triggered.connect(self.remove_cover)
        cover_menu.addAction(remove_cover_action)

        cover_menu.addSeparator()

        view_cover_action = QAction("Просмотреть обложку", self)
        view_cover_action.triggered.connect(self.view_cover)
        cover_menu.addAction(view_cover_action)

        file_menu.addSeparator()

        export_menu = file_menu.addMenu("&Экспорт")

        export_fb2 = QAction("FB2", self)
        export_fb2.triggered.connect(lambda: self.export_project('fb2'))
        export_menu.addAction(export_fb2)

        export_pdf = QAction("PDF", self)
        export_pdf.triggered.connect(lambda: self.export_project('pdf'))
        export_menu.addAction(export_pdf)

        export_txt = QAction("TXT", self)
        export_txt.triggered.connect(lambda: self.export_project('txt'))
        export_menu.addAction(export_txt)

        file_menu.addSeparator()

        exit_action = QAction("&Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Настройки
        settings_menu = menubar.addMenu("&Настройки")

        theme_menu = settings_menu.addMenu("&Тема оформления")

        for theme_id, theme_data in Theme.THEMES.items():
            action = QAction(theme_data['name'], self)
            action.setData(theme_id)
            action.triggered.connect(lambda checked, t=theme_id: self.change_theme(t))
            if theme_id == self.settings.config.get('theme'):
                action.setCheckable(True)
                action.setChecked(True)
            theme_menu.addAction(action)

        theme_menu.addSeparator()

        settings_action = QAction("&Настройки...", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self.show_settings)
        settings_menu.addAction(settings_action)

        # Справка
        help_menu = menubar.addMenu("&Справка")

        about_action = QAction("&О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    # НОВЫЕ МЕТОДЫ ДЛЯ РАБОТЫ С ОБЛОЖКОЙ
    def manage_cover(self):
        """Управление обложкой"""
        if not self.current_project:
            QMessageBox.warning(self, "Предупреждение", "Сначала откройте проект")
            return

        dialog = CoverDialog(self.current_project, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.update_stats_display()
            self.statusBar().showMessage("Обложка обновлена", 2000)

    def remove_cover(self):
        """Удалить обложку"""
        if not self.current_project:
            return

        if not self.current_project.cover_path:
            QMessageBox.information(self, "Информация", "У проекта нет обложки")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить обложку?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.current_project.remove_cover()
            self.current_project.save()
            self.update_stats_display()
            self.statusBar().showMessage("Обложка удалена", 2000)

    def view_cover(self):
        """Просмотреть обложку в отдельном окне"""
        if not self.current_project or not self.current_project.cover_path:
            QMessageBox.information(self, "Информация", "У проекта нет обложки")
            return

        pixmap = self.current_project.get_cover_pixmap(800, 600)
        if pixmap:
            dialog = QDialog(self)
            dialog.setWindowTitle("Обложка книги")
            layout = QVBoxLayout()

            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            scroll = QScrollArea()
            scroll.setWidget(label)
            scroll.setWidgetResizable(True)

            layout.addWidget(scroll)

            close_btn = QPushButton("Закрыть")
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)

            dialog.setLayout(layout)
            dialog.resize(900, 700)
            dialog.exec()

    # ОСТАЛЬНЫЕ МЕТОДЫ С НЕБОЛЬШИМИ ИЗМЕНЕНИЯМИ
    def change_theme(self, theme_name: str):
        """Сменить тему"""
        self.settings.update_theme(theme_name)
        self.apply_theme(theme_name)
        self.create_menu()

    def apply_theme(self, theme_name: str):
        """Применить тему"""
        theme = Theme(theme_name)
        self.setStyleSheet(theme.get_stylesheet())

        for sub in self.mdi_area.subWindowList():
            if isinstance(sub.widget(), ChapterEditor):
                sub.widget().editor.setStyleSheet("")
                sub.widget().editor.setStyleSheet(theme.get_stylesheet())

    def show_settings(self):
        """Показать диалог настроек"""
        dialog = SettingsDialog(self.settings, self)
        dialog.theme_changed.connect(self.change_theme)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.apply_theme(self.settings.config.get('theme'))
            self.statusBar().showMessage("Настройки сохранены", 2000)

    def show_about(self):
        """Показать информацию о программе"""
        QMessageBox.about(
            self,
            "О программе",
            """<h1>Читалка-писалка Pro</h1>
            <p>Версия: 3.4.0</p>
            <p>Профессиональный инструмент для писателей</p>
            <br>
            <p><b>Возможности:</b></p>
            <ul>
                <li>Многодокументный интерфейс</li>
                <li>Дерево проекта с Drag&Drop</li>
                <li>Система тем оформления</li>
                <li>Поддержка обложек книг</li>
                <li>Статистика в реальном времени</li>
                <li>Экспорт в FB2/PDF/TXT с обложкой</li>
                <li>Vim-режим</li>
                <li>Система недавних проектов</li>
                <li>Автосохранение и бэкапы</li>
            </ul>
            <br>
            <p>© 2024 Читалка-писалка Pro</p>"""
        )

    def update_recent_menu(self):
        """Обновить меню недавних проектов"""
        self.recent_menu.clear()

        recent = self.settings.get_recent_projects()
        if not recent:
            action = QAction("Нет недавних проектов", self)
            action.setEnabled(False)
            self.recent_menu.addAction(action)
            return

        for project in recent:
            name = project['name']
            path = project['path']
            action = QAction(name, self)
            action.setData(path)
            action.triggered.connect(lambda checked, p=path: self.open_project_path(p))
            self.recent_menu.addAction(action)

        self.recent_menu.addSeparator()
        clear_action = QAction("Очистить список", self)
        clear_action.triggered.connect(self.clear_recent)
        self.recent_menu.addAction(clear_action)

    def clear_recent(self):
        """Очистить список недавних проектов"""
        self.settings.recent_projects = []
        self.settings.save_recent()
        self.update_recent_menu()

    def create_toolbar(self):
        """Создать тулбар"""
        toolbar = self.addToolBar("Основная")

        new_btn = QAction(QIcon.fromTheme('document-new'), "Новый проект", self)
        new_btn.triggered.connect(self.new_project)
        toolbar.addAction(new_btn)

        open_btn = QAction(QIcon.fromTheme('document-open'), "Открыть", self)
        open_btn.triggered.connect(self.open_project_dialog)
        toolbar.addAction(open_btn)

        toolbar.addSeparator()

        save_btn = QAction(QIcon.fromTheme('document-save'), "Сохранить всё", self)
        save_btn.triggered.connect(self.save_all)
        toolbar.addAction(save_btn)

        toolbar.addSeparator()

        add_chapter_btn = QAction(QIcon.fromTheme('list-add'), "Добавить главу", self)
        add_chapter_btn.triggered.connect(self.add_chapter)
        toolbar.addAction(add_chapter_btn)

        toolbar.addSeparator()

        # НОВОЕ: Кнопка обложки на тулбаре
        cover_btn = QAction(QIcon.fromTheme('image-x-generic'), "Обложка", self)
        cover_btn.triggered.connect(self.manage_cover)
        toolbar.addAction(cover_btn)

        toolbar.addSeparator()

        settings_btn = QAction(QIcon.fromTheme('preferences-system'), "Настройки", self)
        settings_btn.triggered.connect(self.show_settings)
        toolbar.addAction(settings_btn)

    def create_dock_widgets(self):
        """Создать закрепляемые панели"""
        # Дерево проекта
        self.project_dock = QDockWidget("Проект", self)
        self.project_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea |
                                          Qt.DockWidgetArea.RightDockWidgetArea)

        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderLabel("Главы")
        self.project_tree.setDragEnabled(True)
        self.project_tree.setAcceptDrops(True)
        self.project_tree.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.project_tree.itemDoubleClicked.connect(self.open_chapter)
        self.project_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.project_tree.customContextMenuRequested.connect(self.show_chapter_context_menu)

        self.project_dock.setWidget(self.project_tree)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.project_dock)

        # Панель статистики
        self.stats_dock = QDockWidget("Статистика", self)
        self.stats_widget = QWidget()
        self.stats_layout = QVBoxLayout()

        # НОВОЕ: Добавляем отображение обложки в статистику
        self.cover_preview = QLabel()
        self.cover_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover_preview.setMinimumHeight(150)
        self.cover_preview.setStyleSheet("border: 1px solid gray; margin: 5px;")
        self.stats_layout.addWidget(self.cover_preview)

        self.stats_text = QLabel()
        self.stats_text.setWordWrap(True)
        self.stats_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.stats_text.setOpenExternalLinks(False)

        self.stats_layout.addWidget(self.stats_text)
        self.stats_layout.addStretch()

        self.stats_widget.setLayout(self.stats_layout)
        self.stats_dock.setWidget(self.stats_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.stats_dock)

        # Панель поиска
        self.search_dock = QDockWidget("Поиск", self)
        search_widget = QWidget()
        search_layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        self.search_input.textChanged.connect(self.search_text)

        self.search_results = QListWidget()
        self.search_results.itemDoubleClicked.connect(self.goto_search_result)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_results)

        search_widget.setLayout(search_layout)
        self.search_dock.setWidget(search_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.search_dock)

        self.search_dock.hide()

    def show_chapter_context_menu(self, position):
        """Показать контекстное меню для главы"""
        item = self.project_tree.itemAt(position)
        if not isinstance(item, ChapterTreeItem):
            return

        menu = QMenu()

        rename_action = menu.addAction("Переименовать")
        delete_action = menu.addAction("Удалить")
        menu.addSeparator()

        status_menu = menu.addMenu("Изменить статус")
        draft_action = status_menu.addAction("Черновик")
        review_action = status_menu.addAction("На ревью")
        done_action = status_menu.addAction("Готово")

        action = menu.exec(self.project_tree.viewport().mapToGlobal(position))

        if action == rename_action:
            self.rename_chapter(item)
        elif action == delete_action:
            self.delete_chapter(item)
        elif action == draft_action:
            self.change_chapter_status(item, 'draft')
        elif action == review_action:
            self.change_chapter_status(item, 'review')
        elif action == done_action:
            self.change_chapter_status(item, 'done')

    def rename_chapter(self, item: ChapterTreeItem):
        """Переименовать главу"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Переименовать главу")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Новое название:"))

        title_input = QLineEdit(item.chapter.title)
        layout.addWidget(title_input)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("ОК")
        cancel_btn = QPushButton("Отмена")

        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        dialog.setLayout(layout)

        def rename():
            new_title = title_input.text().strip()
            if new_title and new_title != item.chapter.title:
                if self.current_project.update_chapter_title(item.chapter.id, new_title):
                    self.current_project.save()
                    item.chapter.title = new_title
                    item.update_display()

                    if item.chapter.id in self.editors:
                        editor = self.editors[item.chapter.id].widget()
                        if isinstance(editor, ChapterEditor):
                            editor.setWindowTitle(f"{new_title} - {self.current_project.name}")
                            editor.title_editor.title_edit.setText(new_title)

                    self.statusBar().showMessage("Глава переименована", 2000)
            dialog.accept()

        ok_btn.clicked.connect(rename)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec()

    def delete_chapter(self, item: ChapterTreeItem):
        """Удалить главу"""
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Удалить главу '{item.chapter.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if item.chapter.id in self.editors:
                self.editors[item.chapter.id].close()

            self.current_project.delete_chapter(item.chapter.id)
            self.current_project.save()

            index = self.project_tree.indexOfTopLevelItem(item)
            self.project_tree.takeTopLevelItem(index)

            for i in range(self.project_tree.topLevelItemCount()):
                tree_item = self.project_tree.topLevelItem(i)
                if isinstance(tree_item, ChapterTreeItem):
                    tree_item.chapter.order = i
                    tree_item.update_display()

            self.update_stats_display()
            self.statusBar().showMessage("Глава удалена", 2000)

    def change_chapter_status(self, item: ChapterTreeItem, status: str):
        """Изменить статус главы"""
        item.chapter.status = status
        item.update_display()
        self.current_project.save()

        if item.chapter.id in self.editors:
            editor = self.editors[item.chapter.id].widget()
            if isinstance(editor, ChapterEditor):
                editor.status_combo.setCurrentText(status)

        self.update_stats_display()
        self.statusBar().showMessage(f"Статус изменен на {status}", 2000)

    def show_start_page(self):
        """Показать стартовую страницу"""
        try:
            self.mdi_area.closeAllSubWindows()
            self.project_tree.clear()
            self.current_project = None

            start_widget = QWidget()
            layout = QVBoxLayout()
            layout.setSpacing(20)

            title = QLabel("📚 Читалка-писалка Pro")
            title.setStyleSheet("font-size: 32px; font-weight: bold; margin: 30px;")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title)

            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(20)

            new_btn = QPushButton("➕ Создать новый проект")
            new_btn.setMinimumHeight(60)
            new_btn.setMinimumWidth(200)
            new_btn.clicked.connect(self.new_project)
            btn_layout.addWidget(new_btn)

            open_btn = QPushButton("📂 Открыть существующий")
            open_btn.setMinimumHeight(60)
            open_btn.setMinimumWidth(200)
            open_btn.clicked.connect(self.open_project_dialog)
            btn_layout.addWidget(open_btn)

            layout.addLayout(btn_layout)

            recent = self.settings.get_recent_projects()
            if recent:
                recent_label = QLabel("Недавние проекты:")
                recent_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 30px;")
                layout.addWidget(recent_label)

                for project in recent[:5]:
                    project_widget = self.create_recent_project_widget(project)
                    layout.addWidget(project_widget)

            layout.addStretch()
            start_widget.setLayout(layout)

            scroll = QScrollArea()
            scroll.setWidget(start_widget)
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("QScrollArea { border: none; }")

            sub = self.mdi_area.addSubWindow(scroll)
            sub.setWindowTitle("Стартовая страница")
            sub.show()

        except Exception as e:
            print(f"Ошибка при показе стартовой страницы: {e}")

    def create_recent_project_widget(self, project: Dict) -> QWidget:
        """Создать виджет недавнего проекта"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        icon_label = QLabel("📁")
        icon_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(icon_label)

        info_layout = QVBoxLayout()
        name_label = QLabel(project['name'])
        name_label.setStyleSheet("font-weight: bold;")

        path_label = QLabel(project['path'])
        path_label.setStyleSheet("color: gray; font-size: 10px;")

        info_layout.addWidget(name_label)
        info_layout.addWidget(path_label)
        layout.addLayout(info_layout, 1)

        open_btn = QPushButton("Открыть")
        open_btn.clicked.connect(lambda: self.open_project_path(project['path']))
        layout.addWidget(open_btn)

        widget.setLayout(layout)
        return widget

    def new_project(self):
        """Создать новый проект"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Новый проект")
        dialog.setMinimumWidth(500)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        layout.addWidget(QLabel("Название проекта:"))
        name_input = QLineEdit()
        name_input.setPlaceholderText("Введите название проекта")
        layout.addWidget(name_input)

        layout.addWidget(QLabel("Автор:"))
        author_input = QLineEdit()
        author_input.setPlaceholderText("Ваше имя")
        layout.addWidget(author_input)

        layout.addWidget(QLabel("Папка для сохранения:"))
        path_layout = QHBoxLayout()

        path_input = QLineEdit()
        default_path = os.path.join(Config.PROJECTS_DIR, "Новый проект")
        path_input.setText(default_path)
        path_input.setReadOnly(True)

        browse_btn = QPushButton("Обзор...")
        browse_btn.clicked.connect(lambda: self.browse_project_folder(path_input))

        path_layout.addWidget(path_input)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        # НОВОЕ: Опция добавить обложку сразу
        cover_layout = QHBoxLayout()
        cover_layout.addWidget(QLabel("Обложка (можно добавить позже):"))
        self.temp_cover_path = None
        self.temp_cover_label = QLabel("Не выбрана")
        cover_layout.addWidget(self.temp_cover_label)
        select_cover_btn = QPushButton("Выбрать...")
        select_cover_btn.clicked.connect(self.select_temp_cover)
        cover_layout.addWidget(select_cover_btn)
        layout.addLayout(cover_layout)

        btn_layout = QHBoxLayout()
        create_btn = QPushButton("Создать")
        create_btn.setDefault(True)
        cancel_btn = QPushButton("Отмена")

        btn_layout.addWidget(create_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        dialog.setLayout(layout)

        def create():
            name = name_input.text().strip()
            if not name:
                QMessageBox.warning(dialog, "Ошибка", "Введите название проекта")
                return

            safe_name = Config.sanitize_folder_name(name)

            path = path_input.text().strip()
            if not path or path == default_path:
                path = os.path.join(Config.PROJECTS_DIR, safe_name)

            if os.path.exists(path):
                reply = QMessageBox.question(
                    dialog,
                    "Подтверждение",
                    f"Папка уже существует. Открыть существующий проект?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    dialog.accept()
                    self.open_project_path(path)
                return

            project = Project(name, path)
            if author_input.text():
                project.settings['author'] = author_input.text()

            # Добавляем обложку если выбрана
            if self.temp_cover_path:
                project.set_cover(self.temp_cover_path)

            if project.save():
                dialog.accept()
                self.settings.add_recent_project(path, name)
                self.update_recent_menu()
                self.open_project_path(path)
            else:
                QMessageBox.critical(dialog, "Ошибка",
                                   "Не удалось создать проект. Проверьте права доступа.")

        create_btn.clicked.connect(create)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec()

    def select_temp_cover(self):
        """Выбрать временную обложку при создании проекта"""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение для обложки",
            os.path.expanduser("~"),
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if path:
            self.temp_cover_path = path
            self.temp_cover_label.setText(os.path.basename(path))

    def browse_project_folder(self, line_edit: QLineEdit):
        """Выбрать папку для проекта"""
        path = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для проекта",
            Config.PROJECTS_DIR
        )
        if path:
            line_edit.setText(path)

    def open_project_dialog(self):
        """Диалог открытия проекта"""
        path = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку проекта",
            Config.PROJECTS_DIR
        )

        if path:
            self.open_project_path(path)

    def open_project_path(self, path: str):
        """Открыть проект по пути"""
        try:
            project = Project.load(path)
            if project:
                self.load_project(project)
                self.settings.add_recent_project(path, project.name)
                self.update_recent_menu()
            else:
                QMessageBox.critical(self, "Ошибка",
                                   "Не удалось загрузить проект. Файл проекта поврежден или отсутствует.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть проект: {e}")

    def load_project(self, project: Project):
        """Загрузить проект в интерфейс"""
        try:
            self.current_project = project
            self.setWindowTitle(f"Читалка-писалка Pro - {project.name}")

            self.mdi_area.closeAllSubWindows()

            self.project_tree.clear()
            for chapter in project.chapters:
                item = ChapterTreeItem(chapter)
                self.project_tree.addTopLevelItem(item)

            self.update_stats_display()

            self.project_dock.show()
            self.stats_dock.show()

            self.statusBar().showMessage(f"Проект '{project.name}' загружен")
        except Exception as e:
            print(f"Ошибка загрузки проекта в интерфейс: {e}")

    def update_stats_display(self):
        """Обновить отображение статистики"""
        if not self.current_project:
            return

        try:
            stats = self.current_project.get_stats()

            # Обновляем предпросмотр обложки
            pixmap = self.current_project.get_cover_pixmap(180, 250)
            if pixmap:
                self.cover_preview.setPixmap(pixmap)
                self.cover_preview.setToolTip("Обложка книги")
            else:
                self.cover_preview.setText("📖\nНет обложки")
                self.cover_preview.setStyleSheet("border: 1px solid gray; margin: 5px; font-size: 14px;")

            text = f"""
            <b>Статистика проекта</b><br><br>
            📚 Глав: {stats['chapters']}<br>
            📝 Слов: {stats['words']:,}<br>
            🔤 Символов: {stats['chars']:,}<br>
            <br>
            <b>Статусы:</b><br>
            📝 Черновиков: {stats['drafts']}<br>
            🔍 На ревью: {stats['review']}<br>
            ✅ Готово: {stats['done']}<br>
            <br>
            <b>Обложка:</b><br>
            {'✅ Есть' if stats['has_cover'] else '❌ Нет'}<br>
            <br>
            <b>Даты:</b><br>
            ✨ Создан: {stats['created']}<br>
            📅 Изменён: {stats['modified']}<br>
            """

            self.stats_text.setText(text)
        except Exception as e:
            print(f"Ошибка обновления статистики: {e}")

    def add_chapter(self):
        """Добавить главу"""
        if not self.current_project:
            QMessageBox.warning(self, "Предупреждение", "Сначала откройте проект")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Новая глава")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Название главы:"))
        title_input = QLineEdit(f"Глава {len(self.current_project.chapters) + 1}")
        layout.addWidget(title_input)

        btn_layout = QHBoxLayout()
        create_btn = QPushButton("Создать")
        cancel_btn = QPushButton("Отмена")

        btn_layout.addWidget(create_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        dialog.setLayout(layout)

        def create():
            title = title_input.text().strip()
            chapter = self.current_project.add_chapter(title)
            self.current_project.save()

            item = ChapterTreeItem(chapter)
            self.project_tree.addTopLevelItem(item)

            dialog.accept()
            self.open_chapter(item)

        create_btn.clicked.connect(create)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec()

    def open_chapter(self, item):
        """Открыть главу"""
        if not isinstance(item, ChapterTreeItem):
            item = self.project_tree.currentItem()
            if not isinstance(item, ChapterTreeItem):
                return

        chapter = item.chapter

        if chapter.id in self.editors:
            self.mdi_area.setActiveSubWindow(self.editors[chapter.id])
            return

        editor = ChapterEditor(self.current_project, chapter, self)
        editor.chapter_title_changed.connect(self.on_chapter_title_changed)

        sub = self.mdi_area.addSubWindow(editor)
        sub.setWindowTitle(chapter.title)
        sub.show()

        self.editors[chapter.id] = sub
        sub.destroyed.connect(lambda: self.editors.pop(chapter.id, None))

    def on_chapter_title_changed(self, chapter_id: str, new_title: str):
        """Когда изменено название главы в редакторе"""
        for i in range(self.project_tree.topLevelItemCount()):
            item = self.project_tree.topLevelItem(i)
            if isinstance(item, ChapterTreeItem) and item.chapter.id == chapter_id:
                item.update_display()
                break

    def save_all(self):
        """Сохранить всё"""
        if not self.current_project:
            return

        try:
            for sub in self.mdi_area.subWindowList():
                if isinstance(sub.widget(), ChapterEditor):
                    sub.widget().save_chapter()

            if self.current_project.save():
                self.update_stats_display()
                self.statusBar().showMessage("Всё сохранено", 2000)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def export_project(self, format: str):
        """Экспорт проекта"""
        if not self.current_project:
            QMessageBox.warning(self, "Предупреждение", "Сначала откройте проект")
            return

        default_dir = os.path.dirname(self.current_project.path)

        ext = format
        if format == 'fb2':
            ext = 'fb2'

        default_name = f"{self.current_project.name}.{ext}"

        path, _ = QFileDialog.getSaveFileName(
            self,
            f"Экспорт в {format.upper()}",
            os.path.join(default_dir, default_name),
            f"*.{ext}"
        )

        if not path:
            return

        if not path.lower().endswith(f'.{ext}'):
            path += f'.{ext}'

        try:
            if format == 'fb2':
                self.export_fb2(path)
            elif format == 'txt':
                self.export_txt(path)
            elif format == 'pdf':
                self.export_pdf(path)

            reply = QMessageBox.question(
                self,
                "Экспорт завершен",
                f"Проект экспортирован в:\n{path}\n\nОткрыть файл?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                QDesktopServices.openUrl(QUrl.fromLocalFile(path))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка экспорта: {e}")

    def export_fb2(self, path: str):
        """Экспорт в FB2 с поддержкой обложки"""
        try:
            # Создаем корневой элемент с правильными пространствами имен
            root = ET.Element("FictionBook")
            root.set("xmlns", "http://www.gribuser.ru/xml/fictionbook/2.0")
            root.set("xmlns:l", "http://www.w3.org/1999/xlink")  # Добавляем пространство имен для ссылок

            description = ET.SubElement(root, "description")
            title_info = ET.SubElement(description, "title-info")

            # Обложка
            if self.current_project.cover_data:
                coverpage = ET.SubElement(title_info, "coverpage")
                image = ET.SubElement(coverpage, "image")
                # Используем правильный синтаксис для xlink:href
                image.set("{http://www.w3.org/1999/xlink}href", "#cover.jpg")

                # Добавляем бинарные данные
                binary = ET.SubElement(root, "binary")
                binary.set("id", "cover.jpg")

                # Определяем тип изображения по расширению файла
                content_type = "image/jpeg"
                if self.current_project.cover_path:
                    ext = os.path.splitext(self.current_project.cover_path)[1].lower()
                    if ext == '.png':
                        content_type = "image/png"
                    elif ext == '.gif':
                        content_type = "image/gif"
                    elif ext == '.bmp':
                        content_type = "image/bmp"

                binary.set("content-type", content_type)
                binary.text = self.current_project.cover_data

            book_title = ET.SubElement(title_info, "book-title")
            book_title.text = self.current_project.name

            author = ET.SubElement(title_info, "author")
            first_name = ET.SubElement(author, "first-name")
            last_name = ET.SubElement(author, "last-name")

            author_name = self.current_project.settings.get('author', 'Автор')
            if ' ' in author_name:
                parts = author_name.split(' ', 1)
                first_name.text = parts[0]
                last_name.text = parts[1] if len(parts) > 1 else ""
            else:
                first_name.text = author_name
                last_name.text = ""

            lang = ET.SubElement(title_info, "lang")
            lang.text = self.current_project.settings.get('language', 'ru')

            if self.current_project.annotation:
                annotation = ET.SubElement(title_info, "annotation")
                p = ET.SubElement(annotation, "p")
                p.text = self.current_project.annotation

            body = ET.SubElement(root, "body")

            for chapter in self.current_project.chapters:
                section = ET.SubElement(body, "section")

                title = ET.SubElement(section, "title")
                title_p = ET.SubElement(title, "p")
                title_p.text = chapter.title

                # Разбиваем на параграфы по пустым строкам
                paragraphs = chapter.content.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        # Дополнительно разбиваем длинные параграфы на строки
                        lines = para.strip().split('\n')
                        for line in lines:
                            if line.strip():
                                p = ET.SubElement(section, "p")
                                p.text = line.strip()

            # Преобразуем в строку с правильной обработкой пространств имен
            xml_str = ET.tostring(root, encoding='utf-8', method='xml')

            # Используем minidom для форматирования
            dom = xml.dom.minidom.parseString(xml_str)
            pretty_xml = dom.toprettyxml(indent="  ", encoding='utf-8')

            # Добавляем XML декларацию вручную (minidom иногда ее портит)
            if pretty_xml.startswith(b'<?xml'):
                # Уже есть декларация
                pass
            else:
                pretty_xml = b'<?xml version="1.0" encoding="utf-8"?>\n' + pretty_xml

            with open(path, 'wb') as f:
                f.write(pretty_xml)

            print(f"FB2 успешно экспортирован в {path}")

        except Exception as e:
            print(f"Ошибка экспорта в FB2: {e}")
            import traceback
            traceback.print_exc()
            raise

    def export_txt(self, path: str):
        """Экспорт в TXT"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f"{self.current_project.name}\n")
                f.write(f"Автор: {self.current_project.settings.get('author', 'Автор')}\n")
                if self.current_project.cover_path:
                    f.write(f"Обложка: {os.path.basename(self.current_project.cover_path)}\n")
                f.write("="*60 + "\n\n")

                for chapter in self.current_project.chapters:
                    f.write(f"\n\n{chapter.title}\n")
                    f.write("-"*40 + "\n\n")
                    f.write(chapter.content)
                    f.write("\n\n")
        except Exception as e:
            print(f"Ошибка экспорта в TXT: {e}")
            raise

    def export_pdf(self, path: str):
        """Экспорт в PDF с поддержкой обложки"""
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(path)

            doc = QTextDocument()

            html = "<html><body>"

            # Добавляем обложку если есть
            if self.current_project.cover_path:
                html += f'<div style="text-align: center; margin: 50px;">'
                html += f'<img src="file:///{self.current_project.cover_path}" style="max-width: 400px; max-height: 600px;">'
                html += f'</div>'
                html += '<div style="page-break-after: always;"></div>'

            html += f"<h1 style='text-align: center;'>{self.current_project.name}</h1>"
            html += f"<p style='text-align: center;'><i>{self.current_project.settings.get('author', 'Автор')}</i></p>"
            html += "<hr/>"

            for chapter in self.current_project.chapters:
                html += f"<h2>{chapter.title}</h2>"
                text = chapter.content.replace('\n', '<br>')
                html += f"<p>{text}</p>"
                html += "<div style='page-break-after: always;'></div>"

            html += "</body></html>"

            doc.setHtml(html)
            doc.print_(printer)
        except Exception as e:
            print(f"Ошибка экспорта в PDF: {e}")
            raise

    def search_text(self, text: str):
        """Поиск по проекту"""
        if not self.current_project or len(text) < 3:
            self.search_results.clear()
            return

        try:
            self.search_results.clear()

            for chapter in self.current_project.chapters:
                if text.lower() in chapter.content.lower():
                    pos = chapter.content.lower().find(text.lower())
                    start = max(0, pos - 30)
                    end = min(len(chapter.content), pos + len(text) + 30)
                    preview = chapter.content[start:end]

                    item = QListWidgetItem(f"{chapter.title}: ...{preview}...")
                    item.setData(Qt.ItemDataRole.UserRole, (chapter.id, pos))
                    self.search_results.addItem(item)
        except Exception as e:
            print(f"Ошибка поиска: {e}")

    def goto_search_result(self, item):
        """Перейти к результату поиска"""
        try:
            chapter_id, pos = item.data(Qt.ItemDataRole.UserRole)

            for sub in self.mdi_area.subWindowList():
                if isinstance(sub.widget(), ChapterEditor):
                    if sub.widget().chapter.id == chapter_id:
                        sub.show()
                        sub.raise_()
                        editor = sub.widget().editor
                        cursor = editor.textCursor()
                        cursor.setPosition(pos)
                        cursor.setPosition(pos + len(self.search_input.text()),
                                          QTextCursor.MoveMode.KeepAnchor)
                        editor.setTextCursor(cursor)
                        return

            chapter = self.current_project.get_chapter(chapter_id)
            if chapter:
                temp_item = ChapterTreeItem(chapter)
                self.open_chapter(temp_item)
        except Exception as e:
            print(f"Ошибка перехода к результату: {e}")

    def closeEvent(self, event):
        """При закрытии"""
        try:
            if self.current_project:
                reply = QMessageBox.question(
                    self,
                    "Подтверждение",
                    "Сохранить изменения перед выходом?",
                    QMessageBox.StandardButton.Yes |
                    QMessageBox.StandardButton.No |
                    QMessageBox.StandardButton.Cancel
                )

                if reply == QMessageBox.StandardButton.Yes:
                    self.save_all()
                    event.accept()
                elif reply == QMessageBox.StandardButton.No:
                    event.accept()
                else:
                    event.ignore()
            else:
                event.accept()
        except Exception as e:
            print(f"Ошибка при закрытии: {e}")
            event.accept()

# === ЗАПУСК ===
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Читалка-писалка Pro")
    app.setOrganizationName("ChitalkaPisalka")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
