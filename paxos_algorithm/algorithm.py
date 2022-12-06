

rnd = None
v_rnd = None
v_val = None


class Paxos:
    def __init__(self, id_paxos, proposer):
        self.c_rnd = None
        self.c_val = None
        self.id = id_paxos
        self.proposer = proposer

    def propose(self, v, ):
        
        