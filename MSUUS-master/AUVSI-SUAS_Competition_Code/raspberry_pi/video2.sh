sudo modprobe -v bcm2835-v4l2

/opt/vc/bin/raspivid -t 0 -hf -fps 20 -w 300 -h 300 -o - | gst-launch-1.0 fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=192.168.1.4 port=5000
