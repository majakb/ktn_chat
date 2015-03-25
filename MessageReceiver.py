# -*- coding: utf-8 -*-
from threading import Thread
import simplejson

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and permits
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        super(MessageReceiver, self).__init__()

        self.client = client
        self.connection = connection

        # Flag to run thread as a deamon
        self.daemon = True



        # TODO: Finish initialization of MessageReceiver

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while True:
            payload = self.connection.recv(4096)
            message = simplejson.loads(payload)
            self.client.receive_message(message)