import os
import json
import uuid
import shutil
from datetime import datetime
from typing import List, Dict, Optional
import re
from zipfile import ZipFile
import base64
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from config import Config

class Chapter:
    """Глава проекта"""
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
