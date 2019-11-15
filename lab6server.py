import socket
import sys
import binascii
from check import *
IDcheck = None
msgID = 1
def make_pkt(msg):
        global msgID
        if(msgID == "0"):
                msgID = "1"
        else:
                msgID = "0"

        pktID = msgID
        pktMsg = msgID + msg
        pktchecksum = ip_checksum(pktMsg)
        pktMsg = msgID + pktchecksum + msg
        return pktMsg.encode('utf-8')

def processData(data):
  global IDcheck
  #break up the string
  msgID  = data[0]
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
    if IDcheck == "0":
      IDcheck = "1"
    else:
      IDcheck = "0"

  else:
    isCorrupt = True  
  result = {"message":msg,"msgID":msgID, "pktchecksum":pktchecksum,"isCorrupt": isCorrupt }
  return result
  
HOST = ''
PORT = 8888

try:
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  print("Print Socket Created")

except (socket.error,msg):
  print ("Failed to create socket. Error Code : " + str(msg[0]))
  sys.exit()


try:
  s.bind((HOST,PORT))

except socket.error as msg:
  print ('Bind failed. Error Code : ' + str(msg))
  sys.exit()

while 1:
  d = s.recvfrom(1024)
  data = d[0]
  addr = d[1]
  data = data.decode("utf-8")
  if not data:
    break
  result = processData(data)
  if(result["isCorrupt"] == True or result["ACK"] is not ++cumACK):
            #send oldACK
           
  if(result["isCorrupt"] == False):
    reply = 'OK...' + result["message"]
    reply = make_pkt(reply)
    s.sendto(reply, addr)
    print("Message: " + result["message"])
  else:
    reply = "NAK"
    reply = make_pkt(reply)
    s.sendto(reply,addr)
  
s.close()


