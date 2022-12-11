from threading import Thread 
from algorithm import Components
import sys
import socket
import struct
import json

class Participant:
    def __init__(self, participant_id, config_mcast_receiver, config_the_receivers, quorum_value):
        self.participant_id = participant_id
        self.config_the_receivers = config_the_receivers
        self.config_mcast_receiver = config_mcast_receiver
        self.components = None
        self.mcast_receiver = None
        self.mcast_sender = None
        self.c_rnd = None
        self.components_list = []
        self.quorum = {}
        self.quorum_value = quorum_value
        
    def run(self):
        self.config_mcast_receiver = mcast_receiver(self.config_mcast_receiver)
        self.mcast_sender = mcast_sender()
        
        while True: 
            msg = self.mcast_receiver.recv(2**16)   
            message = decode_message(msg)
            
            
            if message["origin"] == "client": 
                self.c_rnd = 0 
                self.component = Components(self.participant_id,  self.mcast_sender, self.config_the_receivers)    
                self.components_list.append({self.components.paxos_id,  self.components})
                self.component.proposer_phase_1A(self.c_rnd, self.participant_id)   
                
            elif message["origin"] == "proposer": 
                if message["phase"] == "PHASE 1A":
                    # Acceptor
                    # this is not an instance of Paxos, acceptors use it just to call the functions. 
                    self.component = Components(self.participant_id,  self.mcast_sender, self.config_the_receivers)    
                    self.components_list.append({message[paxos_id],  self.components})
                    
                    self.component.acceptor_phase_1B()
                    
                elif message["phase"] == "PHASE 2A":
                    component = self.components_list[message["paxos_id"]]
                    component.acceptor_phase_2B(message["c-rnd"], message["c-val"])
            
            elif message["origin"] == "acceptor": 
                    if message["phase"] == "PHASE 1B": 
                        # Proposer
                        # Only the correct proposer will respond to acceptors messages.
                        if self.participant_id == message["proposer_id"]: 
                            component = self.components_list[message["paxos_id"]]
                            component.proposer_phase_2A(component.c_rnd, message)
                     
                    elif message["phase"] == "PHASE 2B":
                        
                        self.quorum[message["paxos_id"]].append(message)
                        if len(self.quorum[message["paxos_id"]]) > self.quorum_value:
                            self.proposer_phase_3( self.quorum[message["paxos_id"]])
    
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
    



