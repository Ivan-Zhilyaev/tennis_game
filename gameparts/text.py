"""Модуль для отображения текста."""

from main import SCREEN_WIDTH


class Text:
    """Класс для отображения текста."""

    def __init__(self, text, font, color, x, y):
        """Инициализация класса."""
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y

    def draw(self, surface):
        """Отображение текста."""
        text_surface = self.font.render(self.text, True, self.color)
        surface.blit(text_surface, (self.x, self.y))
        return text_surface.get_rect()

    def update(self, text):
        """Обновление текста."""
        self.text = text

    def left_edge(self, margin=10):
        """Устанавливает отступ текста от левого верхнего угла."""
        self.x = margin
        self.y = margin

    def right_edge(self, margin=10):
        """Устанавливает отступ текста от левого верхнего угла."""
        self.y = margin
        self.x = SCREEN_WIDTH - margin
