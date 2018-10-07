"""
NOT SURE IF THIS IS "TEST" BECAUSE IT'S TESTING SOMETHING OR IT'S TEST CODE.
"""

import tflearn

"""
NumPy is the fundamental package for scientific computing with Python. It contains among other things:

a powerful N-dimensional array object
sophisticated (broadcasting) functions
tools for integrating C/C++ and Fortran code
useful linear algebra, Fourier transform, and random number capabilities
"""
import numpy as np

# This is TensorFlow stuff
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation

# Pretty sure this is Python Image Library?
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import sys


# LOAD IMAGE AND PRE-PROCESS
tmp_img = Image.open(sys.argv[1]) # Can pass an image file as a parameter to the script
tmp_img = tmp_img.resize((64,64), Image.ANTIALIAS)
tmp_img = tmp_img.convert('L')
enh_c = ImageEnhance.Contrast(tmp_img)
tmp_img = enh_c.enhance(12.0)
tmp_img = tmp_img.filter(ImageFilter.SMOOTH_MORE)
tmp_img = tmp_img.filter(ImageFilter.SMOOTH_MORE)
tmp_img = tmp_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
tmp_img = tmp_img.filter(ImageFilter.SMOOTH_MORE)
tmp_img = tmp_img.filter(ImageFilter.EDGE_ENHANCE_MORE)

image = np.reshape(tmp_img.getdata(), (64, 64, 1))

tmp_img.show()


img_preprocessor = ImagePreprocessing()
img_distortion = ImageAugmentation()

# SET UP NETWORK MODEL
network = input_data(shape=[None, 64, 64, 1], 
	data_preprocessing=img_preprocessor,
	data_augmentation=img_distortion)
	
# convolution 2
network = conv_2d(network, 16, 5, activation='relu')
# max pooling 2
network = max_pool_2d(network, 2)
# convolution 2
network = conv_2d(network, 24, 3, activation='relu')
# max pooling 2
network = max_pool_2d(network, 2)
# dropout
#network = dropout(network, 0.3)
# convolution 2
network = conv_2d(network, 32, 3, activation='relu')
# max pooling 2
network = max_pool_2d(network, 2)
# dropout
#network = dropout(network, 0.3)
# fully-connected
network = fully_connected(network, 512, activation='relu')
# fully-connected
network = fully_connected(network, 512, activation='relu')
# dropout
network = dropout(network, 0.5)

network = fully_connected(network, 13, activation='softmax')
network = regression(network, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.01)

# This path is hard coded and will need to be changed
model = tflearn.DNN(network, tensorboard_verbose=2, checkpoint_path='/media/salvi/SSD480/checkpoints/shape_classifier.tfl.ckpt')
model.load('shape_classifier.tfl')

predicted_target_label = model.predict([image])

letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
shape_list = ['Circle', 'Semicircle', 'Quartercircle', 'Triangle', 'Square', 'Rectangle', 'Trapezoid', 'Pentagon', 'Hexagon', 'Heptagon', 'Octagon', 'Star', 'Cross']

index = np.argmax(predicted_target_label)
print("Predicted target shape is a " + shape_list[index])
