import sys
import socket
import struct
import random

rnd = None
v_rnd = None
v_val = None


class Paxos:
    def __init__(self, id_paxos, socket_proposer, acceptors):
        self.c_rnd = None
        self.c_val = None
        self.id = id_paxos
        self.socket_proposer = socket_proposer
        self.acceptors  = acceptors
        self.acceptors_state = []
        self.c_rnd = None
        self.v = None

    def proposer_phase_1A(self, v, id_proposer):
        # increase the c-round to arbitrary unique value 
        self.c_rnd = (id_proposer, random.randint(0,100))
        self.v = v 
        self.socket_proposer.sendto(self.c_rnd, self.acceptors)
        
    # def acceptor(config, id):
    # print ('-> acceptor', id)
    # state = {}
    # r = mcast_receiver(config['acceptors'])
    # s = mcast_sender()
    # while True:
    #     msg = r.recv(2**16)
    #     # fake acceptor! just forwards messages to the learner
    #     if id == 1:
    #         # print "acceptor: sending %s to learners" % (msg)
    #         print(msg)
    #         print("-------")
    #         s.sendto(msg, config['learners'])
    def acceptor_phase_1B(self, ):
        # how can I REV HERE THE MESSAGE
        pass
    
    
    def proposer_phase_2A():
        pass
    
    def acceptor_phase_2B():
        pass
    
    def proposer_phase_3():
        pass
    
    

proposers = [1,2,3]   
messages = ["a", "b", "c"]
id_paxos = 0


# TODO create e class called socket
def mcast_sender():
    """create a udp socket"""
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    return send_sock

acceptors = ("239.0.0.1", 7000)
for v in messages: 

    
    for proposer in proposers:
        socket_proposer = mcast_sender()
        id_paxos = id_paxos + 1
        instance_of_paxos = Paxos(id_paxos, proposer, socket_proposer)
        instance_of_paxos.proposer_phase_1A(v, proposer)
        

    
