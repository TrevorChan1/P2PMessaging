import socket
import threading
import queue

users = {"Trevdawg" : [socket.gethostbyname(socket.gethostname()), 6969],
         "Testopher" : [socket.gethostbyname(socket.gethostname()), 56784]}

# Function that sends a message given a target and message
def sendMessage(host, port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message, (host, port))
    return 0

# Function that will constantly wait for messages then print them
def receiveMessage(host, port):

    # Create a socket and bind it to the host / port of the input
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.bind(host,port)

    # Accept connections
    ip, addr = r.accept()

    # When it gets a connection, check if the ip and address are a known user
    user = [n for n, values in users.items() if values == [ip,addr]]
    if (user):
        name = user
    else:
        name = "UNKNOWN"

    # While receiving messages, print out the messages
    while True:
        message = r.recv(1024)
        print(name + ":", message)
    
    # Close the connection if possible
    r.close()


    

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
    threading.Thread(target=receiveMessage, args=(host, port))

    messager_open = True
    dest_socket = None

    # Loop until told to close the messager
    while (messager_open):

        # If there is no destination, ask for a name
        if (dest_socket == None):
            dest = input("Enter Receiver Name: ")

            # If told to exit, leave
            if (dest == "exit"):
                messager_open = False
                break
            
            # Otherwise, check if destination is a known user
            if (dest in users):
                dest_socket = users[dest]
            else:
                print("User not found")
                dest_socket = None

        # If a user is known, then inquire for message to send
        else:
            message = input("Enter message: ")

            # If asked to exit, exit the current user
            if (message == "exit"):
                dest_socket = None
            # Otherwise, create a thread sending the message
            else:
                threading.Thread(target=sendMessage, args=(dest_socket[0], dest_socket[1], message))

p2pMessager("Steve", 1050)