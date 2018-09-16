# This just looks like a simple script.
# Much less trouble than expected.
import qrtools
qr = qrtools.QR()
qr.decode("test2.jpg")
print(qr.data)
