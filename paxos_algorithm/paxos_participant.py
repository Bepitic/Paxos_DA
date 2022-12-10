from threading import Thread 
from algorithm import Components
import sys
import socket
import struct
import json

class Proposer:
    def __init__(self, proposer_id, config_proposers, config_acceptors):
        self.proposer_id = proposer_id
        self.config_acceptors = config_acceptors
        self.config_proposers = config_proposers
        self.components = None
        self.mcast_receiver = None
        self.mcast_sender = None
        self.c_rnd = 0
    
    def construct(self):
        self.mcast_receiver = mcast_receiver(self.config_proposers)
        self.mcast_sender = mcast_sender
        self.components = Components(self.proposer_id,  self.mcast_sender, self.config_acceptors)    
  
    def run(self):
        while True: 
            msg = self.mcast_receiver.recv(2**16)    
            self.components.process_message(decode_message(msg))            


class Acceptor: 
    def __init__(self, acceptor_id, config_acceptors, config_proposers):
        self.acceptor_id = acceptor_id
        self.config_acceptors = config_acceptors
        self.config_proposers = config_proposers
        self.components = None
        self.mcast_receiver = None
        self.mcast_sender = None
    
    def construct(self): 
        self.mcast_receiver = mcast_receiver(self.config_acceptors)
        self.mcast_sender = mcast_sender()
        self.components = Components(self.acceptor_id, self.mcast_sender, self.config_proposers)
        
    def run(self):
        while True: 
            msg = self.mcast_receiver.recv(2**16)    
            self.components.process_message(decode_message(msg))      
    
    
def mcast_receiver(hostport):
    """create a multicast socket listening to the address"""
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_sock.bind(hostport)

    mcast_group = struct.pack("4sl", socket.inet_aton(hostport[0]), socket.INADDR_ANY)
    recv_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mcast_group)
    return recv_sock


def mcast_sender():
    """create a udp socket"""
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    return send_sock

def decode_message(message): 
    return json.loads( message.decode('utf8'))
    



