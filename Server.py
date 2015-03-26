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
        self.username = None

        print "New client registered."

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            data = json.loads(received_string)
            request = data["request"]
            content = data["content"]

            if request == "login":
                if self.loggedIn():
                    self.send_payload(["error", "Already logged in."])
                else:
                    valid, msg = self.isValidUsername(content)
                    if valid == "error":
                        self.send_payload([valid, msg])
                    else:
                        ClientHandler.clients.append(self)
                        self.username = content
                        self.send_payload(["info", "You're now logged in. Welcome!"])
                        self.send_payload(["history", self.messages])
                        print "User logged in: " + self.username

            elif request == "logout":
                if not self.loggedIn():
                    error = ["error", "Not yet logged in."]
                    self.send_payload(error)
                else:
                    ClientHandler.clients.remove(self)
                    self.send_payload(["info", "You're now logged out. Welcome back!"])
                    print "User logged out: " + self.username

            elif request == "names":
                if not self.loggedIn():
                    error = ["error", "Not yet logged in."]
                    self.send_payload(error)
                else:
                    c = []
                    for client in ClientHandler.clients:
                        c.append(client.username)
                    self.send_payload(["info", c])

            elif request == "help":
                string = "**********************************\n" \
                         "-----  Supported requests  -----\n" \
                         "/login <username>\n" \
                         "<message>\n" \
                         "/names\n" \
                         "/help\n" \
                         "/logout\n" \
                         "/disconnect\n" \
                         "**********************************\n"
                self.send_payload(["info", string])

            elif request == "msg":
                if not self.loggedIn():
                    error = ["error", "Not yet logged in."]
                    self.send_payload(error)
                else:
                    self.broadcast(["message", content])

            else:
                self.send_payload(["error", "Request not supported by server."])



    def send_payload(self, data):
        payload = json.dumps({"timestamp": time.time(), "sender": self.username, "response": data[0], "content": data[1]})
        self.connection.sendall(payload)

    def broadcast(self, data):
        data = {"timestamp": time.time(), "sender": self.username, "response": data[0], "content": data[1]}
        ClientHandler.messages.append(data)
        payload = json.dumps(data)
        for client in ClientHandler.clients:
            if client != self:
                client.connection.sendall(payload)

    def loggedIn(self):
        return self in self.clients

    def isValidUsername(self, content):
        if content=="" or content.isspace():
            msg = "Cannot have emtpy username."
            return "error", msg
        elif ClientHandler.clients:
            for client in ClientHandler.clients:
                name = client.username
                if name == content:
                    msg = "Username \"" + content + "\" is already taken"
                    return "error", msg

        for c in content:
            if not ("a" <= c <= "z") or ("A" <= c <= "Z") or ("0" <= c <= "9"):
                return "error", "Letters in username must be a-z, A-Z or 0-9."

        return "valid", "msg"


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
