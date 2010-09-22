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
from Tkinter import Tk, Button, Text, LEFT, TOP, RIGHT, Entry, END, DISABLED, Scrollbar, Y
import re
import sys
import settings

try:
    HOST = sys.argv[1]
except:
    HOST = settings.HOST

class GUIClient(object):
    """
    Wrapper used to control sockets and widgets
    """
    def __init__(self, host, port, queue, thread_client):
        """
        @param host: unicode
        @param port: int
        @param queue: Queue
        """
        # initialization
        self.threaded_client=thread_client
        
        # Constants
        self.TEXT_WIDTH = 150
        self.INPUT_WIDTH = self.TEXT_WIDTH - self.TEXT_WIDTH/3
        
        # Connecting socket
        self.queue = queue
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((host, port))
        
        # Mount widgets
        scrollbar = Scrollbar()
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text = Text(width=self.TEXT_WIDTH, yscrollcommand=scrollbar.set)
        self.text.pack(side=TOP)
        self.input = Entry(width=self.INPUT_WIDTH)
        self.input.pack(side=LEFT)
        self.send = Button(text="Send a message", command=self.send_message)
        self.send.pack(side=LEFT)
        
        self.input.bind("<Return>", self.send_message_event)
        
    def receive_message(self, msg):
        """
        Receive message from socket and move scrollbar to end.
        """
        self.text.insert(END, msg + "\n")
        self.text.see(END)
    
    def send_message_event(self, event):
        self.send_message()
    
    def send_message(self):
        """
        Send message to server and clean Entry widget.
        """
        msg = self.input.get()
        self.input.delete(0, END)
        quit = re.search('^/quit.*', msg)
        self.socket.send(msg)
        if quit:
            self.threaded_client.close()


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
        """
        Disconnect socket
        """
        self.socket.close()
        

class ThreadedClient(object):
    def __init__(self, master):
        """
        Class used to handle threads and connect to GUI main thread.
        """
        self.master = master
        self.queue = Queue()
        self.gui = GUIClient(HOST, settings.PORT, self.queue, self)
        
        self.thread = Thread(target=self.async_io)
        self.thread.start()
        
        # check if message incoming
        self.check_msgs()
        
    def check_msgs(self):
        """
        Check messages incoming and send to GUI.
        """
        self.gui.incoming()
        self.master.after(1000, self.check_msgs)
        
    def async_io(self):
        """
        Wait and put in queue messages from server.
        """
        while 1:
            data = self.gui.socket.recv(4056)
            self.queue.put(data)
            
    def close(self):
        """
        Close application
        """
        sys.exit(0)
        
if __name__=="__main__":
    root = Tk()
    thr_cli = ThreadedClient(root)
    root.protocol("WM_DELETE_WINDOW", thr_cli.close)
    root.mainloop()
