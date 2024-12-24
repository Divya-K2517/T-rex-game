import pygame
import sys
import random 

pygame.init()
WIDTH, HEIGHT = 1000, 300
BASE_SPEED = 5
game_speed = 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("T-rex game")
clock = pygame.time.Clock()
running = True
collision = False

class Ground():
    def __init__(self):
        self.image1, self.image2 = pygame.image.load("T-rex game/ground.png"), pygame.image.load("T-rex game/ground.png")
        self.rect1, self.rect2 = self.image1.get_rect(), self.image2.get_rect()
        self.rect1.bottom, self.rect2.bottom = HEIGHT, HEIGHT
        self.rect1.left = 0
        self.rect2.left = self.rect1.right
    def draw(self):
        screen.blit(self.image1, self.rect1)
        screen.blit(self.image2, self.rect2)
    def update(self):
        global game_speed
        self.rect1.left -= game_speed
        self.rect2.left -= game_speed

        if self.rect1.right < 0:
            self.rect1.left = self.rect2.right
        if self.rect2.right < 0:
            self.rect2.left = self.rect1.right

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("T-rex game/cactus.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT
        self.rect.right = WIDTH
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def update(self):
        global game_speed
        self.rect.left -= game_speed
        if self.rect.right <= 0:
            self.kill()

class Dino():
    def __init__(self):
        self.image = pygame.image.load("T-rex game/dino.png")
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.left = 10
        self.rect.bottom = int(HEIGHT*0.96) 
        self.jumping = False
        self.jump_velocity = 0
        self.gravity = 0.7
        self.score = 0
        self.high_score = 0
        self.font = pygame.font.Font("T-rex game/font.ttf", 15)
    def draw(self):
        screen.blit(self.image, self.rect)
        score_text = self.font.render("Score: " + str(int(self.score)), True, (0,0,0))
        screen.blit(score_text, (WIDTH-140, 20))
        high_score_text = self.font.render("High score: " + str(int(self.high_score)), True, (0,0,0))
        screen.blit(high_score_text, (WIDTH-140, 0))
    def update(self):
        self.score += 0.1
        if self.score > self.high_score:
                self.high_score += 0.1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.jumping: #press space bar to make dino jump
            self.jumping = True
            self.jump_velocity = 15

        if self.jumping:
            self.rect.bottom -= self.jump_velocity
            self.jump_velocity -= self.gravity
            if self.rect.bottom >= int(HEIGHT * 0.96):
                self.rect.bottom = int(HEIGHT * 0.96)
                self.jumping = False
                self.jump_velocity = 0

def checkcollsion(a, b): #a is the dino/stationary object, b is the cactus
    if a.rect.left >= b.rect.left and a.rect.bottom >= b.rect.top:
        return True
    else:
        return False

def game_over():
    font = pygame.font.Font("T-rex game/font.ttf", 40)
    text = font.render("GAME OVER", True, (255,0,0))
    screen.blit(text, (WIDTH/3, HEIGHT/3))
    restart_font = pygame.font.Font("T-rex game/font.ttf", 20)
    restart_text = restart_font.render("press "+ "'a'" + " to restart game", True, (255,0,0))
    screen.blit (restart_text,(WIDTH/3, HEIGHT/3 + 50))

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
    if not collision:
        ground.update()
    #randomly spawning cacti
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
    if not collision:
        cacti.update()

    dino.draw()
    dino.update()
    #checking for collision
    for c in cacti:
        if checkcollsion(dino, c):
            dino.score = 0
            collision = True
    #ending game
    if collision:
        dino.score = 0
        game_over()
    #updating game speed
    if not collision:
        game_speed += 0.01
    #resetting game
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        collision = False
        game_speed = BASE_SPEED
        cacti.empty()

    pygame.display.flip() #updates display

#quites pygame and closes the window
pygame.quit()
sys.exit()