#!/usr/bin/env python3
import sys
import socket
import struct
import functions as fnc
import json
from paxos_algorithm.algorithm import Paxos

def mcast_receiver(hostport): # TODO : Check if this function is Bloking or not!
    """create a multicast socket listening to the address"""
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_sock.bind(hostport)

    mcast_group = struct.pack("4sl", socket.inet_aton(hostport[0]), socket.INADDR_ANY)
    recv_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mcast_group)
    return recv_sock


def mcast_sender():
    """create a udp socket"""
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    return send_sock


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
    state = {}
    r = mcast_receiver(config['acceptors'])
    s = mcast_sender()
    id_paxos = 0
    instances_of_paxos= {}
    while True:
        msg = r.recv(2**16)
        
        if msg.origine == "proposer": 
            if msg.phase == "PHASE 1A":
                id_paxos = id_paxos + 1
                # TODO this should removed. 
                instance_of_paxo= Paxos(id_paxos, s, config['proposer'])
                instances_of_paxos.update({id_paxos: instance_of_paxo})
                instances_of_paxos.acceptor_phase_1B(msg.c_rnd, msg.id_proposer)
                # instance_of_paxos = instances_of_paxos[msg.id_paxos]
                
        # m = json.loads(msg.decode())
        # #m = json.load(msg).decode()
        # print(m)
        # print(type(m))
        # print(m['id_paxos'])
        # # fake acceptor! just forwards messages to the learner
        # if id == 1:
        #     # print "acceptor: sending %s to learners" % (msg)
        #     s.sendto(msg, config['learners'])



def proposer(config, id):
    print ('-> proposer', id)
    r = mcast_receiver(config['proposers'])
    s = mcast_sender()
    id_paxos = 0
    first_part_of_c_rnd = 0
    instances_of_paxos= {}
    while True:
        
        
        
        msg = r.recv(2**16)
        
        
        if msg.origine == "client": 
            first_part_of_c_rnd = first_part_of_c_rnd + 1
            id_paxos = id_paxos + 1
            instance_of_paxo = Paxos(id_paxos, s, config['acceptors'])
            instance_of_paxo.proposer_phase_1A(msg.content, id, first_part_of_c_rnd)
            instances_of_paxos.update({id_paxos: instance_of_paxo})
        elif msg.origine == "acceptor": 
            if msg.phase == "PHASE 1B":
               instance_of_paxos = instances_of_paxos[msg.id_paxos]
               instance_of_paxos.proposer_phase_2A()
            elif msg.phase == "PHASE 2B":
                instance_of_paxos = instances_of_paxos[msg.id_paxos]
                instance_of_paxos.proposer_phase_3()
                
              
        # fake proposer! just forwards message to the acceptor
        # if id == 1:
        #     # print "proposer: sending %s to acceptors" % (msg)
        #     m =  json.dumps({"c_rnd": (2,2), "id_paxos": 1}).encode('utf8')
        #     s.sendto(m, config['acceptors'])
        
            
        


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
