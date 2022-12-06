from time import time
from paxos import mcast_receiver

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
