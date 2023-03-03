import pygame
import socket
import threading
import time

from wconnection import FPGA

from pygame import mixer

pygame.init()
mixer.init()

#FPGA data
fpga = FPGA() #instance of FPGA class
fpga.start_communication()
#fpga.read() ==> gets reading in that point in time

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

clock = pygame.time.Clock()

# Define keys and their colors
keys = [{'rect': pygame.Rect(200, 500, 80, 80), 'color1': RED, 'color2': (180, 0, 0), 'label': 'L'},    
        {'rect': pygame.Rect(400, 500, 80, 80), 'color1': GREEN, 'color2': (0, 180, 0), 'label': 'U'},    
        {'rect': pygame.Rect(600, 500, 80, 80), 'color1': BLUE, 'color2': (0, 0, 180), 'label': 'D'},    
        {'rect': pygame.Rect(800, 500, 80, 80), 'color1': (255, 255, 0), 'color2': (180, 180, 0), 'label': 'R'},]

# Define levels
# 2/3 level are not implemented yet
levels = [{'name': 'Freedom Dive', 'file': 'freedom dive.txt', 'music': 'freedom dive.mp3'},
          {'name': 'Canon in D', 'file': 'canon_in_d.txt', 'music': 'canon_in_d.mp3'},
          {'name': 'Moonlight Sonata', 'file': 'moonlight_sonata.txt', 'music': 'moonlight_sonata.mp3'}]



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

'''
def draw_menu():
    screen.fill(BLACK)
    draw_text('Select a level', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

    # Draw level options
    for i, level in enumerate(levels):
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2 + i * 60
        draw_text(f'{i+1}. {level["name"]}', small_font, WHITE, x, y)

        '''
        
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

# Start game loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



def receive():
    # Wait for start signal from server
    global in_game
    while not Leave:
       
            global full_ready, is_player1, is_player2, is_player1_ready, is_player2_ready
            global connected, ready_num, player_num, level_selected, start1, start2, current_level
            global P1Score, P2Score, GameOver1, GameOver2
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

            elif data.isdigit():
                if is_player1:
                    P2Score = int(data)
                    print(P2Score)
                    print(" ")
                elif is_player2:
                    P1Score = int(data)
                    print(P1Score)
                    print(" ")

            elif data == "2GameOver":
                GameOver2 = True
            
            elif data == "1GameOver":
                GameOver1 = True

            elif data == "quit":
                print("receive quit")
                break


connected = False
is_player1 = False
is_player2 = False
is_player1_ready = False
is_player2_ready = False

while True:
    # define constant
    game_over = False
    in_game = False
    full_ready = False
    
    
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

    # Start the receive data thread
    receive_thread = threading.Thread(target=receive)
    #receive_thread.setDaemon(True)
    receive_thread.start()
    
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
   
        
    while not full_ready and connected:
        #print("2")
        #print(is_player1)
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
            draw_text('Select a level', big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

            # Draw level options
            draw_text(f'{levels[current_level]["name"]}', small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80 )
    
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
                    if event.key == pygame.K_RETURN:
                        client_socket.send(("level " + str(current_level)).encode())
                        time.sleep(0.5)
                        client_socket.send("LevelS1".encode())
                        level_selected = True
                    elif event.key == pygame.K_1:
                        current_level += 1
                        if current_level >= len(levels):
                            current_level = 0     
        
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
                
    
    # Load level and start game
    map_rect = load_level(levels[current_level])
    combo = 1
    
    messages = []

    clock = pygame.time.Clock()
    game_over = False
    #in_game = True
    

    while in_game:
        
        
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

        # Handle key events
        reading = fpga.read()
        for key in keys:
            if reading == key['label']:
                pygame.draw.rect(screen, key['color1'], key['rect'])
                key['pressed'] = True
            else:
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

            if is_player2:
                GameOver2 = True
                client_socket.send("2GameOver".encode())
             
              
            
        # Update display and tick clock
        pygame.display.update()
        clock.tick(60)

    is_player1_ready = False
    is_player2_ready = False

    while game_over:
        screen.fill(BLACK)
        

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
                    
        if not game_over:
            break
