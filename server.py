#! /usr/env/bin python2.6
# -*- coding: utf-8 -*-
"""
    server

    description

    @copyright: 2010 DiogenesAugusto <diofeher@gmail.com>
    @license: see LICENSE.
"""

from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
import re
import settings


class Connection(object):
    """
    Wrapper used in connection
    """
    def __init__(self, s, addr):
        self.socket = s
        ip, port = addr
        self.ip = ip
        self.port = self.port
        self.nick = "Guest %s" % randint(0, 1000)


class Server(object):
    """TCP Socket Server"""
    def __init__(self, host, port):
        """
        Server class used to wrapper sockets
        
        @param s: socket
        @param host: unicode
        @param port: int
        """
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((host, port))
        self.connections = []
        
    def listen(self, max_number):
        """
        @param num: number of maximum connections
        """
        self.socket.listen(max_number)

    def accept(self):
        con, address = self.socket.accept()
        print con, address
        self.connections.append(con)
        
        thread = Thread(target=self.connection, args=(con,))
        thread.start()
        
    def connection(self, con):
        while 1:
            data = con.recv(1024)
            # handle messages
            if data:
                nick = re.search('^(/nick) (.+)', data)
                if nick:
                    new_nick = nick.group(2)
                    self.send_broadcast("bixin mudou nick para %s" % new_nick)
                else:
                    data = "fulano disse: %s" % data
                    self.send_broadcast(data)
            else:
                break
        con.close()
        
    def send_msg(self, con, msg):
        """
        send data
        """
        con.send(msg)
        
    def send_broadcast(self, msg):
        for con in self.connections:
            self.send_msg(con, msg)
        
    def close_connection(self, con):
        """
        close connection
        """
        con.close()
    
    def disconnect(self):
        """
        shut down the server
        """
        self.socket.close()

server = Server(settings.HOST, settings.PORT)
server.listen(5)  # maximum of 5 connections

while 1:
    try:
        # accepting connections
        server.accept()
    except:
        server.disconnect()