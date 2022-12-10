from threading import Thread 
from algorithm import Components
import sys
import socket
import struct
import json

class Participant:
    def __init__(self, particpiant_id, config_mcast_receiver, config_the_receivers):
        self.particpiant_id = particpiant_id
        self.config_the_receivers = config_the_receivers
        self.config_mcast_receiver = config_mcast_receiver
        self.components = None
        self.mcast_receiver = None
        self.mcast_sender = None
        self.c_rnd = 0
    
    def construct(self):
        self.config_mcast_receiver = mcast_receiver(self.config_mcast_receiver)
        self.mcast_sender = mcast_sender
        self.components = Components(self.particpiant_id,  self.mcast_sender, self.config_the_receivers)    
  
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
    



