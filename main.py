"""Игра 'Теннис' в pg."""
import pygame as pg

from random import randint

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
SCREEN_CENTER_X, SCREEN_CENTER_Y = SCREEN_CENTER

# Направления движения ракетки:
LEFT = -1
RIGHT = 1

BLUE = (0, 0, 228)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50, 50, 50, 180)
YELLOW = (255, 255, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (24, 24, 24)
# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
# Цвет мячика
BALL_COLOR = (182, 216, 3)
# Цвет ракетки
RACKET_COLOR = (0, 0, 255)

# Частота обновления цикла программы:
FPS = 60
# Скорость передвижения ракетки.
SPEED_RACKET = 5
SPEED_BALL = 2
# Размер секции ракетки.
SIDE = 20
# Количество секций ракетки.
LENGTH = 6
TEXT_IDENT = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля:
pg.display.set_caption('Теннис')
# Настройка времени:
clock = pg.time.Clock()


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

    def __init__(self, radius=15, speed=SPEED_BALL):
        """Инициализируем обект 'мячик'."""
        super().__init__()
        self.position = (randint(0, SCREEN_WIDTH), radius)
        self.radius = radius
        self.color = BALL_COLOR
        self.speed = speed
        # Добавляем отдельные рандомные направления для X и Y
        self.dx = 1 if randint(0, 1) == 0 else -1
        self.dy = 1 if randint(0, 1) == 0 else -1

    def draw(self):
        """Отрисовка обекта 'мячик'."""
        pg.draw.circle(screen,
                       self.color,
                       self.position,
                       self.radius)
        pg.draw.circle(screen,
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
        self.ball_drop = False
        self.speed_racket = SPEED_RACKET

    def move(self):
        """Метод обновляет позицию ракетки."""
        # Если нажали кнопку влево.
        if self.direction == LEFT and self.positions[0][0] > 0:
            for i in range(len(self.positions)):
                self.positions[i] = (
                    self.positions[i][0] - self.speed_racket,
                    self.positions[i][1]
                    )
        # Иначе если нажали кнопку вправо.
        elif (self.direction == RIGHT and
              self.positions[0][0] < SCREEN_WIDTH - SIDE * LENGTH):
            for i in range(len(self.positions)):
                self.positions[i] = (
                    self.positions[i][0] + self.speed_racket,
                    self.positions[i][1]
                    )

    def kick(self, ball):
        """Метод отскока мячика от ракетки."""
        # Создадим кортеж с координатами X ракетки.
        racket_coords_x = (x for x in range(self.positions[0][0],
                           self.positions[-1][0] + SIDE))
        # Отскок от ракетки.
        if (ball.y + ball.radius >= SCREEN_HEIGHT - SIDE and
                ball.x in racket_coords_x):
            ball.y = SCREEN_HEIGHT - SIDE - ball.radius
            ball.dy = -1
            return True
        # Столкновение с нижней горизонтальной границей.
        elif (ball.y + ball.radius >= SCREEN_HEIGHT and
                ball.x not in racket_coords_x):
            self.reset_racket()
            ball.position = (randint(0, SCREEN_WIDTH), ball.radius)
            self.ball_drop = True

    def draw(self):
        """Метод draw класса Snake."""
        for position in self.positions:
            rect = (pg.Rect(position, (SIDE, SIDE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset_racket(self):
        """Метод установливает ракетку в начальное положение."""
        self.positions = [(x + SCREEN_CENTER_X - SIDE * LENGTH // 2,
                           SCREEN_HEIGHT - SIDE)
                          for x in range(0, LENGTH * SIDE, SIDE)]


def handle_keys(object, pause_game, start_game):
    """Обработка нажатий кнопок на клавиатуре пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # Добавляем возможность выхода по ESC
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
            # обработка нажатия клавиши СТРЕЛКА_ВЛЕВО
            elif event.key == pg.K_LEFT:
                object.direction = LEFT
            # обработка нажатия клавиши СТРЕЛКА_ВПРАВО
            elif event.key == pg.K_RIGHT:
                object.direction = RIGHT
            elif event.key == pg.K_RETURN:
                pause_game = not pause_game
                start_game = False
        elif event.type == pg.KEYUP:
            # обработка отпускания клавиши СТРЕЛКА_ВЛЕВО
            if event.key == pg.K_LEFT:
                object.direction = None
            # обработка нажатия клавиши СТРЕЛКА_ВПРАВО
            elif event.key == pg.K_RIGHT:
                object.direction = None
    return pause_game, start_game


def start_pause_menu(printable_text='START', font_size=36, color=GREEN):
    """Отрисовывает меню паузы."""
    font = pg.font.Font(None, font_size)
    text = font.render(printable_text, True, color)
    text_rect = text.get_rect(center=SCREEN_CENTER)
    text_bg = pg.Rect(
        SCREEN_WIDTH // 2 - text.get_width() // 2 - 5,
        SCREEN_HEIGHT // 2 - text.get_height() // 2 - 5,
        text.get_width() + 10,
        text.get_height() + 10
    )
    pg.draw.rect(screen, GREY, text_bg)
    screen.blit(text, text_rect)


def draw_menu(score, record_score, speed_ball):
    """Отрисовывает счет."""
    font = pg.font.Font(None, 24)
    text_score = font.render(f'score: {score}', True, GREY)
    screen.blit(text_score, (TEXT_IDENT, TEXT_IDENT))

    text_best_score = font.render(
        f'max: {max(record_score) if record_score else 0}', True, GREY
    )
    screen.blit(
        text_best_score,
        (TEXT_IDENT, TEXT_IDENT + text_score.get_height() + 5)
    )

    text_speed = font.render(f'speed: {speed_ball - SPEED_BALL}', True, GREY)
    screen.blit(
        text_speed,
        (SCREEN_WIDTH - TEXT_IDENT - text_speed.get_width(), TEXT_IDENT)
    )


def main():
    """Основная функция main."""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    ball = Ball()
    racket = Racket()

    fps = FPS
    score = 0
    record_score = []
    speed_ball = SPEED_BALL
    pause_game = True
    start_game = True

    while True:
        pause_game, start_game = handle_keys(racket, pause_game, start_game)
        # Делаем фон черным.
        screen.fill(BLACK)

        if pause_game:
            ball.draw()
            racket.draw()
            draw_menu(score, record_score, speed_ball)
            if start_game:
                start_pause_menu()
            else:
                start_pause_menu(
                    printable_text='PAUSE',
                    font_size=36,
                    color=RED
                )

        else:
            # Обновляем позицию мячика.
            ball.move()
            # Обновляем позицию ракетки.
            racket.move()
            # Проверяем столкновения с границами.
            ball.check_border()
            # Проверяем столкновения мяча с ракеткой.
            if racket.kick(ball):
                score += 1
                if score % 5 == 0:
                    speed_ball += 1
                    ball.speed = speed_ball
                    racket.speed_racket += 1
                    fps -= 1
            if racket.ball_drop:
                score = 0
                speed_ball = SPEED_BALL
                ball.speed = speed_ball
                racket.ball_drop = False
                racket.speed_racket = SPEED_RACKET
                fps = FPS
            score
            record_score.append(score)
            # Рисуем мяч.
            ball.draw()
            # Рисуем ракетку.
            racket.draw()
            # Рисуем текст.
            draw_menu(score, record_score, speed_ball)

        pg.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    main()
