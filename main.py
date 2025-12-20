"""Импортировать библиотеку Pygame."""
import pygame

# from random import randint


class GameObject:
    """Родительский класс GameObject."""

    def __init__(self, surface, color):
        """Инициализируем обект класса."""
        self.surface = surface
        self.color = color

    def draw(self):
        """Метод для отрисовки объекта."""
        pass


class Circle(GameObject):
    """Наследуемый класс Circle."""

    def __init__(self, surface, color, x, y, radius, speed):
        """Инициализируем обект 'мячик'."""
        super().__init__(surface, color)
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = 1

    def draw(self):
        """Отрисовка обекта 'мячик'."""
        pygame.draw.circle(self.surface,
                           self.color,
                           (self.x, self.y),
                           self.radius)

    def move(self):
        """Меняем положение 'мячика' на игровом поле."""
        self.x += self.speed * self.direction

    def check_border(self):
        """Проверяем столкновения 'мячика' с границами поля и ракеткой."""
        if self.x + self.radius >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.direction = -1
        elif self.x - self.radius <= 0:
            self.x = self.radius
            self.direction = 1


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


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER_X, SCREEN_CENTER_Y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
FPS = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Установить заголовок окна.
pygame.display.set_caption('Бешеный Питон')
clock = pygame.time.Clock()

circle = Circle(screen, (255, 0, 0), SCREEN_CENTER_X, SCREEN_CENTER_Y, 40, 10)
# square = Square(screen, (0, 255, 0), 450, 200, 100)
# triangle = Triangle(screen, (0, 0, 255), [(150, 200), (50, 300), (250, 300)])


def main():
    """Основная функция main."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.

    running = True
    while running:
        # Проверяем нажатие кнопок.
        handle_keys(circle)
        # Делаем фон черным.
        screen.fill((0, 0, 0))
        # Обновляем позицию.
        circle.move()
        # Проверяем столкновения с вертикальными границами.
        circle.check_border()
        # Рисуем.
        circle.draw()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
