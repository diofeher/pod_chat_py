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
from Tkinter import Tk, Button, Text, LEFT, TOP, Entry
import Queue
import settings

class ThreadSafeText(Text):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.queue = Queue.Queue()
        self.update_me()
    def write(self, line):
        self.queue.put(line)
    def clear(self):
        self.queue.put(None)
    def update_me(self):
        try:
            while 1:
                line = self.queue.get_nowait()
                if line is None:
                    self.delete(1.0, END)
                else:
                    self.insert(END, str(line))
                self.see(END)
                self.update_idletasks()
        except Queue.Empty:
            pass
        self.after(100, self.update_me)

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
        thread = Thread(target=self.receiving)
        thread.start()
        
        # TODO: Mount widget
        self.text = ThreadSafeText()
        self.text.pack(side=TOP)
        self.send = Button(text="Send a message", command=self.send_message)
        self.send.pack(side=LEFT)
        self.input = Entry()
        self.input.pack(side=LEFT)
        
    def receiving(self):
        data = self.socket.recv(1024)
        self.text.insert('end', data)
    
    def send_message(self):
        msg = self.input.get()
        self.socket.send(msg)
        
    def disconnect(self):
        self.socket.close()
        
if __name__=="__main__":
    client = Client(settings.HOST, settings.PORT)
    root = Tk()
    root.mainloop()