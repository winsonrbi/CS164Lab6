import socket
import logging
import sys
import queue
from check import *
import threading

# create dgram udp socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print('Failed to create socket')
	sys.exit()

host = 'localhost';
port = 8888;
msgID = 1
IDcheck = None
resendLastMessage = False;
window = 4
base = 0
squenceNum = 0

def timeout(s):
    d = s.recvfrom(1024)
    reply = d[0]
    addr = d[1]
    reply = reply.decode("utf-8")
    reply = processData(reply)
    returnQueue.put(reply)
    return


def processData(data):
        global IDcheck
        # break up the string
        msgID = data[0]
        pktchecksum = data[1:3]
        msg = data[3:]
        if(IDcheck == None):
                IDcheck = msgID
        else:
                if IDcheck == "0":
                        IDcheck = "1"
                else:
                        IDcheck = "0"

        if pktchecksum == ip_checksum(msgID+msg) and IDcheck == msgID:
                isCorrupt = False
        else:
                isCorrupt = True
        result = {"message": msg, "msgID": msgID,"pktchecksum": pktchecksum, "isCorrupt": isCorrupt}
        return result


def make_pkt(msg):
	global msgID
  global base
  global window

	if(msgID == "0"):
		msgID = "1"
	else:
		msgID = "0"

	pktID = msgID
	pktMsg = msgID + msg

	pktchecksum = ip_checksum(pktMsg)
	pktMsg = str(sequence)+msgID + pktchecksum + msg
	return pktMsg.encode('utf-8')


threads = list()

while(1):
        
        returnQueue = queue.Queue()
        if(resendLastMessage == False):
                msg = input('Enter Message to Send: ')
                msg = make_pkt(msg)
        try:
                s.sendto(msg, (host, port))
                thread = threading.Thread(target=timeout, args=(s,))
                thread.start()
                thread.join(2)

                while thread.is_alive():  # resend message and wait for timeout again
                    # resend packet due to timeout
                        print("Timeout occured, resending message")
                        s.sendto(msg, (host, port))
                        thread.join(2)
                
                returnVal = returnQueue.get()
                if(returnVal["isCorrupt"] == True or returnVal["message"] == "NAK"):
                        resendLastMessage=True

                else:
                        resendLastMessage=False
                        print("Server Reply: " + returnVal["message"])
        except socket.error as msg:
                print('Error Code: ' + msg)
                sys.exit()
