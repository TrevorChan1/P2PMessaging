import socket
import threading
import queue
import sqlite3
import datetime

users = {"Trevdawg" : [socket.gethostbyname(socket.gethostname()), 6969],
         "Testopher" : [socket.gethostbyname(socket.gethostname()), 56784]}

db = "p2p_database.db"

# Function that sends a message given a target and message
def sendMessage(host, port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.sendto(message, (host, port))
    except:
        # If message fails to send, add it to the database for the user to receive on login
        con = sqlite3.connect(db)
        time = datetime.datetime.now()
        con.execute("INSERT INTO unread_messages (msg, ip, port, time_stamp) VALUES (?, ?, ?, ?)", message, host, port, str(time))
    return 0

# Top level message receiver that waits for connection requests and generates multiple connections
def receiveMessage(host, port):

    # Create a socket and bind it to the host / port of the input
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.bind(host,port)

    while (True):
        # Accept connections
        ip, addr = r.accept()
        con = sqlite3.connect(db)
        cur = con.cursor()

        # When it gets a connection, check if the ip and address are a known user
        cur.execute("SELECT name FROM user WHERE ip=" + host + " AND port=" + port)
        user = cur.fetchall()

        # If user not in database set them as UNKNOWN (still allow messages)
        if len(user) == 0:
            name = "UNKNOWN"
        else:
            name = user[0]
        
        # Create a new thread that will listen for traffic each time a new request is sent
        threading.Thread(target=receiveConnection, args=(name, r))
    
    r.close()
        
        
# Helper function that handles each individual connection to receive and print messages
def receiveConnection(name, sock):
    # Run until the sender asks to exit the connection
    connectionOn = True
    while (connectionOn):

         # While receiving messages, print out the messages
        message = sock.recv(1024)
        if (message == "exit"):
            connectionOn = False
        else:
            print(name + ":", message)
    
    # Terminate the connection by closing the socket
    sock.close()

        



    

# Function that opens user to be messaged and sent message to
def p2pMessager(name, port):
    # Check if the user exists on the P2P service already
    if (name in users):
        print("ERROR: User already exists")
        return -1
    

    # Add new user to users (to be changed into database or server implementation)
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)

    con = sqlite3.connect(db)
    cur = con.cusor()
    cur.execute("SELECT name FROM user WHERE ip=" + host + " AND port=" + port)
    user = cur.fetchall()

    # If user doesn't exist, create a new user in database
    if (len(user) == 0):
        con.execute("INSERT INTO users (name, ip, port) VALUES (?, ?, ?, ?)", name, host, port)

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
            con = sqlite3.connect(db)
            cur = con.cusor()
            cur.execute("SELECT ip, port FROM user WHERE name=" + name)
            user = cur.fetchall()

            if (len(user) == 2):
                dest_socket = [user[0], user[1]]
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

# p2pMessager("Trevdawg", 1050)