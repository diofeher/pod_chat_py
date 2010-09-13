#! /usr/env/bin python2.6
# -*- coding: utf-8 -*-
"""
    client

    description

    @copyright: 2010 DiogenesAugusto <diofeher@gmail.com>
    @license: see LICENSE.
"""
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from Queue import Queue, Empty
from Tkinter import Tk, Button, Text, LEFT, TOP, Entry, END, DISABLED
import settings



class GUIClient(object):
    """Client"""
    def __init__(self, host, port, queue):
        """
        Wrapper used to control sockets and widgets
        
        @param host: unicode
        @param port: int
        """
        # Connecting socket
        self.queue = queue
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((host, port))
        
        # TODO: Mount widget
        self.text = Text()
        self.text.pack(side=TOP)
        self.input = Entry()
        self.input.pack(side=LEFT)
        self.send = Button(text="Send a message", command=self.send_message)
        self.send.pack(side=LEFT)
        
    def receive_message(self, msg):
        self.text.insert(END, msg + "\n")
    
    def send_message(self):
        msg = self.input.get()
        print msg
        self.socket.send(msg)

    def incoming(self):
         """
         Handle all the messages currently in the queue (if any).
         """
         while self.queue.qsize():
             try:
                 msg = self.queue.get(0)
                 # Check contents of message and do what it says
                 # As a test, we simply print it
                 self.receive_message(msg)
             except Empty:
                 pass
        
    def disconnect(self):
        self.socket.close()

class ThreadedClient(object):
    def __init__(self, master):
        self.master = master
        self.queue = Queue()
        self.gui = GUIClient(settings.HOST, settings.PORT, self.queue)
        
        self.thread = Thread(target=self.async_io)
        self.thread.start()
        
        # check if message incoming
        self.check_msgs()
        
    def check_msgs(self):
        self.gui.incoming()
        self.master.after(1000, self.check_msgs)
        
    def async_io(self):
        while 1:
            data = self.gui.socket.recv(1024)
            self.queue.put(data)
        
if __name__=="__main__":
    root = Tk()
    ThreadedClient(root)
    root.mainloop()
