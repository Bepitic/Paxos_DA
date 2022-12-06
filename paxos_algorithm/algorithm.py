import sys
import socket
import struct


rnd = None
v_rnd = None
v_val = None


class Paxos:
    def __init__(self, id_paxos, proposer):
        self.c_rnd = None
        self.c_val = None
        self.id = id_paxos
        self.proposer = proposer

    def proposer_phase_1A(self, v):
        #
        pass
    
    
    def acceptor_phase_1B(self,round):

        if self.c_rnd > round:
            round = self.c_rnd
            return {"phase": "PHASE_1B", "rnd": rnd, "v-rnd": v_rnd, "v-val": v_val}
        else:
            return
        
    
    
    def proposer_phase_2A():
        pass
    
    def acceptor_phase_2B():
        pass
    
    def proposer_phase_3():
        pass
