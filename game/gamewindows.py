#adding name input screen
import pygame
import socket
import threading
import time
import json
import random
import wconnection2

from pygame import mixer

#NIK'S Section =======================================
#import Nik's FPGA library
fpga = wconnection2.FPGA() #instance of FPGA class
fpga.start_communication()

#====================================================

pygame.init()
mixer.init()

# load the icon image
icon_image = pygame.image.load("assets/icon.png")

# set the window icon to the icon image
pygame.display.set_icon(icon_image)

# set heading of pygame window
pygame.display.set_caption("NETFLICKS")


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
CUSTOM_FONT_SIZE = 45
SMALL_FONT_SIZE = 40
TINY_FONT_SIZE = 20
font_path = "assets/Monaco.ttf"

# store good/perfect/miss
#messages = []

Leave = False

### TCP settings
# Set up the TCP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#the server name and port client wishes to access
server_name = '54.210.203.6'
server_port = 12000
client_socket.connect((server_name, server_port))



# Change the size of the image
rightArrow = pygame.image.load("assets/rightArrow.png")
leftArrow = pygame.image.load("assets/leftArrow.png")
upArrow = pygame.image.load("assets/upArrow.png")
downArrow = pygame.image.load("assets/downArrow.png")

scaled_image_right = pygame.transform.scale(rightArrow, (50, 50))
scaled_image_up =pygame.transform.scale(upArrow, (50, 50))
scaled_image_left =pygame.transform.scale(leftArrow, (50, 50))
scaled_image_down =pygame.transform.scale(downArrow, (50, 50))

images = [
    (scaled_image_left, pygame.Rect(0, 0, 50, 50)),
    (scaled_image_up, pygame.Rect(0, 0, 50, 50)),
    (scaled_image_down, pygame.Rect(0, 0, 50, 50)),
    (scaled_image_right, pygame.Rect(0, 0, 50, 50))
]

# Initialize fonts
big_font = pygame.font.Font(font_path, BIG_FONT_SIZE)
medium_font = pygame.font.Font(font_path, MEDIUM_FONT_SIZE)
small_font = pygame.font.Font(font_path, SMALL_FONT_SIZE)
custom_font = pygame.font.Font(font_path, CUSTOM_FONT_SIZE)
tiny_font = pygame.font.Font(font_path, TINY_FONT_SIZE)


clock = pygame.time.Clock()

# Define keys and their colors
redNet = pygame.image.load("assets/basketball-hoop-red.png")
greenNet = pygame.image.load("assets/basketball-hoop-green.png")
blueNet = pygame.image.load("assets/basketball-hoop-blue.png")
yellowNet = pygame.image.load("assets/basketball-hoop-yellow.png")

button_width = 80
button_height = 80

# Create new surfaces with the same size as the scaled images
redNet_surface = pygame.Surface((button_width, button_height))
redNet_surface.set_colorkey((0, 0, 0))
greenNet_surface = pygame.Surface((button_width, button_height))
greenNet_surface.set_colorkey((0, 0, 0))
blueNet_surface = pygame.Surface((button_width, button_height))
blueNet_surface.set_colorkey((0, 0, 0))
yellowNet_surface = pygame.Surface((button_width, button_height))
yellowNet_surface.set_colorkey((0, 0, 0))

# Draw the scaled images onto the new surfaces
redNet_surface.blit(pygame.transform.scale(redNet, (button_width, button_height)), (0, 0))
greenNet_surface.blit(pygame.transform.scale(greenNet, (button_width, button_height)), (0, 0))
blueNet_surface.blit(pygame.transform.scale(blueNet, (button_width, button_height)), (0, 0))
yellowNet_surface.blit(pygame.transform.scale(yellowNet, (button_width, button_height)), (0, 0))

