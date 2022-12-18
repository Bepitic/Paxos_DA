# Distributed Algorithms

Participants
    *Francisco Amoros Cubells 
    *Oscar Arturo Silva Castellanos
    *Shega Likaj

# How to Run

1)Choose the case that you want to run e.g. ./run.sh true-paxos 100 
2)To client data we created an aditional .sh script  which we generate uniquely . For each client we dont have messages with the same value. We are using the value as a key
3)When we stress test for 10,000 , we learn everything that was proposed in total order.
4)To kill acceptors while values are being proposed, we have created  a script ./run_kill.sh which identifies the process id's of the acceptors and kills. At this moment the script kill 2 
acceptors. Please comment this line "../pkill_acceptor.sh 1".
