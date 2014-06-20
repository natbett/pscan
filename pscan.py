#!/usr/bin/python
##
## Since we can't have telnet or nmap, I made my own.
## Extremely useful for testing firewall access.
##
import socket
import subprocess
import sys
import optparse
from datetime import datetime

subprocess.call('clear', shell=True)
parse = optparse.OptionParser()
parse.add_option('-r', help='Port range to scan',
                 dest='prtRange', default='0',
                 action='store')
options, args = parse.parse_args()
if len(args) == 2:
    remoteServer, prt = args
else:
    remoteServer = ''.join(args)

remoteServerIP = socket.gethostbyname(remoteServer)
print "-" * 60
print "Please wait, scanning remote host", remoteServerIP
print "-" * 60

t1 = datetime.now()
if options.prtRange == '0':
    try:
        port = int(prt)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((remoteServerIP, port))
        sock.settimeout(None)
        if result == 0:
            print "Port {0}: \t Open".format(port)
        sock.close()
    except KeyboardInterrupt:
        print "You pressed Ctrl+C"
        sys.exit()
    except socket.gaierror:
        print "Hostname could not be resolved. Exiting"
        sys.exit()
    except socket.error:
        print "Couldn't connect to server"
        sys.exit()
else:
    ports = options.prtRange.split("-")
    low = int(ports[0])
    high = int(ports[1]) + 1
    try:
        for i in range(low, high):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((remoteServerIP, i))
            sock.settimeout(None)
            if result == 0:
                print "Port {0}: \t Open".format(i)
            sock.close()
    except KeyboardInterrupt:
        print "You pressed Ctrl+C"
        sys.exit()
    except socket.gaierror:
        print "Hostname could not be resolved. Exiting"
        sys.exit()
    except socket.error:
        print "Couldn't connect to server"
        sys.exit()

t2 = datetime.now()
total = t2 - t1
print "Scanning Completed in: ", total
