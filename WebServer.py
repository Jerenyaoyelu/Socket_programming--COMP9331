import sys
import socket

#invalid request exception
class InvalidRequest(Exception):
    pass

#process raw request
class Request():
    def __init__(self,raw_request):
        self.raw_request = raw_request
        self.method, self.path, self.protocol, self.header = self.parse_request()

    def parse_request(self):
        #encode the request
        unpack = [line.strip() for line in self.raw_request.splitlines()]

        #check the validation of request method
        method,path,protocol = [k.strip() for k in unpack[0].split()]
        if method.decode() != 'GET':
            raise InvalidRequest("Only accepts GET requests")
        
        #create the header
        header = {}
        for t in unpack[1:-1]:
            for h,c in t.strip().split(":",1):
                header[h.strip()] = c.strip()
        return method, path, protocol, header

    def __repr__(self):
        return repr({'method':self.method,'path':self.path,'protocol':self.protocol,'header':self.header})
        
#Set up the server
#Specify the port 
if len(sys.argv)!=2:
    print("No Such Command!")
    print("Usage:$python Filename.py port")
    sys.exit()
port= int(sys.argv[1])
serversock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversock.bind(('',port))
serversock.listen(5) #listen for connection

#Start the while loop.
while True:
    clientsock,addr = serversock.accept()
    try:
        message = clientsock.recv(1024)
        request = Request(message)
        print(repr(request))
        clientsock.send(repr(request))
        clientsock.close()
    except InvalidRequest as e:
        clientsock.send(bytes('HTTP/1.1 400 Not Found\r\n','utf-8'))
        clientsock.send('Content-Type: text/html' + '\r\n'*2)
        clientsock.send('<h1>Invalid Request: %s</h1>' % e)