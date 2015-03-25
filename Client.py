# -*- coding: utf-8 -*-
import socket
import MessageReceiver
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        self.host = host
        self.server_port = server_port

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

        self.messagereceiver = MessageReceiver.MessageReceiver(self, self.connection)
        self.messagereceiver.start()

        self.loggedIn = False

        # TODO: Finish init process with necessary code

    def run(self):
        self.connection.connect((self.host, self.server_port))

    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        print message

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        # Tar inn argumenter på formen: [<request>, <content>]
        # Dumper argumenter på formen: {'request': <request>, 'content': <content>}'
        # Payload sendes på formen:
        temp = {'request': data[0], 'content': data[1]}
        payload = json.dumps(temp)          #dumps() tar inn string som parameter, dump() tar inn file som parameter.
        self.connection.sendall(payload)

    def login(self, username):
        data = ['login', username]
        self.send_payload(data)

    def logout(self):
        pass

    def retrieve_names(self):
        pass

    def help(self):
        print "\n***********************"
        print "Dette er litt hjelp"
        print "***********************\n"

    def send_message(self, message):
        data = ['msg', message]
        self.send_payload(data)

    def main(self):
        print "**************************************"
        print "* * * * * Velkommen til chat * * * * *"
        print "**************************************\n"
        print "For å logge inn: Skriv /login username"
        while True:
            input = raw_input()
            if input.startswith("/login"):
                if self.loggedIn:
                    print "Already logged in."
                self.login(input[6:].strip())
                self.loggedIn = True

            elif input.startswith("/logout"):
                if not self.loggedIn:
                    print "Not logged in."

            elif input.startswith("/names"):
                if not self.loggedIn:
                    print "Not logged in."
                else:
                    self.retreive_names()

            elif input.startswith("/help"):
                self.help()

            else:
                if not self.loggedIn:
                    print "Du er ikke logget inn enda. Skriv /login username."
                else:
                    self.send_message(input)


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
    client.main()



# Håndtere error og log-in
# - handleInfo ()
# - handleError ()
# - handleHistory ()
# - handleMessage ()


#Endring