import socket
import threading
import queue

class target(socket.socket):
    def __init__(self, host, port):
        self = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(host, port)

users = [
    {"Trevdawg" : [socket.gethostbyname(socket.gethostname()), 6969]},
    {"Testopher" : [socket.gethostbyname(socket.gethostname()), 56784]}
]

# Function that sends a message given a target and message
def sendMessage(host, port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message, (host, port))
    reply = s.recv(1024)
    print(reply)

# Class for people currently sending messages
class sender(threading.Thread):

    def __init__(self, host, port):

# Function that will constantly wait for messages then print them
def receiveMessage(host, port):

    # Create a socket and bind it to the host / port of the input
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.bind(host,port)

    # 

# Function that opens user to be messaged and sent message to
def p2pMessager(name, port):
    # Check if the user exists on the P2P service already
    if (name in users):
        print("ERROR: User already exists")

    # Add new user to users (to be changed into database or server implementation)
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    users[name] = [host, port]

    # Create a thread for the receiver with the host and port as arguments
    threading.Thread(receiveMessage, (host, port))

    
