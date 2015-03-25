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
    messages = []

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        print "New client registered."

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            data = json.loads(received_string)
            request = data["request"]
            content = data["content"]

            if request == "login":
                ClientHandler.clients.append(self)
                self.username = content
                self.send_payload(["info", "Du er nå logget inn. Velkommen!"])
                if self.messages:
                    self.send_payload(["history", self.messages])

            elif request == "logout":
                if not self.loggedIn():
                    self.send_payload("Error", "Du er ikke logget inn enda.")

                ClientHandler.clients.remove(self)
                self.send_payload(["info", "Du er nå logget av. Velkommen tilbake!"])

            elif request == "names":
                c = []
                for client in ClientHandler.clients:
                    c.append(client.username)
                self.send_payload(["info", c])

            elif request == "help":
                string = "**********************************\n" \
                         "-----  Supported requests  -----\n" \
                         "login <username>\n" \
                         "msg <message>\n" \
                         "names\n" \
                         "help\n" \
                         "**********************************\n"
                self.send_payload(["info", string])

            elif request == "msg":
                #Debug
                print content
                #Debug
                self.messages.append(data)
                self.broadcast(["message", content])

            else:
                self.send_payload(["error", "Request not supported by server."])



    def send_payload(self, data):
        payload = json.dumps({"timestamp": time.time(), "sender": self.username, "response": data[0], "content": data[1]})
        self.connection.sendall(payload)

    def broadcast(self, data):
        for client in ClientHandler.clients:
            if client != self:
                payload = json.dumps({"timestamp": time.time(), "sender": self.username, "response": data[0], "content": data[1]})
                client.connection.sendall(payload)

    def loggedIn(self):
        return self.clients.contains(self)


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
    HOST, PORT = "", 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
