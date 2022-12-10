from threading import Thread 
from algorithm import Components
import sys
import socket
import struct
import json

class Proposer:
    def __init__(self, proposer_id):
        self.proposer_id = proposer_id
        self.acceptors = None
        self.components = None
        self.mcast_receiver = None
        self.mcast_sender = None
        
    
    def construct_proposer(self, acceptors, hostport):
        self.acceptors = acceptors
        self.components = Components(self.proposer_id, self.socker_proposer, self.acceptors)    
        self.mcast_receiver = mcast_receiver(hostport)
        self.mcast_sender = mcast_receiver()

class Acceptor: 
    def __init__(self, acceptor_id):
        self.acceptor_id = acceptor_id
        self.socker_proposer = None
        self.proposers = None
        self.mcast_receiver = None
        self.mcast_sender = None
        
    
    def construct_acceptor(self, proposers, hostport): 
        self.proposers = proposers
        self.components = Components(self.acceptor_id, self.socker_proposer, self.proposers)
        self.mcast_receiver = mcast_receiver(hostport)
        self.mcast_sender = mcast_receiver()
    
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