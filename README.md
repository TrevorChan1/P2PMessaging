# P2PMessaging

Implements a peer-to-peer messaging system where users can send and receive messages. The main idea is that once a user runs p2pMessager, it'll prompt the user for their username so that the database can create a user with that name and port if they don't already exist. 

From there, it will start listening for anyone wanting to send in messages in a thread running receiveMessage. This thread will continuously loop, search for any new connection requests, accept those requests and start a new thread that will print any new messages with the sender's name (found from the database).

In the main thread, it will prompt the user for the name of the person they wish to send messages to. Once a user in the database is written, the user can send as many messages as they want (each sent message creates a new thread). The code was designed this way to act like text messager systems where you select the person you want to send messages to and can send them as many as you want (and then switch out by entering "exit").

## p2pMessager(name, port)

Main function to be run. User calls this function with their name and desired port to listen for messages on. This function will then 1. Check that the name doesn't already exist and, if it doesn't, start an instance of receiveMessage then loop asking for recipient name for sending messages using sendMessage.

### receiveMessage(host, port)

Function that, when given a host and port will create a socket then wait to accept a connection request on that host and port number. Whenever it finds a new connection, it will loop infinitely waiting to receive messages from that sender then will print that message and their name until the connection is stopped. 

### sendMessage(host, port, message)

Function that runs once to send a message. In p2pMessager, it is ran in a separate thread so multiple messages can be sent without waiting for the previous to be done. This function takes in as input the host and port and message, and will send the message to the desired port.

## Database (SQLite3)

The database implements a user database that can create new users, search for existing users, and grab those users' names when logging in or receiving messages.

### User table

Used to index into and create new users for establishing a messager instance and for receiving / sending messages.

CREATE TABLE users (
   ...> name text NOT NULL,
   ...> ip text NOT NULL,
   ...> port int NOT NULL,
   ...> UNIQUE(ip, port));

### Unread Messages

Table that contains all missed messages for the user (if not properly able to send)

CREATE TABLE unread_messages (
   ...> msg TEXT NOT NULL,
   ...> ip TEXT NOT NULL,
   ...> port int NOT NULL,
   ...> time_stamp TEXT NOT NULL,
   ...> FOREIGN KEY (ip) REFERENCES users(ip),
   ...> FOREIGN KEY (port) REFERENCES users(port));



