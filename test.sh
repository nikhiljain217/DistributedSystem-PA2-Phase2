#!/bin/bash
echo "qCreate first" > /dev/udp/172.0.0.1/10000
sleep 2
i=0
while [ $i -le 10 ]
do
	echo "qPush 1 $i"> /dev/udp/127.0.0.1/10000
	i=`expr $i + 1`
done

