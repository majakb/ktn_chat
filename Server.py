# -*- coding: utf-8 -*-
import SocketServer
import json
import time


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    clients = []

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            data = json.loads(received_string)
            request = data["request"]

            if request == "login":
                ClientHandler.clients.append(self)
                self.username = data["content"]
                self.send_response("info", "Du er nå logget inn. Velkommen!")

            elif request == "logout":
                pass

            elif request == "names":
                pass

            elif request == "msg":
                self.broadcast(data["content"])

            else:
                raise ValueError("Ugyldig argument til serveren.")
            
            # TODO: Add handling of received payload from client

    def broadcast(self, data):
        for client in ClientHandler.clients:
            payload = json.dumps({"timestamp": 3, "sender": self.username, "response": "message", "content": data})
            client.connection.sendall(payload)

    def send_response(self, response, content):
        data = {"timestamp": time.time(), "sender": "Server", "response": response, "content": content}
        payload = json.dumps(data)
        self.connection.sendall(payload)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations is necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations is necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
