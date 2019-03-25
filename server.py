# Created by: Yevhenii Ganusich
# UCID: yog2
# Section: 004

import sys
import os
import datetime
import time
import codecs
from socket import *


# This function takes care of the request and assembles HTTP reply message
def processRequest(request):
    retMess=""
    # Break up request into separate lines
    inLines = request.split('\n')
    # Retrieve filename by finding everything after character / and before second occurence of space
    fileName = str(inLines[0][inLines[0].find("/")+1:inLines[0].find(" ", 5, len(inLines[0]))])
    # Get current date in HTTP format
    date = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime())

    # If the server has the file
    if(os.path.isfile(fileName) == True):
        # Get the last modified date of the HTML file in seconds
        secs = os.path.getmtime('filename.html')
        secs2 = time.gmtime(secs)
        last_mod = time.strftime("%a, %d %b %Y %H:%M:%S %Z", secs2)

        # Conditional GET request
        if len(inLines)>4:
            # Retrieve the Last-Modified-Date of the cached file in seconds
            secsCache = os.path.getmtime('cache.html')
            # If the file was cached after the server file was last modified, return 304
            if(secsCache > secs):
                retMess = "HTTP/1.1 304 Not Modified" + "\r\n" + "Date: " + date + "\r\n\r\n"
            # If cached file is older than the server file, return 200
            else:
                # Get the size of the file
                fileSize = os.path.getsize(fileName)
                # Read file into a string called fileContent
                fileContent = open(fileName, "r").read()
                # Assembling return message
                retMess = "HTTP/1.1 200 OK" + "\r\n" + "Date: " + date + "\r\n" + "Last-Modified: " + str(last_mod) + "\r\n" + "Content-Length: " + str(fileSize) + "\r\n" + "Content-Type: text/html; charset=UTF-8\r\n\r\n" + fileContent

        # Non Conditional GET request
        else:
            # Get the size of the file
            fileSize = os.path.getsize(fileName)
            # Read file into a string called fileContent
            reader =codecs.open(fileName, 'r')
            fileContent = reader.read()
            # Assembling return message
            retMess = "HTTP/1.1 200 OK\r\n" + "Date: " + date + "\r\n" + "Last-Modified: " + str(last_mod) + "\r\n" + "Content-Length: " + str(fileSize) + "\r\n" + "Content-Type: text/html; charset=UTF-8\r\n\r\n" + fileContent

    # Otherwise server doesn't have the file that is being requested
    else:
        retMess = "HTTP/1.1 404 Not Found\r\n" + "Date: " + date +"\r\n\r\n"
    return retMess
        


# Get the server hostname, port as command line arguments
argv = sys.argv
serverIP = str(sys.argv[1])
serverPort = int(sys.argv[2])
# Create a TCP "welcoming" socket. Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)
# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
# Listen for incoming connection requests
serverSocket.listen(1)
print('The server is ready to receive on port: ' + str(serverPort))
# Loop forever listening for incoming connection requests on "welcoming" socket, create buffer
buffer=""
while True:
    # Accept incoming connection requests, and allocate a new socket for data communication
    connectionSocket, address = serverSocket.accept()
    # Create socket for client
    data = connectionSocket.recv(1024)
    if data:
        # Data received
        buffer += data.decode()
    elif not data:
        # Done receiving
        break
    reply = processRequest(buffer)
    connectionSocket.send(reply.encode())
    connectionSocket.close()
    