import sys
sys.path.append('c:\python35-32\lib')
import xmlrpc.client
from time import time
import json

__author__ = 'Jordan Salvi'

# creates a connection to the proxy server at the URL specified in the
# command line. For example: "python output.py http://localhost:9001"
server = xmlrpc.client.ServerProxy(sys.argv[1])

# the second argument from the command line will be used to create the
# json object that stores the target data. For example:
# python output.py http://localhost:9001 '{
#    "type": "standard",
#    "latitude": 38.1478,
#    "longitude": -76.4275,
#    "orientation": "n",
#    "shape": "star",
#    "background_color": "orange",
#    "alphanumeric": "C",
#    "alphanumeric_color": "blue" }'
target = json.loads(sys.argv[2])


try:
    # sends the target info to the proxy server
    server.target_data(target)
except xmlrpclib.Fault as err:
    print("A fault occurred")
    print("Fault code: %d" % err.faultCode)
    print("Fault string: %s" % err.faultString)
except:
    print(sys.exc_info()[0])

