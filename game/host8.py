import socket
import threading
import time
import boto3
from boto3.dynamodb.conditions import Key
import json

# Define constants
HOST = '0.0.0.0'
PORT = 12000



import json






# Set up the TCP server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2) # listen up to two clients

# List of connected clients and their connection times
connected_clients = []
connection_times = []


# Define player connections and ready status variables
player1_conn = None
player2_conn = None
ready1 = False
ready2 = False
LevelS1 = False
LevelS2 = False

# define a dictionary to store client connections and their scores
client_scores = {}

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
leaderboard_table = dynamodb.Table('PlayerScores')

# Function to store player scores in DynamoDB
def store_player_score(server_name, name, score):
    table = dynamodb.Table('PlayerScores')
    response = table.put_item(
        Item={
            'serverIP': server_name,
            'name': name,
            'score': int(score)
        }
    )
    print("Score stored:", response)

def get_leaderboard(server_name):
    leaderboard_table = dynamodb.Table('PlayerScores')
    response = leaderboard_table.query(
        KeyConditionExpression=Key('serverIP').eq(server_name),
        ProjectionExpression='#n, score',
        ExpressionAttributeNames={'#n': 'name'},
        Limit=10,
        ScanIndexForward=False
        )
    items = response['Items']
    #leaderboard_sorted = sorted(items, key=lambda x: x['score'], reverse=True)
    leaderboard = []
    for item in items:
        name = item['name']
        score = float(item['score'])  # convert score to float
        leaderboard.append({'name': name, 'score': score})
    print(leaderboard)
    return leaderboard

    '''
    print("Leaderboard:")
    for item in items:
        print(item['name'], item['score'])
    '''


# Define a function to handle a client connection
def handle_client(conn,addr):
    global connected_clients, connection_times, player1_conn, player2_conn, ready1, ready2, LevelS1, LevelS2, client_scores
    global P1Score, P2Score
    q = False
    w = False
    while True:            
            data = conn.recv(1024).decode()
            #if not data:
                    #break
            '''
            if not q:
                 print("send start")
                 conn.send("start".encode())
                 q = True
            
            if not w:
                 print ("send player 1")
                 conn.send('player 1'.encode())
                 w = True
            '''

            if data == 'request':
                
                print("receive request")
                # Add the client and its connection time to the lists
                if conn not in connected_clients:
                    connected_clients.append(conn)
                    connection_times.append(time.time())
                    
                if len(connected_clients) == 2:
                    # Determine which client connected first and assign player 1 and player 2
                    if connection_times[0] < connection_times[1]:
                        player1_conn = connected_clients[0]
                        player2_conn = connected_clients[1]
                    else:
                        player1_conn = connected_clients[1]
                        player2_conn = connected_clients[0]
                    # Send player assignments to the clients
                    player1_conn.send('player 1'.encode())
                    player2_conn.send('player 2'.encode())
                    
                elif len(connected_clients) != 2:
                    print("not two players")

            elif data.startswith("Ready"):
                ready_num = int(data.split()[1])
                if ready_num == 1:
                    print("receive ready 1")
                    player2_conn.send('ready 1'.encode())
                    #ready1 = True
                elif ready_num == 2:
                    print("receive ready 2")
                    player1_conn.send('ready 2'.encode())
                    #ready2 = True
            
            elif data == "FullReady":
                print("send fullready")
                player1_conn.send('fullready'.encode())
                #time.sleep(0.1)
                player2_conn.send('fullready'.encode())
                time.sleep(1)

            elif data == "FullStart":
                print("send start")
                player1_conn.send('start'.encode())
                #time.sleep(0.1)
                player2_conn.send('start'.encode())
                time.sleep(1)
                

            elif data.startswith("level"):
                print("send to conn 2 level")
                current_level = int(data.split()[1])
                player2_conn.send(("level " + str(current_level)).encode())
                time.sleep(0.1)

            
            elif data == 'LevelS1':
                print("receive LevelS1")
                LevelS1 = True
                player1_conn.send("levelreceive 1".encode())    # should change here both send to player 1
            
            elif data == 'LevelS2':
                print("receive LevelS2")
                LevelS2 = True
                player1_conn.send("levelreceive 2".encode())    # should change here
            
            # if the data is a score update, store it in the client_scores dictionary
            elif data.isdigit():
                client_scores[addr[1]] = int(data) # addr[1] = port number, two computers under same network only difference is port number
                print(f'Received score update from {addr}: {data}')
                
            # if the data is a request for the other player's score, send it back to the client
            elif data == 'get_score':
                other_clients = [k for k in client_scores.keys() if k != addr[1]]
                #print(len(other_clients))
                if len(other_clients) == 1:
                    other_client = other_clients[0]
                    other_score = client_scores.get(other_client, 999)
                    print("1:"+str(other_score))
                    conn.send(str(other_score).encode())
                elif len(other_clients) == 0:
                    print("0:"+str(100))
                    conn.send(str(100).encode()) 

            elif data.startswith("1Score"):
                P1Score = int(data.split()[1])
                print("P1SCore" + str(P1Score))
                player2_conn.send((str(P1Score)).encode())
            
            elif data.startswith("2Score"):
                P2Score = int(data.split()[1])
                print("P2SCore" + str(P2Score))
                player1_conn.send((str(P2Score)).encode())
            
            elif data == "2GameOver":
                player1_conn.send("2GameOver".encode())

            elif data == "1GameOver":
                player2_conn.send("1GameOver".encode())
            
            elif data.startswith("Leaderboard"):
                # convert leaderboard list to a string
                LevelNo= data.split("/")[1]
                leaderboard_str = json.dumps(get_leaderboard(LevelNo))

                # send the leaderboard string to the client
                conn.send(leaderboard_str.encode())
            
            elif data == "1Minus":
                player1_conn.send("Minus".encode())

            elif data == "2Minus":
                player2_conn.send("Minus".encode())

            elif data == 'quit':
                    print('receive quit')
                    conn.send("quit".encode())
                    print("send quit")
                    time.sleep(0.1)
                    conn.close()
                    if conn in connected_clients:
                        connection_times.remove(connection_times[connected_clients.index(conn)])
                        connected_clients.remove(conn) 
                        print(f'Disconnected by {addr}')
                        print(connected_clients)
                        print(connection_times)                       
                    break
            
            elif data.startswith("serverName"):
                print("receiving")
                server_name,level, score, name = data.split("/")
                store_player_score(level, name, score)
                
                
            '''
    except ConnectionResetError:
        print("connectionRESETERROR")
        pass  # client disconnected unexpectedly
    finally:
            print('finally')
            conn.close()
            if conn in connected_clients:
                connected_clients.remove(conn)
                connection_times.remove(connection_times[connected_clients.index(conn)])
        '''
# Accept client connections and spawn a new thread to handle each one
while True:
    conn, addr = server_socket.accept()
    print(f'Connected by {addr}')
    thread = threading.Thread(target=handle_client, args=(conn,addr))
    thread.start()
