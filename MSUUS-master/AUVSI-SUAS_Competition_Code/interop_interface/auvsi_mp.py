# Add paths to libraries that script needs.
import sys
sys.path.append('c:\python27\lib')
# Add the path to the interoperability libraries here!

# Configure the script.
INTEOR_URL = 'http://127.0.0.1'
INTEROP_USERNAME = 'testuser'
INTEROP_PASSWORD = 'testpass'
POLL_SEC = 0.1
PRINT_SEC = 10

import datetime
import threading
from time import time

try:
    from interop import AsyncClient
    from interop import Telemetry
except ImportError as e:
    raise ImportError(
        'Failed to import interop libraries. Have you added the libs to '
        'the path? Error: %s' % e)

# Create a client and connect to interop.
client = AsyncClient(INTEROP_URL, INTEROP_USERNAME, INTEROP_PASSWORD)

# Tracks the uploads since last print.
sent_lock = threading.Lock()
last_print = datetime.datetime.now()
sent_since_print = 0


# Tracks upload success and prints any exceptions.
def handle_upload_result(future):
    if future.exception():
        print 'Request Failed. Exception: %s' % str(future.exception())
    else:
        with sent_lock:
            sent_since_print += 1

# Continuously poll for new telemetry and send to server.
last_telemetry = Telemetry(0, 0, 0, 0)
while True:
    telemetry = Telemetry(latitude=cs.lat,
                          longitude=cs.lng,
                          altitude=cs.alt,
                          uas_heading=cs.groundcourse)
    if telemetry != last_telemetry:
        client.post_telemetry(telemetry).add_done_callback(
            handle_upload_result)
        last_telemetry = telemetry

    now = datetime.datetime.now()
    since_print = (now - last_print).total_seconds()
    if since_print >= PRINT_SEC:
        with sent_lock:
            local_sent_since_print = sent_since_print
            sent_since_print = 0
        print 'Upload Rate: %f' % (local_sent_since_print / since_print)
        last_print = now

    time.sleep(POLL_SEC)
