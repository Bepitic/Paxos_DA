#!/usr/bin/env python3
import sys
import socket
import struct
import functions as fnc
import json
from paxos_algorithm.algorithm import Components, _decode
from paxos_algorithm.paxos_participant import Acceptor, Proposer, mcast_receiver, mcast_sender
import time
def parse_cfg(cfgpath):
    cfg = {}
    with open(cfgpath, 'r') as cfgfile:
        for line in cfgfile:
            (role, host, port) = line.split()
            cfg[role] = (host, int(port))
    return cfg

# ----------------------------------------------------

def acceptor(config, id):
    print ('-> acceptor', id)
    proposer_obj = Acceptor(id, config['acceptors'], config['proposers'], 2)
    proposer_obj.run()
            
def proposer(config, id):
    print ('-> proposer', id)
    proposer_obj = Proposer(id, config['proposers'], config['acceptors'],config['learners'], 2)
    proposer_obj.run()
    

def learner(config, id):
    r = mcast_receiver(config['learners'])
    s = mcast_sender()

    msg_paxos = {}
    sentinel = 0 # the first paxos id
    while True:
        msg = r.recv(2**16)
        px_id = _decode(msg)["paxos_id"]
        if(px_id not in msg_paxos):
            msg_paxos[px_id] = _decode(msg)["msg"]["v_val"] 

        if(sentinel in msg_paxos):
            for item in msg_paxos[sentinel]:
                #print(int(item)) #TODO check out if the msg is a list or a value anditerate over it
                if type(item) == list:
                    for i in item: 
                        print(int(item))
                else: 
                    print(int(item))
                sys.stdout.flush()
            sentinel +=1
        else: 
            delay = 0.1  # initial delay in seconds
            max_delay = 0.4
            if sentinel not in msg_paxos:
                s.sendto(Components.build_msg(None, "learner", sentinel, None, None), config['proposers'])
                time.sleep(delay)
                delay = min(delay * 2, max_delay)
            

def client(config, id):
    print ('-> client ', id)
    s = mcast_sender()
    for value in sys.stdin:
        value = value.strip()
        print ("client: sending %s to proposers" % (value))
        s.sendto(Components.build_msg(None, "client", None, None, value), config['proposers'])
    print ('client done.')    

if __name__ == '__main__':
        cfgpath = sys.argv[1]
        config = parse_cfg(cfgpath)
        role = sys.argv[2]
        id = int(sys.argv[3])
        if role == 'acceptor':
            rolefunc = acceptor
        elif role == 'proposer':
            rolefunc = proposer
        elif role == 'learner':
            rolefunc = learner
        elif role == 'client':
            rolefunc = client
        rolefunc(config, id)
