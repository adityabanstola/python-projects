import pygame 
import sys
import os
import random 
import math

pygame.init()
pygame.display.set_caption("Snake game")
pygame.font.init()

# Define global constants
score_msg = "Score: 0"
SPEED = 0.30
SNAKE_SIZE = 9
APPLE_SIZE = SNAKE_SIZE
SEPARATION = 10
SCREEN_HEIGHT = 600 
SCREEN_WIDTH = 800 
FPS = 25 
KEY = {"UP":1, "DOWN":2, "LEFT":3, "RIGHT":4}

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE)
score_font = pygame.font.Font(None, 38)
score_numb_font = pygame.font.Font(None, 28)
game_over_font = pygame.font.Font(None, 48)
play_again_font = score_numb_font
score_msg_size = score_font.size("Score")
background_color = pygame.Color(0, 0, 0)

gameClock = pygame.time.Clock()

def checkCollision(posA, As, posB, Bs):
    if posA.x < posB.x + Bs and posA.x + As > posB.x and posA.y < posB.y + Bs and posA.y + As > posB.y:
        return True
    return False

def checkLimits(snake):
    if snake.x > SCREEN_WIDTH:
        snake.x = SNAKE_SIZE
    if snake.x < 0:
        snake.x = SCREEN_WIDTH - SNAKE_SIZE
    if snake.y > SCREEN_HEIGHT:
        snake.y = SNAKE_SIZE
    if snake.y < 0:
        snake.y = SCREEN_HEIGHT - SNAKE_SIZE

class Apple:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.color.Color("orange")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, APPLE_SIZE, APPLE_SIZE), 0)

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.color = "white"

class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.stack = [self]
        blackBox = Segment(self.x, self.y + SEPARATION)
        blackBox.color = "NULL"
        self.stack.append(blackBox)

    def move(self):
        last_element = len(self.stack) - 1
        while last_element != 0:
            self.stack[last_element].direction = self.stack[last_element - 1].direction
            self.stack[last_element].x = self.stack[last_element - 1].x
            self.stack[last_element].y = self.stack[last_element - 1].y
            last_element -= 1
        last_segment = self.stack[0]
        if self.direction == KEY["UP"]:
            last_segment.y -= SPEED * FPS
        elif self.direction == KEY["DOWN"]:
            last_segment.y += SPEED * FPS
        elif self.direction == KEY["LEFT"]:
            last_segment.x -= SPEED * FPS
        elif self.direction == KEY["RIGHT"]:
            last_segment.x += SPEED * FPS
        self.stack.insert(0, last_segment)

    def grow(self):
        last_element = len(self.stack) - 1
        last_segment = self.stack[last_element]
        newSegment = Segment(last_segment.x, last_segment.y)
        self.stack.append(newSegment)

    def draw(self, screen):
        for segment in self.stack:
            color = pygame.color.Color("green") if segment.color != "NULL" else pygame.color.Color("yellow")
            pygame.draw.rect(screen, color, (segment.x, segment.y, SNAKE_SIZE, SNAKE_SIZE), 0)

def getKey():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return KEY["UP"]
            elif event.key == pygame.K_DOWN:
                return KEY["DOWN"]
            elif event.key == pygame.K_LEFT:
                return KEY["LEFT"]
            elif event.key == pygame.K_RIGHT:
                return KEY["RIGHT"]
            elif event.key == pygame.K_ESCAPE:
                return "exit"
            elif event.key == pygame.K_y:
                return "yes"
            elif event.key == pygame.K_n:
                return "no"
        if event.type == pygame.QUIT:
            sys.exit(0)

def endGame():
    message = game_over_font.render("Game Over", True, pygame.Color("white"))
    message_play_again = play_again_font.render("Play Again? (Y/N)", True, pygame.Color("green"))
    screen.blit(message, (320, 240))
    screen.blit(message_play_again, (320 + 12, 240 + 40))
    pygame.display.flip()

def drawScore(score):
    score_msg_surface = score_font.render("Score:", True, pygame.Color("red"))
    score_numb_surface = score_numb_font.render(str(score), True, pygame.Color("red"))
    screen.blit(score_msg_surface, (SCREEN_WIDTH - score_msg_size[0] - 60, 10))
    screen.blit(score_numb_surface, (SCREEN_WIDTH - 45, 14))

def main():
    score = 0
    mySnake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    startTime = pygame.time.get_ticks()
    apples = [Apple(random.randint(60, SCREEN_WIDTH), random.randint(60, SCREEN_HEIGHT), 1)]

    while True:
        gameClock.tick(FPS)
        screen.fill(background_color)
        keyPress = getKey()

        if keyPress == "exit":
            pygame.quit()
            sys.exit(0)

        if keyPress:
            mySnake.direction = keyPress
        mySnake.move()
        mySnake.draw(screen)

        for apple in apples:
            if apple.state == 1:
                apple.draw(screen)
                if checkCollision(mySnake.stack[0], SNAKE_SIZE, apple, APPLE_SIZE):
                    score += 10
                    mySnake.grow()
                    apple.state = 0

        drawScore(score)
        pygame.display.flip()

main()
