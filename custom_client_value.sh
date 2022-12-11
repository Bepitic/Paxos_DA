#!/usr/bin/env bash
projdir="$1"
conf=`pwd`/paxos.conf
n="$2"

if [[ x$projdir == "x" || x$n == "x" ]]; then
	echo "Usage: $0 <project dir> <number of values per proposer>"
    exit 1
fi

# following line kills processes that have the config file in its cmdline
KILLCMD="pkill -f $conf"

$KILLCMD

cd $projdir

../generate.sh $n > ../prop1
echo "starting acceptors..."
./acceptor.sh 1 $conf &

sleep 1
echo "starting proposers..."

./proposer.sh 1 $conf > ../lear1n &

echo "waiting to start clients"
sleep 1
echo "starting clients..."

./client.sh 1 $conf < ../prop1 &
sleep 10
$KILLCMD
wait

cd ..