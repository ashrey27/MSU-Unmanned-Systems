import sys
import re
import Tkinter
from Tkinter import *



def to_decimal(in_str):
	(d,m,s,h) = re.split('\s',in_str, maxsplit=4)
	if (re.search('[swSW]', in_str)):
		sign = -1
	else:
		sign = 1
	return sign * (int(d) + float(m) / 60 + float(s) / 3600)

def main():
	top = Tkinter.Tk()
	top.title("GPS Conversion Tool")
	top.geometry("300x160")
	lat = Entry( top )
	lat_label = Label( top, text="Latitude" )
	lon = Entry( top )
	lon_label = Label( top, text="Longitude" )
	out = Entry( top )
	out_label = Label( top, text="Output")
        def convert_callback():
                out.delete(0, END)
                out.insert(0, str(to_decimal(lat.get())) + ", " + str(to_decimal(lon.get())))

	calc = Button( top, text="Convert", command = convert_callback)
	lat_label.pack()
	lat.pack()
	lon_label.pack()
	lon.pack()
	out_label.pack()
	out.pack()
	calc.pack()
	top.mainloop()
	#output_str = str(to_decimal(argv[0])) + ' ' + str(to_decimal(argv[1]))
	#print(output_str)

if __name__ == "__main__":
	main()
