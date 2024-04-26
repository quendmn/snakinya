import pygame
import sys
import random
import pygame_menu

pygame.init()
background = "background.png"
surf = pygame.Surface((460, 530))

FRAME_COLOR = [255, 188, 217]
WHITE = [255, 255, 255] # йоо миста ваайт
PINK = [255, 240, 246]
GREEN = [170, 240, 209]
GREY = [125, 127, 125]
SIZE_BLOCK = 20
COUNT_BLOCKS = 20
MARGIN = 1
HEADER_COLOR = [255, 188, 217]
HEADER_MARGIN = 70
SNAKINYA_COLOR = [179, 127, 179]

size = (SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("snakinya coquette")
timer = pygame.time.Clock()
font = pygame.font.SysFont('arial', 48)

# класс змейки (coquette)
class SnakinyaBlock:
    # конструктор
    def __init__(self, x, y):
        self.x = x
        self.y = y
    # внутри поля или нет
    def isInside(self):
        return 0 <= self.x < SIZE_BLOCK and 0 <= self.y < SIZE_BLOCK

    # сравнение c положением другого объекта
    def __eq__(self, other):
        return isinstance(other, SnakinyaBlock) and self.x == other.x and self.y == other.y


def start():

    # отрисовка квадратов
    def drawBlock(color, row, column):
        pygame.draw.rect(screen, color, (SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                         HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                         SIZE_BLOCK, SIZE_BLOCK))

    # сама змейка
    snakeBlock = [SnakinyaBlock(9, 8), SnakinyaBlock(9, 9), SnakinyaBlock(9, 10)]

    # блок в рандомном месте
    def getRandomBlock():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        emptyBlock = SnakinyaBlock(x, y)
        while emptyBlock in snakeBlock:
            emptyBlock.x = random.randint(0, COUNT_BLOCKS - 1)
            emptyBlock.y = random.randint(0, COUNT_BLOCKS - 1)
        return emptyBlock

    timer = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 36)

    total = 0
    speed = 2
    apple = getRandomBlock()
    d_row = 0
    d_col = 1
    total = 0
    speed = 2

    # процесс игры
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # игра
            elif event.type == pygame.KEYDOWN:
                # управление
                if event.key == pygame.K_UP and d_col != 0:
                    d_row -= 1
                    d_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col -= 1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1
                elif event.key == pygame.K_RIGHT and event.key == pygame.K_LEFT and event.key == pygame.K_DOWN and event.key == pygame.K_UP and d_row != 0 and d_col != 0:
                    d_row -= 1
                    d_col = 0
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        # вывод очков
        total_text = font.render(f"total: {total}", False, WHITE)
        screen.blit(total_text, (SIZE_BLOCK, SIZE_BLOCK))


        # coquette фон
        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) %2 == 0:
                    color = PINK
                else:
                    color = WHITE
                drawBlock(color, row, column)

        head = snakeBlock[-1]

        # выход, если змейка не внутри поля
        if not head.isInside():
            start()

        #яблоки
        drawBlock(GREEN, apple.x, apple.y)
        #отрисовка змейки
        for block in snakeBlock:
            drawBlock(SNAKINYA_COLOR, block.x, block.y)

        # если змеища съела яблоко
        if apple == head:
            total += 1
            speed = total // 5 + 2
            snakeBlock.append(apple)
            apple = getRandomBlock()

        #змеиная голова
        head = snakeBlock[-1]
        newHead = SnakinyaBlock(head.x + d_row, head.y + d_col)
        if newHead in snakeBlock:
            pass

        snakeBlock.append(newHead)
        snakeBlock.pop(0)

        pygame.display.flip()
        timer.tick(speed+1)

# менюшка
mytheme = pygame_menu.Theme(background_color='white',
                title_background_color= 'white',
                title_font_color= PINK,
                title = False,
                title_font_shadow=False,
                title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE,
                widget_padding=0)
myimage = pygame_menu.baseimage.BaseImage(
    image_path=background,
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
)
mytheme.background_color = myimage

menu = pygame_menu.Menu('halooo', 460, 530,
                       theme=mytheme)
butt = menu.add.button('playy', start)
butt.set_background_color('pink')
butt.set_font('arial', 56, 'pink', 'pink', 'pink', 'pink', 'white')
menu.mainloop(screen)