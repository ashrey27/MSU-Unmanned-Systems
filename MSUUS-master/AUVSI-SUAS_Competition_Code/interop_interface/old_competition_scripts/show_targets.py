import sys
sys.path.append('c:\python35-32\lib')
import xmlrpc.client
from time import time
import json


__author__ = 'Jordan Salvi'

server = xmlrpc.client.ServerProxy(sys.argv[1])

try: 
    print(server.get_target_data())
except xmlrpclib.Fault as err:
    print("A fault occurred")
    print("Fault code: %d" % err.faultCode)
    print("Fault string: %s" % err.faultString)
except:
    print(sys.exc_info()[0])

