import socket
import sys
from datetime import datetime
import pytz
import time
import struct
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_port=int(sys.argv[1])
# Bind the socket to the port
server_address = ('localhost', server_port)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
port_number = [10000,10001,10002]
port_number.remove(server_port)
while True:
        #print >>sys.stderr, '\nwaiting to receive message'
        data, address = sock.recvfrom(4096)
        print(data)
        #print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
        #print >>sys.stderr, data
        """
        if data:
                #sent = sock.sendto(str(datetime.utcnow().timestamp()).encode("utf-8"), address)
                #print(sys.stderr, 'sent %s bytes back to %s' % (sent, address))
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
                for port in port_number:
                    my_socket.sendto("wearetherock", ('<broadcast>' ,port[i]))
                my_socket.close()
        """

