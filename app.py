import pygame
from random import randint
from pygame import Color
from greedy import Greedy
from Controler import Controler
from Params import *

pygame.init()

WIDTH, HEIGHT = [i*CELL_WIDTH for i in GRID_SIZE]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game = pygame.Surface((WIDTH, HEIGHT))

sm_font = pygame.font.SysFont('Roboto', 20, True, True)

clock = pygame.time.Clock()
dt = 0


fps=base_fps

EYE_WIDTH = CELL_WIDTH // 5
CELL_CENTER = CELL_WIDTH // 2

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

FOOD_CLR = Color(255, 255, 255)
CELL_CLR = Color(0, 255, 0)
EYE_CLR = Color(0, 125, 125)
SCORE_CLR = Color(255, 255, 255)

def adj_cells(x, y):
    adj = []
    adj.append((x-1, y)) if x >  0 else ""
    adj.append((x+1, y)) if x < GRID_SIZE[0]-1 else ""
    adj.append((x, y-1)) if y > 0 else ""
    adj.append((x, y+1)) if y < GRID_SIZE[1]-1  else ""
    return adj
    

def random_point():
    return (randint(0, GRID_SIZE[0] -1 ), randint(0, GRID_SIZE[1] -1 ))

def get_cords(pos):
    return [i*CELL_WIDTH for i in pos]

def get_center(pos):
    return [i*CELL_WIDTH + CELL_CENTER for i in pos]

if __name__ == "__main__":

    food_pos = random_point()
    score = INIT_LEN

    class BodyCell:
        def __init__(self, pos:tuple, is_head=True, n = 1):
            self.pos = pos
            self.rect = pygame.Rect(pos[0]*CELL_WIDTH-1, pos[1]*CELL_WIDTH-1, CELL_WIDTH-2, CELL_WIDTH-2)
            self.next = None
            self.old_pos = pos
            if is_head:
                self.dir = LEFT
            for _ in range(n-1):
                self.append()

        def draw(self):
            pygame.draw.rect(game, CELL_CLR, self.rect)
            if hasattr(self, 'dir'):
                means =  [self.rect.x + 2*EYE_WIDTH, self.rect.y + 2*EYE_WIDTH]
                e_pos = ((means[i] + d*EYE_WIDTH if d else means[i] + factor*EYE_WIDTH for i, d in enumerate(self.dir)) for factor in [-1, 1])
                [pygame.draw.rect(game, EYE_CLR, pygame.Rect(x, y, EYE_WIDTH, EYE_WIDTH)) for x, y in e_pos]

            if self.next:
                self.next.draw()
        
        def move_to(self, x:int, y:int, head_pos=None):            
            if head_pos is None:
                if not (0 <= x < GRID_SIZE[0] and 0 <= y < GRID_SIZE[1]):
                    raise ValueError("Died")
                
            elif head_pos == (x, y):
                raise ValueError("Died")
            
            self.old_pos = self.pos
            self.pos = (x, y)

            self.rect.x, self.rect.y = get_cords((x, y))

            if self.next:
                self.next.move_to(*self.old_pos, head_pos if head_pos is not None else (x, y))

            global food_pos, score
            if food_pos == self.pos:
                food_pos = random_point()
                if head_pos is None:
                    score += 1
                    self.append()
                    

        def move(self):
            self.move_to(*[self.pos[i] + self.dir[i] for i in range(2)], None)

        def append(self, next = None):
            next = BodyCell(self.pos, is_head=False) if next is None else next
            if self.next:
                self.next.append(next)
            else:
                self.next = next
        
        def turn(self, dir):
            dx, dy = self.dir 
            if dir != (-dx, -dy):
                self.dir = dir

        def body(self):
            current = self
            body = []
            while current:
                body.insert(0, current.pos)
                current = current.next
            return body

    CLOSED = 0
    ACTIVE = 1
    PAUSED = 2
    DEAD = 3

    STATE = PAUSED

    
    HUMAN = 0
    GREEDY = 1
    CONTROLER = 2
    AI = CONTROLER


    snake = BodyCell(init_pos, n = INIT_LEN)

    greedy = Greedy(*GRID_SIZE)
    controler = Controler(*GRID_SIZE, snake)

    while STATE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                STATE = CLOSED

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_f]:
            print(f"Food: {food_pos}")

        if keys[pygame.K_p]:
            print(f"Snake: {snake.pos}")

        if keys[pygame.K_b]:
            print(f"Body: {snake.body()}")

        if keys[pygame.K_t]:
            print(f"Delta Time: {dt}")

        if keys[pygame.K_RALT]:
            fps = alt_fps

        if keys[pygame.K_RCTRL]:
            fps = base_fps

        if keys[pygame.K_RETURN]:
            if STATE == PAUSED:
                STATE = ACTIVE
            elif STATE == DEAD:
                del snake
                snake = BodyCell(init_pos, n = INIT_LEN)
                score = 0
                food_pos = random_point()
                STATE = ACTIVE
        
        if keys[pygame.K_SPACE] and STATE == ACTIVE:
            STATE = PAUSED



        if STATE == ACTIVE:
            if not AI:
                if keys[pygame.K_w]:
                    snake.turn(UP)
                elif keys[pygame.K_s]:
                    snake.turn(DOWN)
                elif keys[pygame.K_a]:
                    snake.turn(LEFT)
                elif keys[pygame.K_d]:
                    snake.turn(RIGHT)

                    
            elif AI == GREEDY:
                snake.turn(greedy.choose(snake.pos, food_pos, snake.body(), 5))
                # snake.turn(greedy.cycle(snake.pos))

            elif AI == CONTROLER:
                controler.move(food_pos)


            try:
                snake.move()
            except Exception as e:
                if str(e) != "Died":
                    raise e

                STATE = DEAD

        game.fill("purple")
        snake.draw()
        pygame.draw.circle(game, FOOD_CLR, get_center(food_pos), CELL_CENTER)
        game.blit(sm_font.render(f"{score}", 1, SCORE_CLR), SCORE_CORDS)

        screen.blit(game, (0, 0))
        
        pygame.display.flip()

        dt = clock.tick(fps) / 1000

    pygame.quit()
