import sys
import socket

#invalid request exception
class InvalidRequest(Exception):
    pass

# #process raw request
# class Request():
#     def __init__(self,raw_request):
#         self.raw_request = raw_request
#         self.method, self.path, self.protocol, self.header = self.parse_request()

#     def parse_request(self):
#         #encode the request
#         unpack = [line.strip() for line in self.raw_request.splitlines()]

#         #check the validation of request method
#         method,path,protocol = [k.strip() for k in unpack[0].split()]
#         if method.decode() != 'GET':
#             raise InvalidRequest("Only accepts GET requests")
        
#         # create the header
#         header = {}
#         for k, v in [i.split(':', 1) for i in unpack[1:-1]]:
#             header[k.strip()] = v.strip()
#         return method, path, protocol, header

#     def __repr__(self):
#         return repr({'method': self.method, 'path': self.path, 'protocol': self.protocol, 'headers': self.header})
        
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
    message = clientsock.recv(1024)

    #check the validation of request method
    method = message.split()[0].strip()
    if method.decode() != 'GET':
        raise InvalidRequest("Only accepts GET requests")
    
    #read the request
    path = message.split()[1].strip()
    filename = path.decode()[1:]
    try:
        #'r' can only decode string but not image
        #'rb' decode everything in bytes
        with open (filename,'rb') as f:
            files= f.read()

        #create response
        length = len(files)
        clientsock.sendall(bytes("HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length: {length}\r\n\r\n","utf-8"))
        clientsock.sendall(files+bytes('\r\n','utf-8'))
        clientsock.close()
    except IOError:
        #no '\n' in the front of the header, will fail
        clientsock.sendall(bytes('\nHTTP/1.1 404 Not Found \r\n\r\n','utf-8'))
        clientsock.sendall(bytes('<h1><center>404 Error: File not Found</center><h1>','utf-8'))
        