import pygame
import sys
import random

SCREENWIDTH = 640
SCREENHEIGHT = 480
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

CAR_WIDTH = 50
CAR_HEIGHT = 30
CAR_SPEED = 5

OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 20
OBSTACLE_COLOR = (255, 0, 0)

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('car.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREENWIDTH / 2
        self.rect.centery = SCREENHEIGHT / 2
        self.speed = CAR_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('obstacle.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREENWIDTH - OBSTACLE_WIDTH)
        self.rect.y = -OBSTACLE_HEIGHT

    def update(self):
        self.rect.y += 5
        if self.rect.y > SCREENHEIGHT:
            self.rect.x = random.randint(0, SCREENWIDTH - OBSTACLE_WIDTH)
            self.rect.y = -OBSTACLE_HEIGHT

def draw_score(screen, score):
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

def draw_button(screen, text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    font = pygame.font.SysFont(None, 36)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)

def game_intro(screen):
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 72)
        text = font.render("Obstacle Tackle", True, WHITE)
        text_rect = text.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2 - 50))
        screen.blit(text, text_rect)
        draw_button(screen, "Start", SCREENWIDTH / 2 - 50, SCREENHEIGHT / 2, 100, 50, GREEN, RED, main)
        pygame.display.update()

def game_over(screen, score):
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 72)
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2 - 50))
        screen.blit(text, text_rect)
        draw_score(screen, score)
        draw_button(screen, "Restart", SCREENWIDTH / 2 - 50, SCREENHEIGHT / 2 + 50, 100, 50, GREEN, RED, main)
        pygame.display.update()

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Obstacle Tackle')
    clock = pygame.time.Clock()
    road_image = pygame.image.load('road.png').convert()
    road_image = pygame.transform.scale(road_image, (SCREENWIDTH, SCREENHEIGHT))
    car = Car()
    obstacles = pygame.sprite.Group()
    for _ in range(5):
        obstacles.add(Obstacle())
    score = 0
    road_y = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        car.update()
        obstacles.update()
        for obstacle in obstacles:
            if obstacle.rect.y == SCREENHEIGHT:
                score += 1
        road_y += 5
        if road_y >= SCREENHEIGHT:
            road_y = 0
        screen.blit(road_image, (0, road_y))
        screen.blit(road_image, (0, road_y - SCREENHEIGHT))
        screen.blit(car.image, car.rect)
        obstacles.draw(screen)
        draw_score(screen, score)
        if pygame.sprite.spritecollide(car, obstacles, True):
            game_over(screen, score)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    game_intro(screen)
