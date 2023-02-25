import pygame
import socket
import threading
import time


from pygame import mixer

pygame.init()
mixer.init()

# Define constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define font sizes
BIG_FONT_SIZE = 80
MEDIUM_FONT_SIZE = 60
SMALL_FONT_SIZE = 40
TINY_FONT_SIZE = 20

# store good/perfect/miss
#messages = []

Leave = False



### TCP settings
# Set up the TCP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#the server name and port client wishes to access
server_name = '54.210.203.6'
#'54.210.203.6'
server_port = 12000
client_socket.connect((server_name, server_port))



# Load the image
image = pygame.image.load("image.jpg")

# Change the size of the image
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

# Initialize fonts
big_font = pygame.font.Font(pygame.font.get_default_font(), BIG_FONT_SIZE)
medium_font = pygame.font.Font(pygame.font.get_default_font(), MEDIUM_FONT_SIZE)
small_font = pygame.font.Font(pygame.font.get_default_font(), SMALL_FONT_SIZE)
tiny_font = pygame.font.Font(pygame.font.get_default_font(), TINY_FONT_SIZE)



# Define keys and their colors
keys = [{'rect': pygame.Rect(200, 500, 80, 80), 'color1': RED, 'color2': (180, 0, 0), 'key': pygame.K_1},    
        {'rect': pygame.Rect(400, 500, 80, 80), 'color1': GREEN, 'color2': (0, 180, 0), 'key': pygame.K_2},    
        {'rect': pygame.Rect(600, 500, 80, 80), 'color1': BLUE, 'color2': (0, 0, 180), 'key': pygame.K_3},    
        {'rect': pygame.Rect(800, 500, 80, 80), 'color1': (255, 255, 0), 'color2': (180, 180, 0), 'key': pygame.K_4},]

# Define levels
# 2/3 level are not implemented yet
levels = [    {'name': 'Freedom Dive', 'file': 'freedom dive.txt', 'music': 'freedom dive.mp3'},  
              {'name': 'Canon in D', 'file': 'canon_in_d.txt', 'music': 'canon_in_d.mp3'},  
              {'name': 'Moonlight Sonata', 'file': 'moonlight_sonata.txt', 'music': 'moonlight_sonata.mp3'},]

# Dropping arrows:
class DroppingRect():
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define functions
def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    rect.center = (x, y)
    screen.blit(surface, rect)

