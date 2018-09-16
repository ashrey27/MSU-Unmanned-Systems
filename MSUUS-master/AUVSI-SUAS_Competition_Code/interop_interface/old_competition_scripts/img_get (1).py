import os
import sys
import paramiko
import time

local = "img/"
remote = "/home/pi/Desktop/MSUUAS/img/"
server = sys.argv[1]
#server = "192.168.1.28"
username = "pi"
password = "raspberry"

ssh = paramiko.SSHClient() 
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(server, username=username, password=password)
sftp = ssh.open_sftp()

i = 0

while True:
    time.sleep(3.0)        
    localpath = local + "img_"+str(i)+".jpg"
    remotepath = remote + "img_"+str(i)+".jpg"
    
    try:
        sftp.get(remotepath, localpath)
        i+=1
    except:
        print("error: something went wrong grabbing img_"+str(i)+".jpg")

    if (i > 14):    
        try:
            sftp.remove(remote + "img_"+str(i-15)+".jpg")
        except:
            print("error: something went wrong deleting img_"+str(i-15)+".jpg")

        
sftp.close()
ssh.close()
    
