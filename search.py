# search.py
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtWidgets import QListWidgetItem


class SearchEngine(QObject):
    result_found = pyqtSignal(object)  # SearchResult

    def __init__(self, project):
        super().__init__()
        self.project = project
        self.results = []

    def search(self, query: str):
        self.results.clear()
        if len(query) < 2:
            return

        for chapter in self.project.chapters:
            content = chapter.content.lower()
            query_lower = query.lower()
            start = 0
            while True:
                pos = content.find(query_lower, start)
                if pos == -1:
                    break

                # Контекст вокруг найденного
                context_start = max(0, pos - 40)
                context_end = min(len(chapter.content), pos + len(query) + 40)
                context = chapter.content[context_start:context_end]

                self.results.append({
                    'chapter_id': chapter.id,
                    'chapter_title': chapter.title,
                    'position': pos,
                    'context': context,
                    'query': query
                })
                start = pos + len(query)

        for result in self.results:
            self.result_found.emit(result)
