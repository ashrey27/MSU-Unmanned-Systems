from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

def killgphoto2process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate ()

    for line in out.splitlines ():
        if b'gvfsd-gphoto2' in line:
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)
            
shot_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
filename = 'filename'

triggerCommand = str("--capture-image-and-download --filename " + shot_time)

def captureImages():
    gp(triggerCommand)
    sleep(12)
    
#x = 1
#while x == 1:
sleep(3)
killgphoto2process()
print ('hello')
captureImages()
print ('yes')
killgphoto2process()
