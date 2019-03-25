# Created by: Yevhenii Ganusich
# UCID: yog2
# Section: 004

import sys
import os
import datetime, time
from socket import *

# This function is responsible for assembling the HTTP GET request
def assembleRequest(host, port, fileName):
    # Conditional GET if cache file exists
    if(os.path.isfile('cache.txt') == True):
        secs = os.path.getmtime('cache.txt')
        secs2 = time.gmtime(secs)
        last_mod = time.strftime("%a, %d %b %Y %H:%M:%S %Z\r\n", secs2)
        request = "GET /" + str(fileName) +" HTTP/1.1\r\n" + "Host: " + str(host) + ":" + str(port) + "\r\n" + "If-Modified-Since: " + last_mod + "\r\n"
    # Regular GET if cache doesn't exist
    else:
        request = "GET /" + str(fileName) +" HTTP/1.1\r\n" + "Host: " + str(host) + ":" + str(port) + "\r\n\r\n"
    
    # Display the request being sent to the server and return to main
    print(request)
    return request



# This function is responsible for disassembling the message received from the server
def disassembleReply(message):
    # Break up the message into 
    inLines = message.split("\r\n")
    # Disregard any other HTTP code because no action needed
    if("200 OK" in inLines[0]):
        # Retrive HTML contents and write them to a file
        # Assuming proper HTML format, with using <!DOCTYPE html> and ending with </html> like any HTML document
        htmlStart = "<!"
        htmlEnd = "</html>"
        htmlContents = str(message[message.find(htmlStart):message.find(htmlEnd)+7])
        # Create cache file and let it be overwritten every time we need to update cache by adding w+ argument
        f=open("cache.html", "w+")
        f.write(htmlContents)
        f.close()
        
    print(message)


  
# Get the server hostname, port as command line arguments
argv = sys.argv
# Main argument containing server, port and filename
mainarg = str(sys.argv[1])
# Retrieving ipaddress, Port Number and File name
host = mainarg.split(':')[0]
port = int(mainarg[mainarg.find(":")+1:mainarg.find("/")])
fileName = mainarg.split('/')[1]
request = assembleRequest(host, port, fileName)
# Create TCP client socket. Note the use of SOCK_STREAM for TCP packet
clientSocket = socket(AF_INET, SOCK_STREAM)
# Create TCP connection to server
clientSocket.connect((host, port))
# Send data through TCP connection
clientSocket.send(request.encode())
# Create a buffer that will hold the data
buffer=""
# Receive the server response
while True:
    data = clientSocket.recv(1024)
    if data:
        buffer += data.decode()
    elif not data:
        break
disassembleReply(buffer)
# Close the client socket
clientSocket.close()

