# from http.server import HTTPServer, BaseHTTPRequestHandler
# from os import curdir
# import sys

# if len(sys.argv)!=2:
#     print("No Such Command!")
#     print("Usage:$python Filename.py port")
#     sys.exit()
# class Serv(BaseHTTPRequestHandler):
#     def do_GET(self):
#         try:
#             file_to_open = open(curdir+self.path)
#             self.send_response(200)
#             self.wfile.write(bytes(file_to_open.read(),'utf-8'))
#         except:
            
#             self.send_response(404)
#         self.end_headers()
            

# httpd = HTTPServer(('localhost',int(sys.argv[1])),Serv)
# httpd.serve_forever()


import sys
import socket
from os import curdir

#Specify the port 
if len(sys.argv)!=2:
    print("No Such Command!")
    print("Usage:$python Filename.py port")
    sys.exit()
port= int(sys.argv[1])
serversock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversock.bind(('',port))
serversock.listen(1) #listen for connection
# print("Web server up on port",port) #print port address

#Start the while loop.
while True:
    clientsock,addr = serversock.accept()
    try:
        message = clientsock.recv(1024)
        path = message.split()[1] # message.split()[1]is bytes type, can be decoded by using decode()
        # print(path)
        # p2 = path.decode()
        # print(curdir+p2[1:])
        # f = open(curdir+p2[1:])
        # clientsock.send(bytes('HTTP/1.1 200 OK \r\n','utf-8'))
        # clientsock.send(bytes(f.read(),'utf-8'))
        clientsock.close()


    except IOError:
        pass
        #Send response message for the file not found.
        print ("404 Not Found")
        clientsock.send(bytes('HTTP/1.1 404 Not Found \r\n','utf-8'))