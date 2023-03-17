#adding name input screen
import pygame
import socket
import threading
import time
import json
import random

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
big_font = pygame.font.Font(pygame.font.get_default_font(), BIG_FONT_SIZE)
medium_font = pygame.font.Font(pygame.font.get_default_font(), MEDIUM_FONT_SIZE)
small_font = pygame.font.Font(pygame.font.get_default_font(), SMALL_FONT_SIZE)
tiny_font = pygame.font.Font(pygame.font.get_default_font(), TINY_FONT_SIZE)
font = pygame.font.SysFont("Arial", 20)

clock = pygame.time.Clock()

# Define keys and their colors
keys = [{'rect': pygame.Rect(200, 500, 80, 80), 'color1': RED, 'color2': (180, 0, 0), 'key': pygame.K_1},    
        {'rect': pygame.Rect(400, 500, 80, 80), 'color1': GREEN, 'color2': (0, 180, 0), 'key': pygame.K_2},    
        {'rect': pygame.Rect(600, 500, 80, 80), 'color1': BLUE, 'color2': (0, 0, 180), 'key': pygame.K_3},    
        {'rect': pygame.Rect(800, 500, 80, 80), 'color1': YELLOW, 'color2': (180, 180, 0), 'key': pygame.K_4},]

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
    wallpaper = pygame.image.load("assets/levelSelect.png")
    wallpaper.set_alpha(128)
    screen.blit(wallpaper, (0,0))
    draw_text('Select a level', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

    # Draw level options
    for i, level in enumerate(levels):
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2 + i * 60
        draw_text(f'{i+1}. {level["name"]}', small_font, WHITE, x, y)

def generate_text():
    with open("assets/level.txt", "w") as file:
        levelGen = ["0", "1", "2", "3"]
        levelstring = ""
        file.truncate(0)
        for i in range(50):
            temp = levelGen[random.randint(0,3)]
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

    name = ""
    # Start the receive data thread
    receive_thread = threading.Thread(target=receive)
    #receive_thread.setDaemon(True)
    receive_thread.start()
    
    while not name_entered:
        
        screen.fill(BLACK)
        draw_text('Enter your name:', medium_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text(name, medium_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Leave = True
                time.sleep(1)  # use to let the thread close first before disconnecting the socket
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
        clock.tick(60)

        '''
        name = input("Enter your name:  ")
        print(name)
        name_entered = True
        '''
        
    while not connected:
        print('1')
        screen.fill(BLACK)
        draw_text('Waiting for other player...', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        client_socket.send("request".encode())
        time.sleep(0.3)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Leave = True
                time.sleep(1)  # use to let the thread close first before disconnecting the socket
                client_socket.send('quit'.encode())
                time.sleep(1)
                client_socket.close()
                pygame.quit()
                quit()
   

    send_level = ""

    while not full_ready and connected:
        #print("2")
        #print(is_player1)
        time.sleep(0.3)

        if i == 0 and is_player1:
            send_level = generate_text() 
            client_socket.send(("LevelString/" + send_level).encode())
            time.sleep(0.2)
            i += 1


        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        draw_text(f'You are player  {"2" if is_player2 else "1"}', medium_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)
        draw_text(f'Player 1: {"Ready" if is_player1_ready else "Not Ready"}', medium_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(f'Player 2: {"Ready" if is_player2_ready else "Not Ready"}', medium_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)

        if is_player1_ready and is_player2_ready:
            client_socket.send("FullReady".encode())

        pygame.display.update()
        clock.tick(60)
                
    

    while not level_selected and full_ready:
        print("3")
        screen.fill(BLACK)
        print(is_player2)
        
        if is_player2:
            draw_text('You are Player 2', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            draw_text('Waiting for Player 1 to select level', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            # Check for messages from server
            pygame.display.update()

        # Handle level selection for player 1
        if is_player1:
            # Draw level selection menu
            # screen.fill(BLACK)
            draw_text('You are Player 1', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            
            draw_menu()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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

    while not in_game:
        #print("4")
        screen.fill(BLACK)
        draw_text('Wait for start', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        if start1 and start2:
            #print("send FullStart")
            client_socket.send("FullStart".encode())
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
    

    while in_game:
        
        
        screen.blit(levels[current_level]["backdrop"], (0, 0))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Leave = True
                time.sleep(1)  # use to let the thread close first before disconnecting the socket
                client_socket.send('quit'.encode())
                time.sleep(1)
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
            #send the message to the TCP server
            
            if is_player1:                
                client_socket.send(("1Score " + str(myscore)).encode())
            elif is_player2:
                client_socket.send(("2Score " + str(myscore)).encode())

        if is_player1:
            othertext = tiny_font.render(f"Others Score: {P2Score}", True,"white")
            screen.blit(othertext,(600,0))
        
        if is_player2:
            othertext = tiny_font.render(f"Others Score: {P1Score}", True,"white")
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

    while game_over:
        screen.fill(BLACK)
        wallpaper = pygame.image.load("assets/levelSelect.png")
        wallpaper.set_alpha(128)
        screen.blit(wallpaper, (0,0))

        #draw_text('test', tiny_font, WHITE, SCREEN_WIDTH // 9, SCREEN_HEIGHT // 3)
        
        if GameOver1 and GameOver2:
            print("both game over")
            both_game_over = True

        if both_game_over:
            if is_player1:
                print("gameover 1 finish")
                if (score > P2Score):
                    draw_text('Game Over ! YOU WIN !', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                elif (score < P2Score):
                    draw_text('Game Over ! YOU LOSE !', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                else:
                    draw_text('Game Over !!!', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                
                draw_text(f'Final Score: {score}', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 80)
                draw_text(f'Player2 score: {P2Score}', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 160)
                draw_text('Press 0 to go back to the main menu', tiny_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 240)
                draw_text('Press 1 to show leaderboard', tiny_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 280)
                pygame.display.update()
                clock.tick(60)
            
            if is_player2:
                print("gameover 1 finish")
                if (score > P1Score):
                    draw_text('Game Over ! YOU WIN !', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                elif (score < P1Score):
                    draw_text('Game Over ! YOU LOSE !', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                else:
                    draw_text('Game Over !!!', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

                draw_text(f'Final Score: {score}', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 80)
                draw_text(f'Player1 score: {P1Score}', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 160)
                draw_text('Press 0 to go back to the main menu', tiny_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 240)
                draw_text('Press 1 to show leaderboard', tiny_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5 + 280)
                pygame.display.update()
                clock.tick(60)

            
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
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

        while leaderboard:
            screen.fill(BLACK)
            client_socket.send(("Leaderboard" +"/"+ str(current_level)).encode())
            time.sleep(0.2)
            # Define the position to start rendering the text

            draw_text('LeaderBoard', small_font, WHITE, SCREEN_WIDTH // 2, 60)

            x = SCREEN_WIDTH // 5
            y = SCREEN_HEIGHT // 5

            # Render the leaderboard data as text on the screen
            for i, entry in enumerate(leaderboard_data):
                # Render the player name
                name_text = font.render(f"{i+1}. {entry['name']}", True, (255, 255, 255))
                screen.blit(name_text, (x, y + i*45))
                
                # Render the player score
                score_text = font.render(str(entry['score']), True, (255, 255, 255))
                screen.blit(score_text, (x + 500, y + i*45))

            # Update the display
            pygame.display.update()

            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
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
