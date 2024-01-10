import pygame
import random

def genrate_food(snake):
        error = True
        x = 0
        y = 0
        while error:
            error = False
            x = random.randint(0, cell_count - 1)
            y = random.randint(0, cell_count - 1)
            for i in snake.body:
                if (i.x  == x * cell_size and i.y == y * cell_size):
                    error = True
                    break
        return Food(x, y)

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = pygame.math.Vector2(self.x * cell_size, self.y * cell_size)

    def draw(self):
        x_pos = self.pos.x
        y_pos = self.pos.y
        food_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        pygame.draw.rect(screen, "yellow", food_rect)    

class Snake:
    def __init__(self, x, y):
        head_pos= pygame.math.Vector2(x * cell_size, y * cell_size)
        self.body = [head_pos]
        self.direction = pygame.math.Vector2(0, 1 * cell_size)
    
    def draw_snake(self):
        for i in range(len(self.body)):
            x_pos = self.body[i].x
            y_pos = self.body[i].y
            i_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            str = "red"
            pygame.draw.rect(screen, str, i_rect)
    
    def append_snake(self):
        new_body = self.body
        direction = self.direction
        if len(self.body) > 1: 
            direction = new_body[-2] - new_body[-1]
        last = new_body[len(new_body) - 1] + direction
        new_body.append(last)
        self.body = new_body
    
    def move(self):
        new_body = self.body[:-1]     
        new_body.insert(0, self.body[0] + self.direction)
        self.body = new_body
    
    def change_direction(self, str):
        direction = self.direction
        if str == "down":
            self.direction = pygame.math.Vector2(0, 1 * cell_size)
        elif str == "up":
            self.direction = pygame.math.Vector2(0, -1 * cell_size)
        elif str == "right":
            self.direction = pygame.math.Vector2(1 * cell_size, 0)
        elif str == "left":
            self.direction = pygame.math.Vector2(-1 * cell_size, 0)
        head = self.body[0] + self.direction
        if len(self.body) != 1 and head == self.body[1]:
            self.direction = direction

pygame.init()
pygame.font.init()
cell_size = 30
cell_count = 20
screen = pygame.display.set_mode((cell_size * cell_count, cell_size * cell_count))
clock = pygame.time.Clock()
running = True
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 500)
font = pygame.font.SysFont("impact", 35)

snake = Snake(0, 2)
food = genrate_food(snake)

while running:
    
    screen.fill("green")
    
    food.draw()

    snake.draw_snake()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == timer_event:
            snake.move()
            if snake.body[0].x < 0 or snake.body[0].x + cell_size> cell_size * cell_count or snake.body[0].y < 0 or snake.body[0].y + cell_size > cell_size * cell_count:
                running = False
            else:    
                for i in snake.body[1:]:
                    if snake.body[0] == i:
                        running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        snake.change_direction("up")
    if keys[pygame.K_s]:
        snake.change_direction("down")
    if keys[pygame.K_a]:
        snake.change_direction("left")
    if keys[pygame.K_d]:
        snake.change_direction("right")

    if snake.body[0] == food.pos:
        snake.append_snake()
        food = genrate_food(snake)
    
    score_text = str(len(snake.body) - 1)
    score_surface = font.render(score_text,True,(56,74,12))
    score_x = cell_size
    score_y = cell_size
    score_rect = score_surface.get_rect(center = (score_x,score_y))
    screen.blit(score_surface, score_rect)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()