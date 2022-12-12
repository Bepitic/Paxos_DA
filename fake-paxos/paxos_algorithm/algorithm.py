import sys
import socket
import struct
import random
import json

def _decode(msg):
    return json.loads(msg.decode())
def _encode(jsn):
    return json.dumps(jsn).encode('utf8')

class Components:
    def __init__(self, participant_id, mcast_sender, receivers, instance_paxos, value=None):
        self.id = participant_id
        self.send = mcast_sender.sendto
        self.receivers = receivers
        self.rnd = 0
        self.c_rnd = None
        self.c_val = None
        self.v_val = None
        self.v_rnd = 0
        self.instance_paxos = instance_paxos
        self.value = value

        self.k = -1
        self.v = None

    @staticmethod
    def build_msg(phase,origin,Px_instance,id_proposer,msg):
        jsn =  {"phase":phase,"origin":origin, "paxos_id":Px_instance,"proposer_id":id_proposer, "msg":msg}
        return _encode(jsn=jsn)


    def proposer_phase_1A(self, c_rnd):
        self.c_rnd = c_rnd
        msg = Components.build_msg("P1A", "proposer", self.instance_paxos, self.id, {"c_rnd":c_rnd})
        self.send(msg, self.receivers)

        # # increase the c-round to arbitrary unique value 
        # #(id_proposer, random.randint(0,100))
        # self.c_rnd  = (first_part_of_c_rnd, id_proposer)
        # self.v = v 
        # msg= json.dumps({"c_rnd": self.c_rnd, "id_paxos": self.id_paxos, "id_proposer": id_proposer, "origine": "proposer", "phase": "PHASE 1A"}).encode('utf8')
        # self.socket_proposer.sendto(msg, self.receivers)
    
    def acceptor_phase_1B(self, c_rnd):
        # print(f"acceptor: {self.id} c_rnd: {c_rnd} rnd: {self.rnd}")
        # until here is correct
        
        if (c_rnd> self.rnd):
            # print(f"c_rnd {c_rnd}")
            self.rnd = c_rnd
            # print( self.receivers)
            msg = Components.build_msg("P1B", "acceptor", self.instance_paxos, self.id, {"rnd":self.rnd, "v_rnd":self.v_rnd,"v_val":self.v_val })
            print(msg)

            self.send(msg, self.receivers)
        # if c_rnd(0)> self.rnd:
        #     rnd = c_rnd
        #     msg= json.dumps({"rnd": self.rnd, "id_proposer": id_proposer, "origine": "acceptor", "phase": "PHASE 1B"}).encode('utf8')
        #     s.sentto(self.receivers)
    
    def proposer_phase_2A(self,list_msg):# rnd, v_rnd, v_val):
        #FIXME: the number of the quorum should be a global value or a parameter to pass
        num_Q = 2 # Minimum size of the Quorum number
        sentinel = 0
        print("1")
        for message in list_msg:
            message['msg']['rnd']
            rnd = message['msg']['rnd']

            if (self.c_rnd == rnd):
                sentinel += 1

        k = -1
        v = None
        for message in list_msg:
            rnd =message['msg']['rnd']
            v_rnd = message['msg']['v_rnd']
            v_val =message['msg']['v_val']
            if(sentinel >= num_Q): #We have a quorum
                if (self.c_rnd == rnd):# We are in the Quorum group
                    if(k < v_rnd):
                        k = v_rnd
                        v = v_val
                    if (k == 0):
                        self.c_val = self.value
                    else:
                        self.c_val = v
                    print(self.c_val)
        if(sentinel >= num_Q): #We have a quorum
            
            msg = Components.build_msg("P2A", "proposer", self.instance_paxos, self.id, {"c_rnd":self.c_rnd,"c_val":self.c_val })
            print(msg)

            self.send(msg, self.receivers)
    
    def acceptor_phase_2B(self, c_rnd,c_val):
        if(c_rnd >= self.rnd):
            self.v_rnd = c_rnd
            self.v_val = c_val
            print(self.v_val)
            msg = Components.build_msg("P2B", "acceptor", self.instance_paxos, self.id, {"v_rnd":self.v_rnd,"v_val":self.v_val })
            print(msg)
            self.send(msg, self.receivers)

    def proposer_phase_3(self, list_msg, listeners):
        #FIXME: the number of the quorum should be a global value or a parameter to pass
        num_Q = 2 # Minimum size of the Quorum number
        sentinel = 0
        for message in list_msg:
            v_rnd = message['msg']['v_rnd']
            self.v_val =  message['msg']['v_val']
            if (v_rnd == self.c_rnd):
                sentinel += 1
        # print(f"{self.v_val}vval")
        if(sentinel >= num_Q): #We have a quorum
            msg = Components.build_msg("DECISION", "proposer", self.instance_paxos, self.id, {"v_val":self.v_val})
            print(msg)
            self.send(msg, listeners) 