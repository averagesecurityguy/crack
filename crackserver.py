#!/usr/bin/env python
'''
Launches an XMLRPC listener for password cracking requests from crackclient.py
'''

import SimpleXMLRPCServer as sxml
import argparse
import os
import shutil
from modules.core_crackserver import *

desc = """Crackserver launches a XMLRPC server to handle password cracking requests."""

parser = argparse.ArgumentParser(description=desc)
parser.add_argument('-l', action='store', default='127.0.0.1',
                    help='IP address to listen on. (default: 127.0.0.1)')
parser.add_argument('-p', action='store', default='8000',
                    help='Port to listen on. (default: 8000)')
parser.add_argument('-c', action='store', default='crackserver.cfg',
                    help='Configuration file. (default: crackserver.cfg)')

args = parser.parse_args()

#check to see if specified config file exists; if not copy default
if os.path.exists(args.c):
    pass
else:
    shutil.copyfile("default.cfg", args.c)

# Create new CrackManager object to handle cracking process.
try:
    c = CrackManager(args.c)
    print "CrackManager configured successfully"
except Exception, err:
    print "CrackManager configuration unsuccessful:\n"
    print str(err)
    exit()
    
try:
    server = sxml.SimpleXMLRPCServer((args.l, int(args.p)),
        requestHandler=sxml.SimpleXMLRPCRequestHandler)
    print "XMLRPC server configuration successful."
except Exception, err:
    print "XMLRPC server configuration unsuccessful:\n"
    print str(err)
    exit()

# Register CrackManager functions to be used with by XMLRPC client.
server.register_introspection_functions()
server.register_function(c.crack_passwords, 'crack')
server.register_function(c.get_progress, 'results')
server.serve_forever()
