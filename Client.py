# -*- coding: utf-8 -*-
import socket
import MessageReceiver
import json
import datetime

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
        self.loggedIn = False

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        self.connection.connect((self.host, self.server_port))


    def disconnect(self):
        self.connection.close()

    def receive_message(self, message):
        timestamp = datetime.datetime.fromtimestamp(int(message["timestamp"])).strftime('%Y-%m-%d %H:%M:%S')
        sender = message["sender"]
        response = message["response"]
        content = message["content"]


        if response == "message":
            print "@ Melding fra " + sender + " ("+timestamp+"):"
            print ">> " + content

        elif response == "info":
            print "@ Info fra server ("+timestamp+"):"
            print content

        elif response == "history":
            print "\n-------------- HISTORIE -----------------"
            if not content:
                print "Ingen historie å vise."
            else:
                for msg in content:
                    self.receive_message(msg)
            print "----------------------------------------\n"

        elif response == "error":
            print "@ Error ("+timestamp+"):"
            print content

        else:
            print "@ Udefinert response fra " + sender + " ("+timestamp+"):"
            print content


    def send_payload(self, data):
        # Tar inn argumenter på formen: [<request>, <content>]
        # Dumper argumenter på formen: {'request': <request>, 'content': <content>}'

        temp = {'request': data[0], 'content': data[1]}
        payload = json.dumps(temp)          #dumps() tar inn string som parameter, dump() tar inn file som parameter.
        self.connection.sendall(payload)

    def login(self, username):
        data = ["login", username]
        self.send_payload(data)

        payload = self.connection.recv(4096)
        message = json.loads(payload)
        self.receive_message(message)

        #Create a MessageReceiver thread
        self.messagereceiver = MessageReceiver.MessageReceiver(self, self.connection)
        self.messagereceiver.start()

    def logout(self):
        data = ["logout", None]
        self.send_payload(data)

        #Close the MessageReceiver thread
        self.messagereceiver.join()
        self.loggedIn = False


    def retrieve_names(self):
        data = ["names", None]
        self.send_payload(data)

    def help(self):
        if self.loggedIn:
            data = ["help", None]
            self.send_payload(data)
        else:
            print "**********************************"
            print "-----  Supported requests  -----"
            print "/login <username>"
            print "<message>"
            print "/names"
            print "/help"
            print "/logout"
            print "/disconnect"
            print "**********************************\n"

    def send_message(self, message):
        data = ["msg", message]
        self.send_payload(data)

    def main(self):

        print "**************************************"
        print "* * * * * Velkommen til chat * * * * *"
        print "**************************************\n"
        print "-----  Funksjoner  -----"
        print "<message>"
        print "/login <username>"
        print "/logout"
        print "/names"
        print "/disconnect"
        print "/help\n"

        while True:
            input = raw_input()
            if input.startswith("/login"):
                self.login(input[6:].strip())
                self.loggedIn = True

            elif input.startswith("/logout"):
                self.logout()
                self.disconnect()

            elif input.startswith("/names"):
                if self.loggedIn:
                    self.retrieve_names()
                else:
                    print "Error: Du må være logget inn for å bruke denne funksjonen"

            elif input.startswith("/help"):
                self.help()

            elif input.startswith("/disconnect"):
                if self.loggedIn:
                    print "Error: Du må logge ut før du kan avslutte programmet"
                else:
                    self.disconnect()
                    break

            else:
                if self.loggedIn:
                    self.send_message(input)
                else:
                    print "Error: Du må være logget inn for å bruke denne funksjonen"



if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client("localhost", 9998)           #78.91.72.240
    client.main()



# Håndtere error og log-in
# - handleInfo ()
# - handleError ()
# - handleHistory ()
# - handleMessage ()


#Endring