def draw_menu():
    screen.fill(BLACK)
    draw_text('Select a level', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

    # Draw level options
    for i, level in enumerate(levels):
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2 + i * 60
        draw_text(f'{i+1}. {level["name"]}', small_font, WHITE, x, y)

def load_level(level):
    rects = []
    mixer.music.load(level['music'])
    mixer.music.play()

    f = open(level['file'])
    data = f.readlines()

    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '0':
                rects.append(DroppingRect(images[0][0], keys[x]['rect'].centerx - 25, y * -100))
            elif data[y][x] == '1':
                rects.append(DroppingRect(images[1][0], keys[x]['rect'].centerx - 25, y * -100))
            elif data[y][x] == '2':
                rects.append(DroppingRect(images[2][0], keys[x]['rect'].centerx - 25, y * -100))
            elif data[y][x] == '3':
                rects.append(DroppingRect(images[3][0], keys[x]['rect'].centerx - 25, y * -100))
    return rects



# Define a function to receive data from the server
def receive_data():
    global other_player_score
    while not Leave:
        client_socket.send("get_score".encode())
        data = client_socket.recv(1024).decode()
        
        if data.isdigit():
            other_player_score = int(data)
    #client_socket.send("quit".encode())
        
# Start the receive data thread
receive_thread = threading.Thread(target=receive_data)
#receive_thread.setDaemon(True)
receive_thread.start()



# Start game loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game_over = False
in_game = False

while True:
    # Draw level selection menu
    draw_menu()
    pygame.display.update()

    # Wait for level selection
    level = None
    while not level:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = levels[0]
                elif event.key == pygame.K_2:
                    level = levels[1]
                elif event.key == pygame.K_3:
                    level = levels[2]

    # Load level and start game
    map_rect = load_level(level)
    combo = 1
    score = 0
    oldscore = 0
    other_player_score = 0
    messages = []

    clock = pygame.time.Clock()
    game_over = False
    in_game = True

    while in_game:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Leave = True
                time.sleep(1)
                client_socket.send('quit'.encode())
                client_socket.close()
                
                pygame.quit()
                quit()

        # Handle key events
        k = pygame.key.get_pressed()
        for key in keys:
            if k[key['key']]:
                pygame.draw.rect(screen, key['color1'], key['rect'])
                key['pressed'] = True
            if not k[key['key']]:
                pygame.draw.rect(screen, key['color2'], key['rect'])
                key['pressed'] = False

        # Draw the rectangles for the falling notes
        for rect in map_rect:
            screen.blit(rect.image, rect.rect)
            rect.rect.y += 5  # ----------------------------falling speed --------------------

            # Check if a note hits a key
            for key in keys:
                if key['rect'].colliderect(rect.rect) and key['pressed']:
                    if abs(rect.rect.centery - key['rect'].centery) < 15:
                        # perfect hit
                        map_rect.remove(rect)
                        combo += 1
                        score += 2 * combo
                        #print("perfect")
                        messages.append(('perfect', small_font, GREEN, key['rect'].centerx, key['rect'].top - 20))
                    else:
                        # good hit
                        map_rect.remove(rect)
                        combo += 1
                        score += 1 * combo
                        #print("good")
                        messages.append(('good', small_font, YELLOW, key['rect'].centerx, key['rect'].top - 20))
                    key['pressed'] = False
                    break

            if keys[0]['rect'].bottom < rect.rect.y:
                # if the note goes past the key, remove it and reset the combo
                map_rect.remove(rect)
                combo = 1
                messages.append(('miss', small_font, RED, rect.rect.centerx, key['rect'].top - 20))

        # display good/perfect/miss
        if (len(messages) > 0):
            for message in messages:
                if (len(messages) > 1):
                    messages.pop(0)
                text, font, color, x, y = message
                draw_text(text, font, color, x, y)

        # send score to TCP sever ???
        if oldscore != score:            
            oldscore = score
            myscore = score
            #send the message to the TCP server
            
            client_socket.send(str(myscore).encode())

        
        othertext = tiny_font.render(f"Others Score: {other_player_score}", True,"white")
        screen.blit(othertext,(600,0))
        

        # Draw combo and score text
        combotext = medium_font.render(str(combo)+"X", True,"white")
        screen.blit(combotext,(0,500)) 
        scoretext = medium_font.render("SCORE: " + str(score), True,"white")
        screen.blit(scoretext,(0,0)) 

        
        # Check if the game is over
        if len(map_rect) == 0:
            game_over = True
            in_game = False
             
            
        # When game is over
        if game_over:
            screen.fill(BLACK)
            if (score > other_player_score):
                draw_text('Game Over ! YOU WIN !', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            elif (score < other_player_score):
                draw_text('Game Over ! YOU LOSE !', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            else:
                draw_text('Game Over !!!', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            draw_text(f'Final Score: {score}', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 80)
            draw_text(f'Other player score: {other_player_score}', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 160)
            draw_text('Press 0 to go back to the main menu', tiny_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 240)
            pygame.display.update()

        # Update display and tick clock
        pygame.display.update()
        clock.tick(60)

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Leave = True
                time.sleep(1)  # use to let the thread close first before disconnecting the socket
                client_socket.send('quit'.encode())
                client_socket.close()               
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    print("0 is pressed")
                    mixer.music.stop()
                    game_over = False
                    break
        if not game_over:
            break

        