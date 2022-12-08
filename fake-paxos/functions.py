from time import time
from paxos import mcast_receiver
import json 

def _decode(msg):
    return json.loads(msg.decode())
def _encode(jsn):
    return json.dumps(jsn).encode('utf8')

def gather_msg(t,config,id):
    be4 = time()
    r = mcast_receiver(config['acceptors']) # is this blocking or not?
    msg_list = []
    max_size_list = 5
    # if there have not passed t seconds and the len of the list is less than max_size 
    # appending msg received
    while (not((time() - be4)>(t)))and(len(msg_list) < max_size_list ):
        msg = r.recv(2**16)# how much is the size of the msg
        msg_list.append(msg)
    return msg_list

class AtomicBroadcast():
    def __init__(self, config, id, num_processor=0):
        self.R_Del, self.A_Del = [] , []
        self.k = 0 # paxos instance
        self.config = config
        self.id = id
        self.num_processor = num_processor # the max number of processors in the system

    @staticmethod
    def substract(A,B):
        # Substract the elements from A(list) of the B(list)
        # B = [1,2,3] // A = [2] // substract(A,B) = [1,3] #
        # Also Removes Duplicates
        C = set(B) - set(A)
        return list(C)
        # or C = [x for x in B if x not in A]


    def run(self):
        while (True): # Maybe put a signal to make it  stop in some moments?
            # Gather msg
            msg_gathered = gather_msg(2,self.config,self.id)
            self.R_Del.append(msg_gathered)
            while(self.substract(self.A_Del,msg_gathered)):
                self.k += 1
                undel = self.substract(self.A_Del,msg_gathered) # Duplicate in the while possible to remove
                decision = [] # = paxos_manager(k,undel)
                # wait paxos recieve msg
                # if not send again?
                clean_decision = self.substract(self.A_Del, decision)
                self.A_Del.append(clean_decision)
