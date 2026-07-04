import os
import json
from datetime import datetime
from typing import List, Dict

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

class Theme:
    """Класс для работы с темами оформления"""
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

class Settings:
    """Настройки приложения"""
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
