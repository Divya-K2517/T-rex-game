import pygame
import sys
import random 
import time

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

class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.image = pygame.image.load("T-rex game/cactus.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT
        self.rect.right = WIDTH
        self.speed = speed
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def update(self):
        self.rect.left -= self.speed
        if self.rect.right <= 0:
            self.kill()

class Dino():
    def __init__(self):
        self.image = pygame.image.load("T-rex game/dino.png")
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.left = 10
        self.rect.bottom = int(HEIGHT*0.96) 
    def draw(self):
        screen.blit(self.image, self.rect)
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: #press space bar to make dino jump
            self.rect.bottom = int(HEIGHT*0.96) - 120
        elif not keys[pygame.K_UP]:
            self.rect.bottom = int(HEIGHT*0.96) 

def checkcollsion(a, b): #a is the dino/stationary object, b is the cactus
    if a.rect.left >= b.rect.left and a.rect.bottom >= b.rect.top:
        return True
    else:
        return False


#objects
ground = Ground()
dino = Dino()
cacti = pygame.sprite.Group()
cactus = Cactus()
cacti.add(cactus)

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

    if len(cacti) < 3:
        if len(cacti) == 0:
            cacti.add(Cactus())
        else:
            for c in cacti:
                if c.rect.right < WIDTH*0.6 and random.randint(0,50) == 10:
                    new_cactus = Cactus()
                    cacti.add(new_cactus)
                    if random.randint(0,40) == 10:
                        new_cactus2 = new_cactus
                        new_cactus2.rect.left = new_cactus.rect.right
                        cacti.add(new_cactus2)
            

    cacti.draw(screen)
    cacti.update()

    dino.draw()
    dino.update()

    for c in cacti:
        if checkcollsion(dino, c):
            print ("collsion detected")

    

    pygame.display.flip() #updates display

#quites pygame and closes the window
pygame.quit()
sys.exit()
