from threading import Thread 
from .algorithm import Components
import sys
import socket
import struct
import json

class Participant:
    def __init__(self, participant_id, config_mcast_receiver, config_the_receivers, config_listeners, quorum_value):
        self.participant_id = participant_id
        self.config_the_receivers = config_the_receivers
        self.config_mcast_receiver = config_mcast_receiver
        self.listeners = config_listeners
        self.mcast_receiver = None
        self.mcast_sender = None
        self.c_rnd = None
        self.components = {}
        self.quorum = {}
        self.quorum_value = quorum_value
        
        

    def run(self):
        self.config_mcast_receiver = mcast_receiver(self.config_mcast_receiver)
        self.mcast_sender = mcast_sender()
        self.paxos_id = 0 
        
        while True: 
            msg = self.config_mcast_receiver.recv(2**16)   
            message = decode_message(msg)
            
            if message["origin"] == "client": 
                # Proposers
                print(message)
                self.c_rnd = 1
                
                self.component = Components(self.participant_id,  self.mcast_sender, self.config_the_receivers, self.paxos_id, message["msg"])
                print(message["msg"])    
                self.components[self.paxos_id] =self.component
                self.components[self.paxos_id].proposer_phase_1A(self.c_rnd)  
                self.paxos_id = self.paxos_id + 1
                self.c_rnd = self.c_rnd + 1 

            elif message["origin"] == "proposer": 
                if message["phase"] == "P1A":
                    # print(message)s
                    # Acceptor
                    # this is not an instance of Paxos, acceptors use it just to call the functions. 
                    self.component = Components(self.participant_id,  self.mcast_sender, self.config_the_receivers, message["paxos_id"]) 
                    if message["paxos_id"] not in self.components:    
                        self.components[message["paxos_id"]] = self.component
                    self.components[message["paxos_id"]].acceptor_phase_1B(message["msg"]["c_rnd"])
                    
                elif message["phase"] == "P2A":
                    component = self.components[message["paxos_id"]]
                    component.acceptor_phase_2B(message["msg"]["c_rnd"], message["msg"]["c_val"])
            
            elif message["origin"] == "acceptor":
                    if message["phase"] == "P1B": 
                        # Proposer
                        # Only the correct proposer will respond to acceptors messages.
                            # print(f"proposer_id: {self.participant_id}")
                            # print(message)
                        component = self.components[message["paxos_id"]]
                        # print(message["paxos_id"],message["phase"])
                        # print(self.quorum)
                        
                        if message["paxos_id"] in self.quorum and message["phase"] in self.quorum[message["paxos_id"]]:
                            self.quorum[message["paxos_id"]][message["phase"]].append(message)
                            # print("append_2")
                        else:
                            # print("append_1")
                            self.quorum[message["paxos_id"]] = {message["phase"]: []}
                            self.quorum[message["paxos_id"]][message["phase"]].append(message)
                            # print(self.quorum)
                        if len(self.quorum[message["paxos_id"]][message["phase"]]) >= self.quorum_value:
                            # print("message")
                            # print(self.quorum[message["paxos_id"]][message["phase"]])
                            print("test")
                            self.component.proposer_phase_2A(self.quorum[message["paxos_id"]][message["phase"]])
                            # print("the quorum list: {} and  the length: {} \n".format(self.quorum,len(self.quorum[message["paxos_id"]][message["phase"]])))
                    elif message["phase"] == "P2B":
                        # Proposer
                        # print(message)
                        
                        if self.participant_id == message["proposer_id"]: 
                            component = self.components[message["paxos_id"]]
                            
                            if message["paxos_id"] in self.quorum and message["phase"] in self.quorum[message["paxos_id"]]:
                                self.quorum[message["paxos_id"]][message["phase"]].append(message)
                            else:
                                self.quorum[message["paxos_id"]] = {message["phase"]: []}
                                self.quorum[message["paxos_id"]][message["phase"]].append(message)
                            if len(self.quorum[message["paxos_id"]][message["phase"]]) >= self.quorum_value:
                                self.component.proposer_phase_3(self.quorum[message["paxos_id"]][message["phase"]], self.listeners)
    
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
    



