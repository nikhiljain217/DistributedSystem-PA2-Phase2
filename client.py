import socket
import sys
from datetime import datetime, timedelta
import time
import csv
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = 'qpush'
send_time=[]
rec_time=[]
server_time=[]


def addQueue(label,port):
    server_address = ('localhost', port)
    message="qCreate "+label
    send(message,server_address)
    test()

def pushNumber(qid,item,port):
    server_address =('localhost', port)
    message = "qPush "+str(qid)+" "+str(item)
    send(message,server_address)

def getTop(qid,port):
    server_address =('localhost', port)
    message = "qTop "+str(qid)
    send(message,server_address)
    test()

def removeNumber(qid,port):
    server_address =('localhost', port)
    message = "qPop "+str(qid)
    send(message,server_address)
    test()

def getQid(label,port):
    server_address =('localhost', port)
    message = "qId "+str(qid)
    send(message,server_address)
    test()  

def test():
    global sock
    data, server = sock.recvfrom(4096)
    print(data,server)


def send(message, server_address):
    global sock
    sent = sock.sendto(message.encode("utf-8"), server_address)

try:
    addQueue('first',10000)
    addQueue('first',10002)
    pushNumber(1,1,10001)
    pushNumber(1,2,10000)
    getTop(1,10002)
    removeNumber(1,10000)



    test()
finally:
    print(sys.stderr, 'closing socket')
    sock.close()
