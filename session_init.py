import socket
import threading
import queue

class target(socket.socket):
    def __init__(self, host, port):
        self = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(host, port)


