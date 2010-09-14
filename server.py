#! /usr/env/bin python2.6
# -*- coding: utf-8 -*-
"""
    server

    description

    @copyright: 2010 DiogenesAugusto <diofeher@gmail.com>
    @license: see LICENSE.
"""
from random import randint
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
import re
import settings

try:
    HOST = sys.argv[1]
except:
    HOST = settings.HOST

WELCOME_MSG = """
######################################################
#                     P.O.D. CHAT PY                 #
######################################################
# To speak, just write and click in 'Send a message' #
# To change your nick: /nick new_nick                #
# To quit: /quit                                     #
######################################################

"""


class Connection(object):
    """
    Wrapper used in connection
    """
    def __init__(self, s, addr):
        self.socket = s
        ip, port = addr
        self.ip = ip
        self.port = port
        self.nick = "Guest %s" % randint(0, 1000)
        self.socket.send(WELCOME_MSG)
        
    def to_s(self):
        return "%s (%s-%s)" % (self.nick, self.ip, self.port)


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
        self.sockets = {}
        
    def listen(self, max_number):
        """
        @param num: number of maximum connections
        """
        self.socket.listen(max_number)

    def accept(self):
        sock, address = self.socket.accept()
        connection = Connection(sock, address)
        self.sockets.update({sock:connection})
        self.send_broadcast("%s has joined chat." %  connection.nick)
        
        thread = Thread(target=self.connection, args=(sock, connection))
        thread.start()
        
    def connection(self, sock, connection):
        try:
            while 1:
                data = sock.recv(4056)
                # handle messages
                if data:
                    nick = connection.nick
                    nick_regex = re.search('^/nick (.+)', data)
                    quit = re.search('^quit.+', data)
                    if nick_regex:
                        new_nick = nick_regex.group(1)
                        connection.nick = new_nick
                        self.send_broadcast("%s is now known as %s" % (nick, new_nick))
                    elif quit:
                        break
                    else:
                        data = "%s says: %s" % (connection.to_s(), data)
                        self.send_broadcast(data)
                else:
                    break
        except Exception, e:
            print e
        finally:
            self.send_broadcast("%s has left chat." % connection.nick)
            self.sockets.pop(sock)
            sock.close()
        
    def send_msg(self, con, msg):
        """
        Wrapper used to send data
        """
        con.send(msg)
        
    def send_broadcast(self, msg):
        """
        Send message to all clients connected
        """
        for sock in self.sockets:
            self.send_msg(sock, msg)
        
    def close_connection(self, con):
        """
        Close connection
        """
        con.close()
    
    def disconnect(self):
        """
        Shut down the server
        """
        self.socket.close()

server = Server(HOST, settings.PORT)
server.listen(5)  # maximum of 5 connections

while 1:
    try:
        # accepting connections
        server.accept()
    except:
        server.disconnect()