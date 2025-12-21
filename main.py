"""Импортировать библиотеку Pygame."""
import pygame

from random import randint

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

SCREEN_CENTER_X, SCREEN_CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Направления движения ракетки:
LEFT = -1
RIGHT = 1

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (24, 24, 24)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет мячика
BALL_COLOR = (182, 216, 3)

# Цвет ракетки
RACKET_COLOR = (0, 255, 0)

# Частота обновления цикла программы:
FPS = 60

# Скорость передвижения ракетки.
SPEED_RACKET = 5

# Размер секции ракетки.
SIDE = 20

# Количество секций ракетки.
LENGTH = 6

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Теннис')

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

    def __init__(self):
        """Инициализируем обект 'ракетка'."""
        super().__init__()
        self.body_color = RACKET_COLOR
        self.reset_racket()
        self.direction = None

    def move(self):
        """Метод обновляет позицию ракетки."""
        # Если нажали кнопку влево.
        if self.direction == LEFT and self.positions[0][0] > 0:
            for i in range(len(self.positions)):
                self.positions[i] = (
                    self.positions[i][0] - SPEED_RACKET,
                    self.positions[i][1]
                    )
        # Иначе если нажали кнопку вправо.
        elif (self.direction == RIGHT and
              self.positions[0][0] < SCREEN_WIDTH - SIDE * LENGTH):
            for i in range(len(self.positions)):
                self.positions[i] = (
                    self.positions[i][0] + SPEED_RACKET,
                    self.positions[i][1]
                    )

    def draw(self):
        """Метод draw класса Snake."""
        for position in self.positions:
            rect = (pygame.Rect(position, (SIDE, SIDE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset_racket(self):
        """Метод установливает ракетку в начальное положение."""
        self.positions = [(x + SCREEN_CENTER_X - SIDE * LENGTH // 2,
                           SCREEN_HEIGHT - SIDE)
                          for x in range(0, LENGTH * SIDE, SIDE)]


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
                object.direction = LEFT
            # обработка нажатия клавиши СТРЕЛКА_ВПРАВО
            if event.key == pygame.K_RIGHT:
                object.direction = RIGHT
        if event.type == pygame.KEYUP:
            # обработка отпускания клавиши СТРЕЛКА_ВЛЕВО
            if event.key == pygame.K_LEFT:
                object.direction = None
            # обработка нажатия клавиши СТРЕЛКА_ВПРАВО
            if event.key == pygame.K_RIGHT:
                object.direction = None


def main():
    """Основная функция main."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    ball = Ball()
    racket = Racket()
    # square = Square(screen, (0, 255, 0), 450, 200, 100)
    # triangle = Triangle(screen, (0, 0, 255), [(150, 200), (50, 300),
    # (250, 300)])

    running = True
    while running:
        # Проверяем нажатие кнопок.
        handle_keys(racket)
        # Делаем фон черным.
        screen.fill((0, 0, 0))
        # Обновляем позицию мячика.
        ball.move()
        # Обновляем позицию ракетки.
        racket.move()
        # Проверяем столкновения с границами.
        ball.check_border()
        # Рисуем мяч.
        ball.draw()
        # Рисуем ракетку.
        racket.draw()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
