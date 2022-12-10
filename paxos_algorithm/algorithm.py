import sys
import socket
import struct
import random
import json
rnd = None
v_rnd = None
v_val = None


class Components:
    def __init__(self):
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
    
    

# proposers = [1,2,3]   
# messages = ["a", "b", "c"]
# id_paxos = 0


# # TODO create e class called socket
# def mcast_sender():
#     """create a udp socket"""
#     send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#     return send_sock

# acceptors = ("239.0.0.1", 7000)
# for v in messages: 

    
#     for proposer in proposers:
#         socket_proposer = mcast_sender()
#         id_paxos = id_paxos + 1
#         instance_of_paxos = Paxos(id_paxos, proposer, socket_proposer)
#         instance_of_paxos.proposer_phase_1A(v, proposer)
        

    
