import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1000, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("T-rex game")
clock = pygame.time.Clock()
running = True

class Ground():
    def __init__(self, speed=5):
        self.image1, self.image2 = pygame.image.load("T-rex game/ground.png"), pygame.image.load("T-rex game/ground.png")
        self.rect1, self.rect2 = self.image1.get_rect(), self.image2.get_rect()
        self.rect1.bottom, self.rect2.bottom = HEIGHT, HEIGHT
        self.rect1.left = 0
        self.rect2.left = self.rect1.right
        self.speed = speed
    def draw(self):
        screen.blit(self.image1, self.rect1)
        screen.blit(self.image2, self.rect2)
    def update(self):
        self.rect1.left -= self.speed
        self.rect2.left -= self.speed

        if self.rect1.right < 0:
            self.rect1.left = self.rect2.right
        if self.rect2.right < 0:
            self.rect2.left = self.rect1.right
#objects
ground = Ground()

#main loop
while running:
    dt = clock.tick(60)/1000  #time passed since last frame
    #so the user can close the game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    screen.fill((255,255,255))
    #game code
    ground.draw()
    ground.update()

    pygame.display.flip() #updates display

#quites pygame and closes the window
pygame.quit()
sys.exit()