keys = [
    {'surface': redNet_surface, 'rect': redNet_surface.get_rect(centerx=SCREEN_WIDTH/5, centery=SCREEN_HEIGHT-100), 'color1': RED, 'color2': (180, 0, 0), 'key': pygame.K_1, 'pressed': False, 'label': 'L\r\n'},
    {'surface': greenNet_surface, 'rect': greenNet_surface.get_rect(centerx=2*SCREEN_WIDTH/5, centery=SCREEN_HEIGHT-100), 'color1': GREEN, 'color2': (0, 180, 0), 'key': pygame.K_2, 'pressed': False, 'label': 'U\r\n'},
    {'surface': blueNet_surface, 'rect': blueNet_surface.get_rect(centerx=3*SCREEN_WIDTH/5, centery=SCREEN_HEIGHT-100), 'color1': BLUE, 'color2': (0, 0, 180), 'key': pygame.K_3, 'pressed': False, 'label': 'D\r\n'},
    {'surface': yellowNet_surface, 'rect': yellowNet_surface.get_rect(centerx=4*SCREEN_WIDTH/5, centery=SCREEN_HEIGHT-100), 'color1': YELLOW, 'color2': (180, 180, 0), 'key': pygame.K_4, 'pressed': False, 'label': 'R\r\n'}
]

