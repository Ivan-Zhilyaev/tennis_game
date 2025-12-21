"""Импортировать библиотеку Pygame."""
import pygame

from random import randint

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER_X, SCREEN_CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (24, 24, 24)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет мячика
BALL_COLOR = (182, 216, 3)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Частота обновления цикла программы:
FPS = 60

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс GameObject."""

    def __init__(self):
        """Инициализируем обект класса."""
        self.position = (SCREEN_CENTER_X, SCREEN_CENTER_Y)
        self.color = None

    def draw(self):
        """Метод для отрисовки объекта."""
        pass


class Ball(GameObject):
    """Наследуемый класс Ball."""

    def __init__(self, radius=15, speed=2):
        """Инициализируем обект 'мячик'."""
        super().__init__()
        self.position = (randint(0, SCREEN_WIDTH), radius)
        self.color = BALL_COLOR
        self.radius = radius
        self.speed = speed
        # Добавляем отдельные рандомные направления для X и Y
        self.dx = 1 if randint(0, 1) == 0 else -1
        self.dy = 1 if randint(0, 1) == 0 else -1

    def draw(self):
        """Отрисовка обекта 'мячик'."""
        pygame.draw.circle(screen,
                           self.color,
                           self.position,
                           self.radius)
        pygame.draw.circle(screen,
                           BORDER_COLOR,
                           self.position,
                           self.radius + 2, 2)

    def move(self):
        """Меняем положение 'мячика' на игровом поле."""
        # Получение стартовой позиции 'мячика'
        self.x, self.y = self.position
        # Изменение положения 'мячика' в зависимости от направления движения
        self.x += self.speed * self.dx
        self.y += self.speed * self.dy

    def check_border(self):
        """Проверяем столкновения 'мячика' с границами поля и объектами."""
        # Вертикальные границы поля
        if self.x + self.radius >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.dx = -1
        elif self.x - self.radius <= 0:
            self.x = self.radius
            self.dx = 1
        # Горизонтальные границы поля
        if self.y + self.radius >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
            self.dy = -1
        elif self.y - self.radius <= 0:
            self.y = self.radius
            self.dy = 1

        # Обновляем положение 'мячика' в игровом поле.
        self.position = (self.x, self.y)


class Racket(GameObject):
    """Наследуемый класс Racket."""

    def __init__(self, surface, color, x, y, side):
        """Инициализируем обект 'ракетка'."""
        super().__init__(surface, color)
        self.x = x
        self.y = y
        self.side = side

    def draw(self):
        """Отрисовка обекта 'ракетка'."""
        pygame.draw.rect(self.surface, self.color,
                         pygame.Rect(self.x, self.y, self.side, self.side))


class Triangle(GameObject):
    """PASS."""

    def __init__(self, surface, color, points):
        """PASS."""
        super().__init__(surface, color)
        self.points = points

    def draw(self):
        """PASS."""
        pygame.draw.polygon(self.surface, self.color, self.points)


def handle_keys(object):
    """Обработка нажатий кнопок на клавиатуре пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        # Добавляем возможность выхода по ESC
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
        if event.type == pygame.KEYDOWN:
            # обработка нажатия клавиши СТРЕЛКА_ВЛЕВО
            if event.key == pygame.K_LEFT:
                object.direction = -1
            # обработка нажатия клавиши СТРЕЛКА_ВПРАВО
            if event.key == pygame.K_RIGHT:
                object.direction = 1


def main():
    """Основная функция main."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    ball = Ball()
    # square = Square(screen, (0, 255, 0), 450, 200, 100)
    # triangle = Triangle(screen, (0, 0, 255), [(150, 200), (50, 300),
    # (250, 300)])

    running = True
    while running:
        # Проверяем нажатие кнопок.
        handle_keys(ball)
        # Делаем фон черным.
        screen.fill((0, 0, 0))
        # Обновляем позицию.
        ball.move()
        # Проверяем столкновения с границами.
        ball.check_border()
        # Рисуем.
        ball.draw()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
