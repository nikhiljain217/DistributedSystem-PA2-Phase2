# DistributedSystem-PA2-Phase2
Phase 2 implemenation for PA2 of Distributed System

Steps to run the program:
python server.py <port-no>

Things which work: 
1. Verified that queue operations exposed (qCreate, qDestroy, qId, qPop, qPush, qDestroy, qTop, qSize) are working correctly.
2. Verified that state is being replicated correctly
3. Verified that the message order is being followed correctly by all nodes and that the sequencer role is rotating correctly.
4. Verified that the system can handle message omission, server crashes and network partition.

Things which does not work:
1. Bounds and exceptional cases handling on queue operations such as popping from an empty queue and deleting a non existent queue have not been verified thoroughly.
2. The system does not handle Extended Virtual Synchrony.