# Define levels
# Music from https://freemusicarchive.org/.  Specific tracks used: Drivin' Round Town by Jack Adkins, Sneakers by Crowander and Freedom by Cyrus 
levels = [    {'name': 'Freedom Drive', 'file': 'assets/level.txt', 'music': 'assets/freedom.mp3', 'backdrop': pygame.image.load("assets/sunsetDriveBackdrop.png"), 'speed':2},  
              {'name': 'Tundra Walkway ', 'file': 'assets/level.txt', 'music': 'assets/tundra.mp3', 'backdrop': pygame.image.load("assets/tundraWalkwayBackdrop.jpg"), 'speed':3},  
              {'name': 'Moonlight Sonata', 'file': 'assets/level.txt', 'music': 'assets/moonlight.mp3', 'backdrop': pygame.image.load("assets/moonlightSontanaBackdrop.png"), 'speed':4},]



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
    levelSelectImage = pygame.image.load('assets/selectLevel.png')
    image = pygame.transform.scale(levelSelectImage, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(image, (0, 0))
    draw_text('Select a level', medium_font, WHITE, SCREEN_WIDTH // 3.2, SCREEN_HEIGHT // 3.5)

    # Draw level options
    for i, level in enumerate(levels):
        x = SCREEN_WIDTH // 3
        y = SCREEN_HEIGHT // 2.4 + i * 80
        draw_text(f'{i+1}. {level["name"]}', small_font, WHITE, x, y)

def generate_text():
    with open("assets/level.txt", "w") as file:
        levelGen = ["0", "1", "2", "3", "4"]
        levelstring = ""
        file.truncate(0)
        for i in range(50):
            temp = levelGen[random.randint(0,4)]
            file.write(temp+"\n")
            levelstring = levelstring + temp
    return levelstring
   
def load_level(level):
    rects = []
    mixer.music.load(level['music'])
    mixer.music.play()

    f = open("assets/level.txt")
    data = f.readlines()

    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '0':
                rects.append(DroppingRect(images[0][0], keys[0]['rect'].centerx - 25, y * -100))
            elif data[y][x] == '1':
                rects.append(DroppingRect(images[1][0], keys[1]['rect'].centerx - 25, y * -100))
            elif data[y][x] == '2':
                rects.append(DroppingRect(images[2][0], keys[2]['rect'].centerx - 25, y * -100))
            elif data[y][x] == '3':
                rects.append(DroppingRect(images[3][0], keys[3]['rect'].centerx - 25, y * -100))
    return rects

def write_level(levelString):
    with open("assets/level.txt", "w") as f:
    
        for char in levelString:
            # write the character to a new line in the file
            f.write(char + "\n")

# Start game loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def format_number(num):
    # Convert the number to a string
    num_str = str(num)
    
    # If the string is less than 4 characters, add leading zeros
    while len(num_str) < 4:
        num_str = '0' + num_str
    
    # Return the formatted string
    return num_str


def receive():
    # Wait for start signal from server
    global in_game, leaderboard_data
    while not Leave:

            global full_ready, is_player1, is_player2, is_player1_ready, is_player2_ready
            global connected, ready_num, player_num, level_selected, start1, start2, current_level
            global P1Score, P2Score, GameOver1, GameOver2, score
            #print(7)
            data = client_socket.recv(1024).decode()
            print(data)
            if data == "fullready":
                full_ready = True

            if data == "start":
                in_game = True
                #connected = True

            elif data.startswith("player"):
                player_num = int(data.split()[1])
                print(f"hahahha{player_num}")
                if player_num == 1:
                    is_player1 = True
                    #is_player2 = False
                    #client_socket.send("Ready 1")
                    connected = True
                else:
                    #is_player1 = False
                    is_player2 = True
                    #client_socket.send("Ready 2")
                    connected = True

            elif data.startswith("ready"):
                ready_num = int(data.split()[1])
                if ready_num == 1:
                    is_player1_ready = True
                    print("received player1 ready")
                    #client_socket.send("Ready 1")
                    #connected = True
                else:
                    is_player2_ready = True
                    print("received player2 ready")
                    #client_socket.send("Ready 2")
                    #connected = True
            elif data.startswith("levelreceive"):
                start_num = int(data.split()[1])
                print("receive levelreceive")
                if start_num == 1:
                    start1 = True   # -------------------need to start from here, start1 and 2 should determined by sending signals
                elif start_num == 2:
                    start2 = True
            
            elif data.startswith("level"):
                    print("recievedlevel")
                    current_level = int(data.split()[1])
                    client_socket.send("LevelS2".encode())
                    level_selected = True

            elif data.isdigit() or (data[0] == '-' and data[1:].isdigit()):

                if is_player1:
                    P2Score = int(data)
                    print(P2Score)
                    print(" ")
                elif is_player2:
                    P1Score = int(data)
                    print(P1Score)
                    print(" ")
            
            elif data.startswith("LevelString"):
                LevelString2= data.split("/")[1]
                write_level(LevelString2)
            
            elif data == "Minus":
                score  = score - 10

            elif data == "2GameOver":
                GameOver2 = True
            
            elif data == "1GameOver":
                GameOver1 = True

            elif data.startswith("["):
                leaderboard_data = json.loads(data)
                print(leaderboard_data)

            elif data == "quit":
                print("receive quit")
                break


connected = False
is_player1 = False
is_player2 = False
is_player1_ready = False
is_player2_ready = False
i = 0

while True:
    # define constant
    game_over = False
    in_game = False
    full_ready = False

    name_entered = False
    
    
    start1 = False
    start2 = False
    
    level_selected = False
    current_level = 0
    LevelS1 = False
    LevelS2 = False
    #start_game = False
    both_game_over = False
    GameOver1 = False
    GameOver2 = False

    score = 0
    P1Score = 0
    P2Score = 0
    oldscore = 0
    other_player_score = 0
    fpgascore = "0000"
    fpga.update_score("0000")

    name = ""
    # Start the receive data thread
    receive_thread = threading.Thread(target=receive)
    #receive_thread.setDaemon(True)
    receive_thread.start()

    mixer.music.load('assets/homeSong.mp3')
    mixer.music.play()
    
    while not name_entered: #Screen 1
        
        screen.fill(BLACK)
        background_image = pygame.image.load('assets/homepage.png')
        image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(image, (0, 0))
        draw_text(name, medium_font, YELLOW, SCREEN_WIDTH // 1.65, SCREEN_HEIGHT // 1.46)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fpga.kill()
                Leave = True
                time.sleep(1) 
                client_socket.send('quit'.encode())
                time.sleep(1)
                client_socket.close()
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    name_entered = True
                    time.sleep(0.1)
                else:
                    name += event.unicode
        print(name)
        pygame.display.update()
        clock.tick(60)
        
    while not connected: #Screen 2
        screen.fill(BLACK)
        wait_screen_image = pygame.image.load('assets/waitingscreen.png')
        image = pygame.transform.scale(wait_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(image, (0, 0))
        client_socket.send("request".encode())
        time.sleep(0.3)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fpga.kill()
                Leave = True
                time.sleep(1)  # use to let the thread close first before disconnecting the socket
                client_socket.send('quit'.encode())
                time.sleep(1)
                client_socket.close()
                pygame.quit()
                quit()

   

    send_level = ""

    while not full_ready and connected: #Screen 3
        time.sleep(0.3)

        if i == 0 and is_player1:
            send_level = generate_text() 
            client_socket.send(("LevelString/" + send_level).encode())
            time.sleep(0.2)
            i += 1


        screen.fill(BLACK)
        background_image = pygame.image.load('assets/standardpage.png')
        image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fpga.kill()
                Leave = True
                time.sleep(1)  # use to let the thread close first before disconnecting the socket
                client_socket.send('quit'.encode())
                time.sleep(1)
                client_socket.close()
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and is_player1 == True and is_player2 == False:
                    is_player1_ready = True
                    client_socket.send("Ready 1".encode())
                    time.sleep(0.1)

                if event.key == pygame.K_r and is_player1 == False and is_player2 == True:
                    is_player2_ready = True
                    client_socket.send("Ready 2".encode())
                    time.sleep(0.1)
            
            
        # Draw player readiness status
        #draw_text(f'You are player  {"1" if is_player1 else "error"}', medium_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 160)
        draw_text(f'YOU ARE PLAYER {"2" if is_player2 else "1"}', tiny_font, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.9 - 80)
        draw_text(f'PLAYER 1: {"Ready!" if is_player1_ready else "Not Ready Yet"}', small_font, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.9)
        draw_text(f'PLAYER 2: {"Ready!" if is_player2_ready else "Not Ready Yet"}', small_font, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.9 + 80)

        if is_player1_ready and is_player2_ready:
            client_socket.send("FullReady".encode())

        pygame.display.update()
        clock.tick(60)
                
    

    while not level_selected and full_ready: #Screen 4
        screen.fill(BLACK)
        print(is_player2)
        
        if is_player2:
            wait_screen_image = pygame.image.load('assets/waitingscreenLevel.png')
            image = pygame.transform.scale(wait_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(image, (0, 0))
            # Check for messages from server
            pygame.display.update()

        # Handle level selection for player 1
        if is_player1:
            # Draw level selection menu
            # screen.fill(BLACK)
            
            draw_menu()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fpga.kill()
                    Leave = True
                    time.sleep(1)  # use to let the thread close first before disconnecting the socket
                    client_socket.send('quit'.encode())
                    time.sleep(1)
                    client_socket.close()
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        level = levels[0]
                        current_level = 0
                        client_socket.send(("level " + str(current_level)).encode())
                        time.sleep(0.5)
                        client_socket.send("LevelS1".encode())
                        level_selected = True
                    elif event.key == pygame.K_2:
                        level = levels[1]
                        current_level = 1
                        client_socket.send(("level " + str(current_level)).encode())
                        time.sleep(0.5)
                        client_socket.send("LevelS1".encode())
                        level_selected = True
                    elif event.key == pygame.K_3:
                        level = levels[2]
                        current_level = 2
                        client_socket.send(("level " + str(current_level)).encode())
                        time.sleep(0.5)
                        client_socket.send("LevelS1".encode())
                        level_selected = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        client_socket.send(("level " + str(current_level)).encode())
                        time.sleep(0.5)
                        client_socket.send("LevelS1".encode())
                        level_selected = True
                    
        
        pygame.display.update()
        clock.tick(60)

    mixer.stop()

    while not in_game: #Screen 4.5
        screen.fill(BLACK)
        draw_text('Wait for start', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        if start1 and start2:
            client_socket.send("FullStart".encode())
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fpga.kill()
                Leave = True
                time.sleep(1)  # use to let the thread close first before disconnecting the socket
                client_socket.send('quit'.encode())
                time.sleep(1)
                client_socket.close()
                pygame.quit()
                quit()
                
    
    # Load level and start game
    map_rect = load_level(levels[current_level])
    combo = 1
    perfect = 0
    
    messages = []

    clock = pygame.time.Clock()
    game_over = False
    #in_game = True
    

    while in_game: #Screen 5
        
        
        screen.blit(levels[current_level]["backdrop"], (0, 0))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fpga.kill()
                Leave = True
                time.sleep(1)  # use to let the thread close first before disconnecting the socket
                client_socket.send('quit'.encode())
                time.sleep(1)
                client_socket.close()
                pygame.quit()
                quit()

        # Handle key events
        k = pygame.key.get_pressed()

        reading = fpga.read()

        print (reading)

        for key in keys:
            if k[key['key']] or reading == key['label']:
                #print ("detected !!!!!!")
                pygame.draw.rect(screen, key['color1'], key['rect'])
                key['pressed'] = True
            else:
                screen.blit(key['surface'], key['rect'])
                key['pressed'] = False

        # Draw the rectangles for the falling notes
        for rect in map_rect:
            screen.blit(rect.image, rect.rect)
            rect.rect.y += levels[current_level]['speed']  # ----------------------------falling speed --------------------

            # Check if a note hits a key
            for key in keys:
                if key['rect'].colliderect(rect.rect) and key['pressed']:
                    if abs(rect.rect.centery - key['rect'].centery) < 15:
                        # perfect hit
                        map_rect.remove(rect)
                        combo += 1
                        score += 2 * combo
                        perfect += 1
                        #print("perfect")
                        messages.append(('perfect', small_font, GREEN, key['rect'].centerx, key['rect'].top - 20))
                    else:
                        # good hit
                        map_rect.remove(rect)
                        combo += 1
                        score += 1 * combo
                        perfect = 0
                        #print("good")
                        messages.append(('good', small_font, YELLOW, key['rect'].centerx, key['rect'].top - 20))
                    key['pressed'] = False
                    break

            if keys[0]['rect'].bottom < rect.rect.y:
                # if the note goes past the key, remove it and reset the combo
                map_rect.remove(rect)
                combo = 1
                perfect = 0
                messages.append(('miss', small_font, RED, rect.rect.centerx, key['rect'].top - 20))

        # display good/perfect/miss
        if (len(messages) > 0):
            for message in messages:
                if (len(messages) > 1):
                    messages.pop(0)
                text, font, color, x, y = message
                draw_text(text, font, color, x, y)
        
        if perfect >= 3 and oldscore != score:
            if is_player1:                
                client_socket.send(("2Minus").encode())
                #time.sleep(0.2)
            elif is_player2:
                client_socket.send(("1Minus").encode())
                #time.sleep(0.2)
            

        # send score to TCP sever ???
        if oldscore != score:            
            oldscore = score
            myscore = score
            fpgascore = format_number(myscore)
            print(fpgascore)
            fpga.update_score(fpgascore)
            #send the message to the TCP server
            
            if is_player1:                
                client_socket.send(("1Score " + str(myscore)).encode())
            elif is_player2:
                client_socket.send(("2Score " + str(myscore)).encode())

        if is_player1:
            othertext = tiny_font.render(f"Other Player Score: {P2Score}", True,"white")
            screen.blit(othertext,(SCREEN_WIDTH-400,0))
        
        if is_player2:
            othertext = tiny_font.render(f"Other Player Score: {P1Score}", True,"white")
            screen.blit(othertext,(SCREEN_WIDTH-400,0))
        

        # Draw combo and score text
        combotext = medium_font.render(str(combo)+"X", True,"white")
        screen.blit(combotext,(0,SCREEN_HEIGHT)) 
        scoretext = medium_font.render("SCORE: " + str(score), True,"white")
        screen.blit(scoretext,(0,0)) 

        
        # Check if the game is over
        if len(map_rect) == 0:
            game_over = True
            in_game = False

            if is_player1:
                GameOver1 = True
                client_socket.send("1GameOver".encode())
                time.sleep(0.2)
                print("serverName")
                client_socket.send(("serverName"+"/"+str(current_level)+"/"+str(score)+"/"+name).encode())

            if is_player2:
                GameOver2 = True
                client_socket.send("2GameOver".encode())
                time.sleep(0.2)
                print("serverName")
                client_socket.send(("serverName"+"/"+str(current_level)+"/"+str(score)+"/"+name).encode())
             
            
              
            
        # Update display and tick clock
        pygame.display.update()
        clock.tick(60)

    is_player1_ready = False
    is_player2_ready = False
    leaderboard = False
    leaderboard_data = []

    while game_over: #Screen 6
        screen.fill(BLACK)
        gameOverImage = pygame.image.load('assets/gameOver.png')
        image = pygame.transform.scale(gameOverImage, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(image, (0, 0))

        #draw_text('test', tiny_font, WHITE, SCREEN_WIDTH // 9, SCREEN_HEIGHT // 3)
        
        if GameOver1 and GameOver2:
            print("both game over")
            both_game_over = True

        if both_game_over:
            if is_player1:
                print("gameover 1 finish")
                if (score > P2Score):
                    draw_text('YOU WIN!', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                elif (score < P2Score):
                    draw_text('YOU LOSE!', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                else:
                    draw_text('TIE!', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                
                draw_text(f'Final Score: {score}', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 80)
                draw_text(f'Other Player score: {P2Score}', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 160)
                draw_text('Press 0 to go back to the Main Menu', tiny_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 240)
                draw_text('Press 1 to go to the Hall of Fame', tiny_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 280)
                pygame.display.update()
                clock.tick(60)
            
            if is_player2:
                print("gameover 1 finish")
                if (score > P1Score):
                    draw_text('YOU WIN!', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                elif (score < P1Score):
                    draw_text('YOU LOSE!', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                else:
                    draw_text('TIE!', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

                draw_text(f'Final Score: {score}', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 80)
                draw_text(f'Other Player Score: {P1Score}', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 160)
                draw_text('Press 0 to go back to the Main Menu', tiny_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 240)
                draw_text('Press 1 to go to the Hall of Fame', tiny_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 280)
                pygame.display.update()
                clock.tick(60)

            
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                fpga.kill()
                Leave = True
                time.sleep(1)  # use to let the thread close first before disconnecting the socket
                client_socket.send('quit'.encode())
                time.sleep(1)
                client_socket.close()
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    print("0 is pressed")
                    mixer.music.stop()
                    game_over = False
                    break
                if event.key == pygame.K_1:
                    print("1 is pressed")
                    #mixer.music.stop()
                    leaderboard = True
                    break

        while leaderboard: #Screen 7
            screen.fill(BLACK)
            client_socket.send(("Leaderboard" +"/"+ str(current_level)).encode())
            time.sleep(0.2)
            # Define the position to start rendering the text

            hallOfFameImage = pygame.image.load('assets/hallOfFame.png')
            image = pygame.transform.scale(hallOfFameImage, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(image, (0, 0))
            

            x = SCREEN_WIDTH // 2
            y = SCREEN_HEIGHT // 5

            # Render the leaderboard data as text on the screen
            for i, entry in enumerate(leaderboard_data):
                # Render the player name
                name_text = font.render(f"{i+1}. {entry['name']}", True, (255, 255, 255))
                screen.blit(name_text, (x - SCREEN_WIDTH/4, y + i*45))
                
                # Render the player score
                score_text = font.render(str(entry['score']), True, (255, 255, 255))
                screen.blit(score_text, (x + SCREEN_WIDTH/4, y + i*45))

            # Update the display
            pygame.display.update()

            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    fpga.kill()
                    Leave = True
                    time.sleep(1)  # use to let the thread close first before disconnecting the socket
                    client_socket.send('quit'.encode())
                    time.sleep(1)
                    client_socket.close()
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        print("0 is pressed")
                        #mixer.music.stop()
                        leaderboard = False
                        break

                    
        if not game_over:
            break
