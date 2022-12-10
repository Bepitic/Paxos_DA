from threading import Thread 
from algorithm import Components
import sys
import socket
import struct
import json

class Proposer:
    def __init__(self, proposer_id, config_acceptors, config_proposers):
        self.proposer_id = proposer_id
        self.config_acceptors = config_acceptors
        self.config_proposers = config_proposers
        self.components = None
        self.mcast_receiver = None
        self.mcast_sender = None
        self.c_rnd = 0
    
    def construct_proposer(self):
        self.mcast_receiver = mcast_receiver(self.config_proposers)
        self.mcast_sender = mcast_sender
        self.components = Components(self.proposer_id,  self.mcast_sender, self.config_acceptors)    
  
    def run(self):
        while True: 
            msg = self.mcast_receiver.recv(2**16)    
            self.components.process_message(decode_message(msg))        
            # self.components.process_message(decode_message(msg))
            
            
            # if msg["origin"] == "client": 
            #     # TODO this is not the final version of the parameters. 
            #     self.components.proposer_phase_1A(msg["content"], self.proposer_id, self.c_rnd)
                
            # elif msg["orgin"] == "acceptor": 
            #     if msg["phase"]
                
                
            
#   """
#   message = {"origin" : "", "phase": "", "content": "write the message here"}
#   """          


class Acceptor: 
    def __init__(self, acceptor_id, acceptors, proposers):
        self.acceptor_id = acceptor_id
        self.config_acceptors = acceptors
        self.config_proposers = proposers
        self.components = None
        self.mcast_receiver = None
        self.mcast_sender = None
    
    def construct_acceptor(self, proposers, hostport): 
        self.proposers = proposers
        self.mcast_receiver = mcast_receiver(hostport)
        self.mcast_sender = mcast_sender()
        self.components = Components(self.acceptor_id, self.mcast_sender, self.proposers)
  
 
    
    
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
    



