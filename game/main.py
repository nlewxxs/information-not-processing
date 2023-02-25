#welcome to my pygame tutorial

import pygame

#lets get sound 
from pygame import mixer

pygame.init()
mixer.init()

font = pygame.font.Font(pygame.font.get_default_font(), 80) #help i can render font / last number change the font size
font1 = pygame.font.Font(pygame.font.get_default_font(), 40)
combo = 1
score = 0


clock = pygame.time.Clock()

#now we will create a map by making a txt file

screen = pygame.display.set_mode((900, 600))

# Load the image
image = pygame.image.load("image.jpg")

#change the size of the image
scaled_image_right = pygame.transform.scale(image, (50, 50))
scaled_image_up =pygame.transform.rotate(scaled_image_right,90)
scaled_image_left =pygame.transform.rotate(scaled_image_up,90)
scaled_image_down =pygame.transform.rotate(scaled_image_left,90)

images = [
    (scaled_image_left, pygame.Rect(0, 0, 50, 50)),
    (scaled_image_up, pygame.Rect(0, 0, 50, 50)),
    (scaled_image_down, pygame.Rect(0, 0, 50, 50)),
    (scaled_image_right, pygame.Rect(0, 0, 50, 50))
]

#first we will create the classes for the keys

class Key():
    def __init__(self,x,y,color1,color2,key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key = key
        self.rect = pygame.Rect(self.x,self.y,80,80)
        self.pressed = False

#now we will make a list of keys

keys = [
    Key(100,500,(255,0,0),(180,0,0),pygame.K_1),
    Key(300,500,(0,255,0),(0,180,0),pygame.K_2),
    Key(500,500,(0,0,255),(0,0,180),pygame.K_3),
    Key(700,500,(255,255,0),(180,180,0),pygame.K_4),
]

class DroppingRect():
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return 0
            elif event.key == pygame.K_2:
                return 1
            elif event.key == pygame.K_3:
                return 2
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            return None

#lets load the map into the game 
def load(map):
    rects = []
    mixer.music.load(map + ".mp3")
    mixer.music.play()
    f = open(map + ".txt", 'r')
    data = f.readlines()

    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '0':
                rects.append(DroppingRect(images[0][0], keys[x].rect.centerx - 25, y * -100))
            elif data[y][x] == '1':
                rects.append(DroppingRect(images[1][0], keys[x].rect.centerx - 25, y * -100))
            elif data[y][x] == '2':
                rects.append(DroppingRect(images[2][0], keys[x].rect.centerx - 25, y * -100))
            elif data[y][x] == '3':
                rects.append(DroppingRect(images[3][0], keys[x].rect.centerx - 25, y * -100))
    return rects

map_rect = load("freedom dive")

game_over = False
while not game_over:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    #now we will loop through the keys and handle the events
    k = pygame.key.get_pressed()

    for key in keys:
        if k[key.key]:
            #screen.blit(scaled_image, key.rect)
            pygame.draw.rect(screen,key.color1,key.rect)
            key.pressed = True
        if not k[key.key]: 
            pygame.draw.rect(screen,key.color2,key.rect)
            key.pressed = False
        #now when we press our keys they will change color
    for rect in map_rect:
        #pygame.draw.rect(screen,(200,0,0),rect)
        screen.blit(rect.image, rect.rect)
        rect.rect.y += 5
        for key in keys: 
            if key.rect.colliderect(rect) and key.pressed:
                # condition of checking good/perfect
                if abs(rect.rect.centery - key.rect.centery) < 15:
                    # perfect hit
                    map_rect.remove(rect)
                    combo += 1
                    score += 2 * combo
                    print("perfect")
                else:
                    # good hit
                    map_rect.remove(rect)
                    combo += 1
                    score += 1 * combo
                    print("good")
                key.pressed = False
                break

        if keys[0].rect.bottom < rect.rect.y: #if the key is 100 pixels lower than the key it will be removed
            map_rect.remove(rect)
            combo = 1

        #lets display our text here
    combotext = font.render(str(combo)+"X", True,"white")
    screen.blit(combotext,(0,500)) 
    scoretext = font.render("SCORE: " + str(score), True,"white")
    screen.blit(scoretext,(0,0)) 

    if len(map_rect) == 0:
        screen.fill((0, 0, 0))
        finishtext = font.render("Game Over !!!", True, "white")
        scoretext1 = font1.render("Final Score: " + str(score), True, "white")
        screen.blit(finishtext, (200, 200))
        
        # print the score in the center of the screen
        score_rect = scoretext1.get_rect()
        score_rect.centerx = screen.get_rect().centerx
        score_rect.y = 300
        screen.blit(scoretext1, score_rect)
        pygame.display.update()

        # loop until the game is closed
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    pygame.display.update()
    clock.tick(60)
