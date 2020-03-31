import socket
from FTQueue import FTQueue
import sys
from datetime import datetime
import pytz
import time
import struct
import uuid
import json

server_port=int(sys.argv[1])
# Bind the socket to the port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address =('localhost',server_port)
sent_sock_address=list()
total_server = int(sys.argv[2])
port_number=list()
for i in range(total_server+1):
    port_number.append(10000+i)
print(port_number)
seq_no =0
server_number = server_port%10000
port_number.remove(server_port)
for port in port_number:
    sent_sock_address.append(('localhost',port))
Localbuffer=dict()
ftQueue =dict()
label=dict()
sock.bind(server_address)
RecBuffer=dict()
sendBuffer=dict()

def isLeader():
    global seq_no
    global server_number
    
    return seq_no%3==server_number

def sendNack(seqNo):
    nMessage = {"NACK":seqNo}
    sendMessageToAll(str(nMessage))


def LeaderOperation(message):
    global seq_no
    print("Server Number %s the leader now" % str(server_number))
    message["seq"]=seq_no
    data = applyOperation(message['message'])
    seq_no+=1
    sendMessageToAll(str(message))
    addToSendBuffer(message)
    postOperationWithSeq(message,data)

def addToSendBuffer(message):
    global sendBuffer
    sendBuffer[message["seq"]] = message


def sendMessageToAll(message):
    global sent_sock_address
    global sendBuffer
    for address in sent_sock_address:
        sock.sendto(message.encode("utf-8"),address)




def postOperationWithSeq(message,data):
    if message["uuid"] in RecBuffer.keys():    
        del RecBuffer[message['uuid']]
    if message["uuid"] in Localbuffer and data!=None:
        sock.sendto(str(data).encode("utf-8"), Localbuffer[message["uuid"]])
        del Localbuffer[message["uuid"]]

def isNACK(message):
    return message.find('NACK')!=-1

def printQueue(qid):
    global ftQueue
    ftQueue[qid].qPrint()

def applyOperation(message):
    global ftQueue
    global label
    client_message=message.split()
    qid=0   
    if client_message[0] == 'qCreate':
            label_message = client_message[1]
            if label_message in label.keys():
                return label[label_message]
            ftQueue[len(ftQueue)+1] = FTQueue(len(ftQueue)+1)
            label[label_message] = len(ftQueue)
            qid=label[label_message]
            printQueue(qid)
            return label[label_message]
    elif client_message[0] == 'qDestroy':
            qid = int(client_message[1])
            del label[getValue(label,qid)]
            del ftQueue[qid]

    elif client_message[0] == 'qId':
            qid = int(client_message[1])
            printQueue(qid)
            return getValue(label,qID)
    elif client_message[0] == 'qPush':
            qid = int(client_message[1])
            item = int(client_message[2])
            ftQueue[qid].qPush(item)
            printQueue(qid)
    elif client_message[0] == 'qPop':
            qid = int(client_message[1])
            printQueue(qid)
            return ftQueue[qid].qPop()
    elif client_message[0] == 'qTop':
            qid = int(client_message[1])
            printQueue(qid)
            return ftQueue[qid].qTop()
    elif client_message[0] == 'qSize':
            qid = int(client_message[1])
            printQueue(qid)
            return ftQueue[qid].qId()
    else:
        return "Invalid Operation"



            
def getValue(d, val):
    for key, value in d.items():
        if val == value:
            return key


def expectedSeqNo(seqNo):
    global seq_no
    return seq_no==seqNo

def isMessageFromClient(message):
    return message.find("uuid")==-1

def isMessageFromServerWihoutSeq(message):
    return message.find("seq")==-1

def addUuidToMessage(message,address):
    global ftQueue
    global Localbuffer
    
    message_from_server =dict()
    message_from_server["uuid"]=str(uuid.uuid1())
    message_from_server["message"]=message
    Localbuffer[message_from_server["uuid"]]=address
    return message_from_server



while True:
        #print >>sys.stderr, '\nwaiting to receive message'
        data, address = sock.recvfrom(4096)
        
        data=data.decode()
        if(isMessageFromClient(data)):
            messageToServer = addUuidToMessage(data,address)
            print("Message after adding uud %s" %str(messageToServer))
            if isLeader():
                LeaderOperation(messageToServer)
            else:
                sendMessageToAll(str(messageToServer))
        elif(isMessageFromServerWihoutSeq(data)):
            messageFromServer = eval(data)
            print("Message from other server without seq %s" %str(messageFromServer))
            if isLeader():
                LeaderOperation(messageFromServer)
            else:
                RecBuffer[messageFromServer["uuid"]]=messageFromServer["message"]
        elif(isNACK(data)):
            nackMessage=eval(data)
            print("NACK message %s" %str(nackMessage))
            demandedSeqNo = nackMessage["NACK"]
            if demandedSeqNo in sendBuffer.keys():
                sendMessageToAll(str(sendBuffer[demandedSeqNo]))
            else:
                continue
                
        else:
            
            message = eval(data)
            print("Message with seqNo %s "% str(message))
            if(expectedSeqNo(message["seq"])):
                data = applyOperation(message["message"])
                seq_no+=1
                postOperationWithSeq(message,data)
                if(isLeader() and len(RecBuffer)!=0):
                    LeaderOperation(RecBuffer[list(RecBuffer.keys()[0])])

            else:
                print("Sending NACK message")
                for i in range(seq_no,message["seq"]+1):
                    sendNack(i)
                #will add the code later

