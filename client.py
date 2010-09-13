#! /usr/env/bin python2.6
# -*- coding: utf-8 -*-
"""
    client

    description

    @copyright: 2010 DiogenesAugusto <diofeher@gmail.com>
    @license: see LICENSE.
"""
from socket import socket, AF_INET, SOCK_STREAM
from Tkinter import Tk, Button, Text, LEFT, TOP, Entry
import settings

class Client(object):
    """Client"""
    def __init__(self, host, port):
        """
        Wrapper used to control sockets and widgets
        
        @param host: unicode
        @param port: int
        """
        # Connecting socket
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((host, port))
        
        # TODO: Mount widget
        self.text = Text()
        self.text.pack(side=TOP)
        self.send = Button(text="Send a message", command=self.send_message)
        self.send.pack(side=LEFT)
        self.input = Entry()
        self.input.pack(side=LEFT)
        
    def receiving(self):
        data = self.socket.recv(1024)
        self.text.insert('end', data)
        self.disconnect()
    
    def send_message(self):
        msg = self.input.get()
        self.socket.send(msg)
        
    def disconnect(self):
        self.socket.close()
        
if __name__=="__main__":
    client = Client(settings.HOST, settings.PORT)
    #client.receiving()
    root = Tk()
    root.mainloop()