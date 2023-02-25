import socket
import time

# Set up the TCP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the server name and port
server_name = '54.210.203.6'
server_port = 12000

# Connect to the server
client_socket.connect((server_name, server_port))
print('Connected to server')

# Send requests to the server
i = 0
myscore = 50

while i < 80:
    client_socket.send(str(myscore).encode()) 
    time.sleep(0.3)
    myscore += 5   
    i += 1

# Close the connection
client_socket.send('quit'.encode())
time.sleep(1)
client_socket.close()
print('Connection closed')