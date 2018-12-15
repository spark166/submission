from zeep import Client
import socket  #socket library
import os
import pyping

PORT = 12345
PORT2 = 12346
#registry_hard = '127.0.0.1'  #localhost
registry_hard = '130.85.251.172' 
replica_hard = '130.85.241.172'
#host = socket.gethostname()  #return a hostname of this machine

mssg = 'Request Subtracter'

# ping if registry is up
response = pyping.ping(registry_hard)
if response.ret_code == 0:
  print('registry at '+registry_hard+ ' is up.')
  registry = registry_hard
else:
  print ('registry at '+registry_hard+' is down!')
  registry = replica_hard
  PORT = PORT2
  

#create a socket object with IPv4 and TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect to a server with registry address and specified port
s.connect((registry, PORT))
#send the user input to the server
s.send(mssg)
#receive and print to a screen
wsdl_received = s.recv(1024)
print('received the following WSDL from '+registry+': '+ wsdl_received)

s.close()

#generate a SOAP client using the received WSDL
client = Client(wsdl_received+'?wsdl')
result = client.service.subtractNum(5,2)
print('The difference of 5 and 2 is')
print(result)