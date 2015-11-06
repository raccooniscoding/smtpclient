# Script name    : smtp.py
# Author         : Abhishek kadian
# Created        : 5 November,2015
# Last Modified  :
# Version        : 1.0


# Description: SMTP Client without using python's library: smtplib



import ssl
import base64
from socket import *

sender = raw_input('Enter your email address \n')

#mail server
splt = sender.split('@',1)
if splt[1]=='gmail.com':
    mailserver = 'smtp.gmail.com'
    portnumber = 465

elif splt[1] == 'yahoo.com':
	mailserver = 'smtp.mail.yahoo.com'
	portnumber = 587

elif splt[1]=='hotmail.com':
	mailserver = 'smtp.live.com'
	portnumber = 465

else:
	print 'Only Google,Yahoo and Hotmail servers supported in this version'

password = raw_input('Enter your password\n')
receiver = raw_input('Enter receiver email address\n')

#create a socket called client socket and establish connection
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver,portnumber))

recv = clientSocket.recv(1024)
print recv
if recv[:3] != '220':
    print "220 Reply not received from server"

# Send HELO command and print server response
heloCommand = "HELO Alice\r\n"
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
if recv1[:3] != '250':
    print "250 Reply not received from server"

# Use TLS
clientSocket.send("STARTTLS\r\n")
recv = clientSocket.recv(1024)
print recv
if recv[:3] != '220':
    print " 220 Reply not received from server"

# use SSL
ssl_clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

#User Auth
authComm = "auth login\r\n"
ssl_clientSocket.send(authComm)

#usernames and passwords have to be base64 encoded.
ssl_clientSocket.send(base64.b64encode(sender)+'\r\n')
ssl_clientSocket.send(base64.b64encode(password)+'\r\n')
recv = ssl_clientSocket.recv(1024)
print recv

# Send MAIL FROM command
mailFrom = "mail FROM:<"+sender+">\r\n"
ssl_clientSocket.send(mailFrom)
recv = ssl_clientSocket.recv(1024)
print recv

# Send RCPT TO command
rcptTo = "rcpt TO:<"+receiver+">\r\n" 
ssl_clientSocket.send(rcptTo)
recv = ssl_clientSocket.recv(1024)
print recv

# Send DATA Command
ssl_clientSocket.send("data\r\n")
recv = ssl_clientSocket.recv(1024)
print recv

msg = raw_input('Enter Your Message Here')
endmsg = '\r\n.\r\n'
sendmsg = msg + endmsg

#send message data
sendData = "From:"+sender+"\r\nTo:"+receiver+"\r\n\r\n%s" %(sendmsg)
ssl_clientSocket.send(sendData)
recv = ssl_clientSocket.recv(1024)
print recv

#send the quit command and close
ssl_clientSocket.send("quit\r\n")
recv = ssl_clientSocket.recv()
ssl_clientSocket.close()
print recv

