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
    def __init__(self, participant_id, mcast_sender, receivers, instance_paxos, value=None, c_rnd=None, quorum_value=2):
        self.id = participant_id
        self.send = mcast_sender.sendto
        self.receivers = receivers
        self.rnd = 0
        self.c_rnd = c_rnd
        self.c_val = None
        self.v_val = None
        self.v_rnd = 0
        self.instance_paxos = instance_paxos
        self.value = value
        self.quorum_value = quorum_value
        self.k = -1
        self.v = None

    @staticmethod
    def build_msg(phase,origin,Px_instance,id_proposer,msg):
        jsn =  {"phase":phase,"origin":origin, "paxos_id":Px_instance,"participant_id":id_proposer, "msg":msg}
        return _encode(jsn=jsn)


    def proposer_phase_1A(self, c_rnd):
        msg = Components.build_msg("P1A", "proposer", self.instance_paxos, self.id, {"c_rnd":c_rnd})
        # print(msg)
        self.send(msg, self.receivers)
    
    def acceptor_phase_1B(self, c_rnd, proposer_id):
        if (c_rnd> self.rnd):
            self.rnd = c_rnd
            msg = Components.build_msg("P1B", "acceptor", self.instance_paxos, self.id, {"rnd":self.rnd, "v_rnd":self.v_rnd,"v_val":self.v_val,"proposer_id":proposer_id})
            # print(msg)
            self.send(msg, self.receivers)

    
    def proposer_phase_2A(self, list_from_quorum):
        sentinel = 0
        for message in list_from_quorum:
            message['msg']['rnd']
            rnd = message['msg']['rnd']

            if (self.c_rnd == rnd):
                sentinel += 1

        ## shega
        if (sentinel >= self.quorum_value):
            k=0
            list_v=[]
            for promise in list_from_quorum:
                if promise['msg']['v_rnd'] > k :
                    k = promise['msg']['v_rnd']

            for promise in list_from_quorum:
                if promise['msg']['v_rnd'] == k :
                    list_v.append((promise['msg']['v_rnd'] ,promise['msg']['v_val'] ))
            if k == 0:
                self.c_val = self.value
            else:
                # print(list_v)
                self.c_val = list_v[0][1]
                
        if (sentinel >= self.quorum_value):
            
            msg = Components.build_msg("P2A", "proposer", self.instance_paxos, self.id, {"c_rnd":self.c_rnd,"c_val":self.c_val})
            # print(msg)
            self.send(msg, self.receivers)
            
    def acceptor_phase_2B(self, c_rnd, c_val, proposer_id):
        if(c_rnd >= self.rnd):
            self.v_rnd = c_rnd
            self.v_val = c_val
            msg = Components.build_msg("P2B", "acceptor", self.instance_paxos, self.id, {"v_rnd":self.v_rnd,"v_val":self.v_val , "proposer_id":proposer_id})
            # print(msg)
            self.send(msg, self.receivers)

    def proposer_phase_3(self, list_from_quorum, listeners,proposers, retry=False):
        # Paco  
        #if not retry:
            sentinel = 0
            for message in list_from_quorum:
                v_rnd = message['msg']['v_rnd']
                if (v_rnd == self.c_rnd):
                    sentinel += 1
                    self.v_val =  message['msg']['v_val']

            if (sentinel >= self.quorum_value):
                
                msg = Components.build_msg("DECISION", "proposer", self.instance_paxos, self.id, {"v_val":self.v_val, "c_rnd": self.c_rnd})
                #print(msg)
                self.send(msg, listeners)
                self.send(msg, proposers)
        #else:
        #    msg = Components.build_msg("DECISION", "proposer", self.instance_paxos, self.id, {"v_val":self.v_val, "c_rnd": self.c_rnd})
        #    #print(msg)
        #    self.send(msg, listeners) 
        #    self.send(msg, proposers)  
            
