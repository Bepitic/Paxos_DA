#!/usr/bin/env python3
import sys
import socket
import struct
import functions as fnc
import json
from paxos_algorithm.algorithm import Components
from paxos_algorithm.paxos_participant import Participant, mcast_receiver, mcast_sender

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
    proposer_obj = Participant(id, config['acceptors'], config['proposers'])
    proposer_obj.run()
            


def proposer(config, id):
    print ('-> proposer', id)
    proposer_obj = Participant(id, config['proposers'], config['acceptors'])
    proposer_obj.run()
        


def learner(config, id):
    r = mcast_receiver(config['learners'])
    while True:
        msg = r.recv(2**16)
        print(msg)
        sys.stdout.flush()


def client(config, id):
    print ('-> client ', id)
    s = mcast_sender()
    for value in sys.stdin:
        value = value.strip()
        print ("client: sending %s to proposers" % (value))
        s.sendto(value.encode(), config['proposers'])
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
