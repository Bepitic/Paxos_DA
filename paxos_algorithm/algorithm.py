import sys
import socket
import struct
import random
import json

class Components:
    def __init__(self, proposer_id, mcast_sender, receivers):
        pass
    def proposer_phase_1A(self, v, id_proposer, first_part_of_c_rnd):
        # # increase the c-round to arbitrary unique value 
        # #(id_proposer, random.randint(0,100))
        # self.c_rnd  = (first_part_of_c_rnd, id_proposer)
        # self.v = v 
        # msg= json.dumps({"c_rnd": self.c_rnd, "id_paxos": self.id_paxos, "id_proposer": id_proposer, "origine": "proposer", "phase": "PHASE 1A"}).encode('utf8')
        # self.socket_proposer.sendto(msg, self.receivers)
        pass
    
    def acceptor_phase_1B(self, c_rnd, s, id_proposer):
        # if c_rnd(0)> self.rnd:
        #     rnd = c_rnd
        #     msg= json.dumps({"rnd": self.rnd, "id_proposer": id_proposer, "origine": "acceptor", "phase": "PHASE 1B"}).encode('utf8')
        #     s.sentto(self.receivers)
    
        pass

    
    def proposer_phase_2A():
        pass
    
    def acceptor_phase_2B():
        pass
    
    def proposer_phase_3():
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


    
