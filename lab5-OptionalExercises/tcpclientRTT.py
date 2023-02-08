import socket
import time
print("We're in tcp client...");
#the server name and port client wishes to access
server_name = '3.8.190.35' #Public IPv4 address of the instance
#'52.205.252.164'
server_port = 12000



counter = 0
totalTime = 0
while (counter < 500):
    #create a TCP client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Set up a TCP connection with the server
    #connection_socket will be assigned to this client on the server side
    client_socket.connect((server_name, server_port))
    
    msg = input("Enter an integer: ");
    start = time.time() #starts timer right before sending
        #send the message to the TCP server
    client_socket.send(msg.encode())
        #return values from the server
    msg = client_socket.recv(1024)
    stop = time.time() #stops timer right after receiving
    print(msg.decode())

    
    rtt = stop - start #logs time for this round trip
    print("Time in seconds for this Round Trip: " + str(rtt))

    totalTime += rtt
    counter += 1

    print("Moving average: " + str(totalTime/counter))
    client_socket.close()
    
    


