from threading import Thread 
from .algorithm import Components
import sys
import socket
import struct
import json
import random
import time

class Participant:
    def __init__(self, participant_id, config_mcast_receiver, config_the_receivers, config_listeners, quorum_value, is_proposer):
        self.participant_id = participant_id
        self.config_the_receivers = config_the_receivers
        self.config_mcast_receiver = config_mcast_receiver
        self.listeners = config_listeners
        self.mcast_receiver = None
        self.mcast_sender = None
        self.components = {}
        self.quorum = {}
        self.quorum_value = quorum_value
        self.is_proposer = is_proposer
        
        self.c_rnd = 10 + self.participant_id

        # Atomic Broadcast
        self.R_Del, self.A_Delivered = [] , []
        self.active_paxos = False
        self.time = 0
        self.delta = 0 
        #self.k = 0 # paxos instance

    def run(self):
        self.mcast_receiver = mcast_receiver(self.config_mcast_receiver)
        self.mcast_sender = mcast_sender()
        self.paxos_id = 0 
        
        while True: 

            if(self.is_proposer == True):
                if(self.active_paxos == True and time.time()- self.time > self.delta):
                    self.active_paxos = False

                #print('if_a')
                if(substract(self.A_Delivered,self.R_Del) and not self.active_paxos and self.is_proposer):
                    #print('a')
                    undel = substract(self.A_Delivered,self.R_Del)[:10] # Duplicate in the while possible to remove

                    self.component = Components(self.participant_id,  self.mcast_sender, self.config_the_receivers, self.paxos_id, undel)
                    #print(f'id{self.participant_id} undel{undel}')    
                    self.components[self.paxos_id] = self.component
                    self.components[self.paxos_id].proposer_phase_1A(self.c_rnd)  
                    self.c_rnd = self.c_rnd + 10
                    self.active_paxos = True
                    self.time = time.time()
                    self.delta = random.randint(2,4)

            msg = self.mcast_receiver.recv(2**29)   
            message = decode_message(msg)
            #print(f'id{self.participant_id} msg{msg}')    


            if message["origin"] == "client": 
                #Proposers Atomic Broadcast
                self.R_Del.append(message["msg"])

                # Proposers
                # print(message)
                # self.c_rnd = 1
                # 
                # self.component = Components(self.participant_id,  self.mcast_sender, self.config_the_receivers, self.paxos_id, message["msg"])
                # print(message["msg"])    
                # self.components[self.paxos_id] = self.component
                # self.components[self.paxos_id].proposer_phase_1A(self.c_rnd)  
                # self.c_rnd = self.c_rnd + 1 

            elif message["origin"] == "proposer": 
                if message["phase"] == "DECISION":
                    print(f'msg decision : {message["msg"]["v_val"]}')
                    decision = [] 
                    if type(message["msg"]['v_val']) is list:
                        for item in message["msg"]['v_val']:
                            #print(item)
                            #print(type(item))
                            self.A_Delivered.append(item)
                            decision.append(item)
                    else:
                        #print(message["msg"]['v_val'])
                        #print(type(message["msg"]['v_val']))
                        self.A_Delivered.append(message["msg"]['v_val'])
                        decision.append(message["msg"]['v_val'])

                    #print('clean')
                    clean_decision = substract(self.A_Delivered, decision)

                    for item in clean_decision:
                        self.A_Delivered.append(item)

                    self.active_paxos = False
                    self.paxos_id += 1 
                    self.c_rnd = 10 + self.participant_id
 
                elif message["phase"] == "P1A":
                    #print(message)
                    #print("p1a")
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
                            #print("test")
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
                                self.component.proposer_phase_3(self.quorum[message["paxos_id"]][message["phase"]], self.listeners,self.config_mcast_receiver)
    
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
    
def substract(A,B):
    # Substract the elements from A(list) of the B(list)
    # B = [1,2,3] // A = [2] // substract(A,B) = [1,3] #
    # Also Removes Duplicates
    #print(f"substract A {A} B {B}")
    C = set(B) - set(A)
    return list(C)
    # or C = [x for x in B if x not in A]

