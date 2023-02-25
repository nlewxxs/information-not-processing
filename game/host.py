import socket
import threading

server_port = 12000

#create a welcoming socket
welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind the server to the localhost at port server_port
welcome_socket.bind(('0.0.0.0',server_port))
welcome_socket.listen(1)

# define a dictionary to store client connections and their scores
client_scores = {}

# define a function to handle each client connection
def handle_client_connection(conn, addr):
    # send a welcome message to the client
    conn.send('Welcome to the server!'.encode())

    # loop to receive data from the client
    while True:
        data = conn.recv(1024).decode()
        print(data)
        if data:
            # if the data is a score update, store it in the client_scores dictionary
            if data.isdigit():
                client_scores[addr[1]] = int(data) # addr[1] = port number, two computers under same network only difference is port number
                print(f'Received score update from {addr}: {data}')
            # if the data is a request for the other player's score, send it back to the client
            elif data == 'get_score':
                other_clients = [k for k in client_scores.keys() if k != addr[1]]
                #print(len(other_clients))
                if len(other_clients) == 1:
                    other_client = other_clients[0]
                    other_score = client_scores.get(other_client, 0)
                    print("1:"+str(other_score))
                    conn.send(str(other_score).encode())
                elif len(other_clients) == 0:
                    print("0:"+str(100))
                    conn.send(str(100).encode())
            elif data == 'quit':
                break
            # if the data is not recognized, print an error message
            else:
                print(f'Error: unrecognized data received from {addr}: {data}')
        

        # remove the client's connection from the dictionary and close the connection
    print(client_scores)
    
    if addr[1] in client_scores:
        client_scores.pop(addr[1])
    conn.close()
    print(f'Connection closed: {addr}')

# loop to accept incoming connections
while True:
    conn, addr = welcome_socket.accept()
    print(f'Connected by {addr}')

    # create a thread to handle the client connection
    client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr))
    client_thread.start()