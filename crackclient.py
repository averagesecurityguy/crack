#!/usr/bin/env python
'''
Crackclient makes xmlrpc calls to a crack server to automate password
cracking. Crackclient takes a file, a server:port combination, and a hash
type. The file and hash type are passed to the server and the server returns
an id. The id can be polled to get the results and to see if all of the
cracking processes are finished.

Acceptable hash types are defined in config file associated with
listening crackserver instance.

While crackserver.py is dependent upon core modules contained in other files,
crackclient.pl is dependent only upon standard python modules

'''

import xmlrpclib
import argparse
import time

#------------------------------------------------------------------------------
# Configure Argparse to handle command line arguments
#------------------------------------------------------------------------------
desc = """Crackclient makes XMLRPC calls to a crack server to automate password
cracking. Crackclient takes a file, a server:port combination, and a hash type.
The file and hash type are passed to the server and the server returns an id.
The id can be polled to get the results and to see if all of the cracking
processes are finished."""

parser = argparse.ArgumentParser(description=desc)
parser.add_argument('file', action='store', default='hashes.txt',
                    help='Specify a hash file (default: hashes.txt)')
parser.add_argument('server', action='store', default='127.0.0.1:8000',
                    help='Specify a server and port (default: 127.0.0.1:8000)')
parser.add_argument('type', action='store', default='md5',
                    help='Specify the hash type (default: md5)')


#------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------

args = parser.parse_args()

# Open connection to xmlrpc server
try:
    s = xmlrpclib.ServerProxy('http://' + args.server)
except Exception, err:
    print "Error opening connection to server " + args.server + ": " + str(err)

#Upload hash file to server, send crack request to server and receive ID
with open(args.file, 'rb') as handle:
    binary_data = xmlrpclib.Binary(handle.read())
id, msg = s.crack(binary_data, args.type)

if id == 0:
    print msg
else:
    # Poll server for completion status and results using ID.
    complete = False
    wait = 10
    while True:
        time.sleep(wait)
        complete, results = s.results(id)
        if results != []:
            for r in results:
                print r.rstrip('\r\n')
        if complete: break    
