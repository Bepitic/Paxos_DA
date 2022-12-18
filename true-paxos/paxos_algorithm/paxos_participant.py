from threading import Thread 
from .algorithm import Components
import sys
import socket
import struct
import json
import random
import time

class Proposer: 
    def __init__(self, proposer_id , config_mcast_receiver, config_the_receivers, config_listeners, quorum_value):
        self.proposer_id = proposer_id
        self.config_the_receivers = config_the_receivers
        self.config_mcast_receiver = config_mcast_receiver
        self.listeners = config_listeners
        self.mcast_receiver = None
        self.mcast_sender = None
        self.components = {}
        self.quorum = {}
        # test with quorum 3 and everthing will work 
        self.quorum_value = quorum_value
        self.c_rnd = 1+ float("0."+str(self.proposer_id))
        self.R_Del, self.A_Delivered = [] , []
        self.active_paxos = False
        self.time = 0
        self.delta = 0 
        
    def run(self):
        self.mcast_receiver = mcast_receiver(self.config_mcast_receiver)
        self.mcast_sender = mcast_sender()
        self.paxos_id = 0

        while True: 
            if(self.active_paxos == True and time.time()- self.time > self.delta):
                self.active_paxos=False
                self.c_rnd = self.c_rnd + 1
                self.paxos_id = self.paxos_id -1

            if self.active_paxos==False:
                if substract(self.A_Delivered,self.R_Del):
                    undelivered = substract(self.A_Delivered,self.R_Del)[:10]

                    print(f' UNDELIVERED :{undelivered}, adel{self.A_Delivered}, R_del:{self.R_Del}')
                    component = Components(self.proposer_id,  self.mcast_sender, self.config_the_receivers, self.paxos_id, undelivered, self.c_rnd, self.quorum_value)
                    self.components[self.paxos_id] = component
                    self.components[self.paxos_id].proposer_phase_1A(self.c_rnd)  
                    self.active_paxos = True
                    self.time = time.time()
                    self.delta = random.randint(10,20)
                    self.paxos_id = self.paxos_id +1

            msg = self.mcast_receiver.recv(2**29)   
            message = decode_message(msg)
            if message["origin"] == "client": 
                print(message)
                self.R_Del.append(message["msg"])
                
            elif message["origin"] == "proposer": 
                if message["phase"] == "DECISION":
                    if message["participant_id"] == self.proposer_id:
                        if message["paxos_id"] in self.components :                             
                            decision = [] 
                            if type(message["msg"]['v_val']) is list:
                                for item in message["msg"]['v_val']:
                                    decision.append(item)
                            else:
                                decision.append(message["msg"]['v_val'])
                            
                            clean_decision = substract(self.A_Delivered, decision)
                            if(clean_decision):
                                self.active_paxos = False
                            self.A_Delivered = self.A_Delivered + clean_decision
                            print(f'pax_part:{message}')

                            #self.c_rnd = message["msg"]["c_rnd"]
                            self.c_rnd = 1+ float("0."+str(self.proposer_id))
                            
            elif message["origin"] == "acceptor":
                    if message["phase"] == "P1B":  
                        if message["msg"]["proposer_id"] == self.proposer_id: 
                            if message["paxos_id"] in self.components: 
                                component = self.components[message["paxos_id"]]
                                if message["paxos_id"] in self.quorum and message["phase"] in self.quorum[message["paxos_id"]]:
                                    self.quorum[message["paxos_id"]][message["phase"]].append(message)
                                else:
                                    self.quorum[message["paxos_id"]] = {message["phase"]: []}
                                    self.quorum[message["paxos_id"]][message["phase"]].append(message)
                                if len(self.quorum[message["paxos_id"]][message["phase"]]) >= self.quorum_value:
                                    component.proposer_phase_2A(self.quorum[message["paxos_id"]][message["phase"]])
                                    
                    elif message["phase"] == "P2B":
                        if message["msg"]["proposer_id"] == self.proposer_id: 
                            if message["paxos_id"] in self.components:
                                component = self.components[message["paxos_id"]]
                                if message["paxos_id"] in self.quorum and message["phase"] in self.quorum[message["paxos_id"]]:
                                    self.quorum[message["paxos_id"]][message["phase"]].append(message)
                                else:
                                    self.quorum[message["paxos_id"]] = {message["phase"]: []}
                                    self.quorum[message["paxos_id"]][message["phase"]].append(message)
                                if len(self.quorum[message["paxos_id"]][message["phase"]]) >= self.quorum_value:
                                    component.proposer_phase_3(self.quorum[message["paxos_id"]][message["phase"]], self.listeners,self.config_mcast_receiver)
                                    
class Acceptor:
    def __init__(self, acceptor_id, config_mcast_receiver, config_the_receivers, quorum_value):
        self.acceptor_id = acceptor_id
        self.config_the_receivers = config_the_receivers
        self.config_mcast_receiver = config_mcast_receiver
        self.mcast_receiver = None
        self.mcast_sender = None
        self.components = {}
        self.quorum_value = quorum_value
    def run(self):
        self.mcast_receiver = mcast_receiver(self.config_mcast_receiver)
        self.mcast_sender = mcast_sender()
        while True: 
            msg = self.mcast_receiver.recv(2**29)   
            message = decode_message(msg)
            if message["phase"] == "P1A":
                component = Components(self.acceptor_id,  self.mcast_sender, self.config_the_receivers, message["paxos_id"], self.quorum_value) 
                if message["paxos_id"] not in self.components:    
                    self.components[message["paxos_id"]] = component
                self.components[message["paxos_id"]].acceptor_phase_1B(message["msg"]["c_rnd"], message["participant_id"])
            if message["phase"] == "P2A":
                if message["paxos_id"] in self.components : 
                    component = self.components[message["paxos_id"]]
                    component.acceptor_phase_2B(message["msg"]["c_rnd"], message["msg"]["c_val"],message["participant_id"])
                    
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