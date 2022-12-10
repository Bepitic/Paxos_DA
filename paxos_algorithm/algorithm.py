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
    def __init__(self, proposer_id, mcast_sender, receivers):
        self.id = proposer_id
        self.send = mcast_sender
        self.receivers = receivers
        self.rnd = -1
        self.c_rnd = None
        self.c_val = None
        self.v_val = None
        self.v_rnd = 0
        self.instance_paxos = None
        self.value = None

        self.k = -1
        self.v = None

    @staticmethod(function)
    def build_msg(phase,origin,Px_instance,id_proposer,msg):
        jsn =  {"Phase":phase,"Origin":origin, "Paxos_Inst":Px_instance,"Proposer_id":id_proposer, "Msg":msg}
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
        if (c_rnd> self.rnd):
            self.rnd = c_rnd
            msg = Components.build_msg("P1B", "acceptor", self.instance_paxos, self.id, {"rnd":self.rnd, "v_rnd":self.v_rnd,"v_val":self.v_val })
            self.send(msg, self.receivers)
        # if c_rnd(0)> self.rnd:
        #     rnd = c_rnd
        #     msg= json.dumps({"rnd": self.rnd, "id_proposer": id_proposer, "origine": "acceptor", "phase": "PHASE 1B"}).encode('utf8')
        #     s.sentto(self.receivers)
    
    def proposer_phase_2A(self, rnd, v_rnd, v_val):
        if (self.c_rnd == rnd):
            if(self.k < v_rnd):
                self.k = v_rnd
                self.v = v_val
            if (self.k == 0):
                self.c_val = self.value
            else:
                self.c_val = self.v
            msg = Components.build_msg("P2A", "proposer", self.instance_paxos, self.id, {"c_rnd":self.c_rnd,"c_val":self.c_val })
            self.send(msg, self.receivers)




    
    def acceptor_phase_2B(self, c_rnd,c_val):
        if(c_rnd >= self.rnd):
            self.v_rnd = c_rnd
            self.v_val = c_val
            msg = Components.build_msg("P2B", "acceptor", self.instance_paxos, self.id, {"v_rnd":self.v_rnd,"v_val":self.v_val })
            self.send(msg, self.receivers)

    
    def proposer_phase_3():
        #???????
        pass
    
    

    def process_message(self, message):
        if message["origin"] == "client": 
        # TODO this is not the final version of the parameters. Check again.  
            self.proposer_phase_1A()
            pass
        elif message["origin"] == "proposer": 
            if message["phase"] == "PHASE 1A":
                self.acceptor_phase_1B()
                
            elif message["phase"] == "PHASE 2A":
                self.acceptor_phase_2B()
        
        elif message["origin"] == "acceptor": 
                if message["phase"] == "PHASE 1B": 
                    self.proposer_phase_2A()
                elif message["phase"] == "PHASE 2B":
                    self.proposer_phase_3()


    
