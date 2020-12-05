import socket
import sys

# Get hostname, port and message
args = sys.argv
hostname, port, message = args[-3:]
address = (hostname, int(port))

# Create Socket and connect
with socket.socket() as connection_socket:
    connection_socket.connect(address)
    # Send Message
    connection_socket.send(message.encode())
    # Get Response
    response = connection_socket.recv(1024)
    print(response.decode())
