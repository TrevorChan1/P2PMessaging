# P2PMessaging

Implements a peer-to-peer messaging system where users can send and receive messages

## p2pMessager(name, port)

Main function to be run. User calls this function with their name and desired port to listen for messages on. This function will then 1. Check that the name doesn't already exist and, if it doesn't, start an instance of receiveMessage then loop asking for recipient name for sending messages using sendMessage.

### receiveMessage(host, port)

Function that, when given a host and port will create a socket then wait to accept a connection request on that host and port number. Whenever it finds a new connection, it will loop infinitely waiting to receive messages from that sender then will print that message and their name until the connection is stopped. 

### sendMessage(host, port, message)

Function that runs once to send a message. In p2pMessager, it is ran in a separate thread so multiple messages can be sent without waiting for the previous to be done. This function takes in as input the host and port and message, and will send the message to the desired port.