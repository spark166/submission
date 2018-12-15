"""
Multi-threaded server.  Once a connection is accepted, a new 
thread is created to serve the client.
"""
import random
import socket
from thread import start_new_thread
import time

PORT = 12345
replica_port =12346
#host = '130.85.241.172'  #localhost
#host = '127.0.0.1'  #localhost
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
print('Registry is running at: ', host)

replica_hard = '130.85.241.172'    #########################################need to hard code############

add_wsdl = {}  #dict to hold wsdl addresses
add_load = {}  #load dictionary
sub_wsdl = {}
sub_load = {}
hel_wsdl = {}
hel_load = {}

#each new thread executes this function
def contacted(clientsocket):
    #receive string from client
    wsdl_response=""
    mssg = clientsocket.recv(1024)
    print('mssg: ', mssg)

#####send to replica
    #create a socket object with IPv4 and TCP protocol
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect to a server with host address and specified port
    s1.connect((replica_hard, replica_port))

    #send wsdl address to the registry server
    print ('publishing wsdl to replica')
    s1.send(mssg)
    s1.close()
####

    tok = mssg.split(" ")
    # if message received is a wsdl, not a request
    if (mssg[0:3] == 'Add'):
        add_wsdl[tok[0]] = tok[1]
        add_load[tok[0]] = 0
        print('wsdl array has: ')
        for key in add_wsdl:
            print(key + ": " + add_wsdl[key])
    elif (mssg[0:3] == 'Sub'):
        sub_wsdl[tok[0]] = tok[1]
        sub_load[tok[0]] = 0
        print('wsdl array has: ')
        for key in sub_wsdl:
            print(key + ": " + sub_wsdl[key])
    elif (mssg[0:3] == 'Hel'):
        hel_wsdl[tok[0]] = tok[1]
        hel_load[tok[0]] = 0
        print('wsdl array has: ')
        for key in hel_wsdl:
            print(key + ": " + hel_wsdl[key])
    # for request for service
    else:
        # find min load
        if (tok[1][0:3]=='Add'):
            min_key_val = min(add_load.items(), key=lambda x: x[1]) 
            wsdl_response = add_wsdl[min_key_val[0]]
            add_load[min_key_val[0]] += 1
            print("wsdl_response: "+wsdl_response)
            print('addition load: ')
            for key, val in add_load.items():
                print(key, val)
        
        elif (tok[1][0:3]=='Sub'):
            min_key_val = min(sub_load.items(), key=lambda x: x[1]) 
            wsdl_response = sub_wsdl[min_key_val[0]]
            sub_load[min_key_val[0]] += 1
            print("wsdl_response: "+wsdl_response)
            print('subtract load: ')
            for key, val in sub_load.items():
                print(key, val)

        elif (tok[1][0:3]=='Hel'):
            min_key_val = min(hel_load.items(), key=lambda x: x[1]) 
            wsdl_response = hel_wsdl[min_key_val[0]]
            hel_load[min_key_val[0]] += 1
            print("wsdl_response: "+wsdl_response)
            print('hello load: ')
            for key, val in hel_load.items():
                print(key, val)
        else:
            print("UNRECOGNIZED REQUEST")

#        if (len(wsdl)==1):
#            r=0
#        else:
#            r = random.randint(0,len(wsdl)-1)
#        print("length of wsdl array: ", len(wsdl), " random value selected: ", r)
#        wsdl_response = wsdl[r]
        
        clientsocket.send(wsdl_response)

    #delay added to test multi-threading parallelism
    #time.sleep(1)
    #send reverse message to the client
    #clientsocket.send(mssg_reverse)
    clientsocket.close()


#create a socket object with IPv4 and TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to host addr and port
s.bind((host, PORT))
#listen to socket, queue as many as 8 connect requests
s.listen(8)

while True:
    #accept connection requests, this method is blocking
    (clientsocket, addr) = s.accept()
    print "Accepted connection from ", addr
    #multi-threading by start a new thread, which executes the argument's function
    start_new_thread(contacted, (clientsocket,))

s.close()