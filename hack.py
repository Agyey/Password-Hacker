import socket
import sys
from itertools import product
## PART 1
# # Get hostname, port and message
# args = sys.argv
# hostname, port, message = args[-3:]
# address = (hostname, int(port))
#
# # Create Socket and connect
# with socket.socket() as connection_socket:
#     connection_socket.connect(address)
#     # Send Message
#     connection_socket.send(message.encode())
#     # Get Response
#     response = connection_socket.recv(1024)
#     print(response.decode())


## PART 2
# Get hostname and port
args = sys.argv
hostname, port = args[-2:]
address = (hostname, int(port))

# Create Socket and connect
with socket.socket() as connection_socket:
    connection_socket.connect(address)
    options = 'abcdefghijklmnopqrstuvwxyz0123456789'
    i = 1
    while True:
        possibilities = product(options, repeat=i)
        for possibility in possibilities:
            password = "".join(possibility)
            # Send Password
            connection_socket.send(password.encode())
            # Get Response
            response = connection_socket.recv(1024).decode()
            # Print Password if Found
            if response == 'Connection success!':
                print(password)
                exit()
            if response == 'Too many attempts':
                print('Not Found')
                exit()
        i += 1
