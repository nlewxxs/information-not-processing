import socket
import threading
import time

# Define constants
HOST = '0.0.0.0'
PORT = 12000

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

# Define a function to handle a client connection
def handle_client(conn,addr):
    global connected_clients, connection_times, player1_conn, player2_conn, ready1, ready2, LevelS1, LevelS2
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