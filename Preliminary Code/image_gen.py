from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
import random
import webcolors
import math
import os

# A target class
# No methods
# Just a holder for variables
class target():
	def __init__(self, path, letter, letter_color, shape, shape_color, image, label):
		self.path = path
		self.letter = letter
		self.letter_color = letter_color
		self.shape = shape
		self.shape_color = shape_color
		self.label = label
		self.image = image

# Changes black to the specified color
def replace_color(image_path, color):
	img = Image.open(image_path).convert('RGB')
	#pixdata is the 2d list for image
	pixdata = img.load()
	# Loop to loop through the image?
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			if pixdata[x, y] == (0,0,0):
				pixdata[x, y] = webcolors.name_to_rgb(color)
	
	return img

# Used to generate testing images
def generate_image(requested_letter = None, requested_shape = None, requested_letter_color = None, requested_shape_color = None, requested_label = None, return_type = "target"):	
	#----------------------------------------------------------------
	# Set up our lists of different letters, shapes, and colors
	letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	shape_list = ['Circle', 'Semicircle', 'Quartercircle', 'Triangle', 'Square', 'Rectangle', 'Trapezoid', 'Pentagon', 'Hexagon',
'Heptagon', 'Octagon', 'Star', 'Cross']
	color_list = ['White', 'Black', 'Gray', 'Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Brown', 'Orange']
	#----------------------------------------------------------------




	#----------------------------------------------------------------
	# This code block is for setting up the random images
	if (requested_letter == None):
		letter = letter_list[random.randrange(0,26)]
	else:
		letter = requested_letter

	if (requested_shape == None):
		shape_index = random.randrange(0,13)
		shape = shape_list[shape_index]
	else:
		shape = requested_shape
	
	if (requested_letter_color == None):
		letter_color_temp = random.randrange(0,10)
		letter_color = color_list[letter_color_temp]
	else:
		letter_color = requested_letter_color
		letter_color_temp = color_list.index(letter_color)
	
	if (requested_shape_color == None):
		shape_color_temp = random.randrange(0,10)
		while (shape_color_temp == letter_color_temp):
			shape_color_temp = random.randrange(0,10)
		shape_color = color_list[shape_color_temp]
	else:
		shape_color = requested_shape_color
	#----------------------------------------------------------------
	
	# Loads up a random background from grass samples
	background_path = 'grass_images/Grass'+str(random.randint(1,7))+'.png'
	
	# Loading from random shape pngs
	shape_path = 'shapes/' + shape + '_' + str(random.randint(1,2)) + '.png'
	composite_path = letter_color + "_" + letter + "_" + shape_color + "_" + shape + ".png"

	#----------------------------------------------------------------
	# Not sure exactly what this block of code does
	composite = Image.open(background_path)
	shape_temp = Image.open(shape_path)
	shape_temp2 = shape_temp.copy()
	
	shape_temp2.paste(shape_temp, mask=shape_temp)
	#----------------------------------------------------------------
	
	#----------------------------------------------------------------
	# Applies some filters to the image
	shape_temp2 = shape_temp2.filter(ImageFilter.EDGE_ENHANCE)
	shape_temp2 = shape_temp2.filter(ImageFilter.GaussianBlur(3))
	
	# Not sure exactly what this block of code does
	shape_temp2.paste(replace_color(shape_path, shape_color), mask=shape_temp)
	composite.paste(shape_temp2, (64,64), shape_temp)
	temp = ImageDraw.Draw(composite)
	font = ImageFont.truetype("arial.ttf", 62)
	W, H = 256, 256
	w, h = temp.textsize(letter)
	temp.text((108, 99),letter,letter_color,font=font)
	
	# This is where rotation happens 
	composite = composite.rotate(random.randint(0,359))
	scalex = random.randint(-5,5)
	scaley = random.randint(-5,5) 
	scale = random.randint(-27,27) 
	composite = composite.resize((256+scalex+scale,256+scaley+scale), Image.ANTIALIAS)
	composite = composite.crop((32+math.floor(scalex+scale), 32+math.floor(scaley+scale), 224+math.floor(scalex+scale), 224+math.floor(scaley+scale)))
	composite = composite.resize((80,80), Image.ANTIALIAS)
	randx = random.randint(4,12)
	randy = random.randint(4,12) 
	composite = composite.crop((randx, randy, randx+64, randy+64))

	# Here is the distortion, can probably pull into variable and randomize and
	composite = composite.filter(ImageFilter.GaussianBlur(0.5))
	
	#----------------------------------------------------------------
	# Looks like the OS side of outputing
	directory = 'composites/shapes/'+letter_list[shape_index].lower()
	if not os.path.exists(directory):
		os.makedirs(directory)
	composite.save(directory+'/'+composite_path)

	image = composite.convert("RGBA")
	#----------------------------------------------------------------

	
	#----------------------------------------------------------------
	# Looks like the ability to change out what
	# output to output	
	if (return_type == "target"):
		return target(composite_path, letter, letter_color, shape, shape_color, image, label)
	elif (return_type == "set"):
		return image
	elif (return_type == "shape"):
		label = shape_list.index(shape)		
		return image, label
	elif (return_type == "letter"):
		label = letter_list.index(letter)		
		return image, label
