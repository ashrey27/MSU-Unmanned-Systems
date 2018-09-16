"""
Author: Klint Kaercher
Date: 12/20/17
Description: Testing some different coding from Jordan's 'target_classifier_test.py'
Changes: Added letter network. Changed parameters of 'target_classifier_test.py' to match those in the training
scripts. I believe those need to be the same in order to load in the trained weights to those networks. I could be
mistaken, though.
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
tmp_img = Image.open(sys.argv[1])  # Can pass an image file as a parameter to the script
tmp_img = tmp_img.resize((64, 64), Image.ANTIALIAS)
tmp_img = tmp_img.convert('L')
enh_c = ImageEnhance.Contrast(tmp_img)
tmp_img = enh_c.enhance(12.0)
tmp_img = tmp_img.filter(ImageFilter.SMOOTH_MORE)
tmp_img = tmp_img.filter(ImageFilter.SMOOTH_MORE)
tmp_img = tmp_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
tmp_img = tmp_img.filter(ImageFilter.SMOOTH_MORE)
tmp_img = tmp_img.filter(ImageFilter.EDGE_ENHANCE_MORE)

image = np.reshape(tmp_img.getdata(), (64, 64, 1))

# Commented out because I don't think we need to show the image ever
#tmp_img.show()

img_preprocessor = ImagePreprocessing()
img_distortion = ImageAugmentation()
# Changing these parameters to match the initial models set up in
# shape_trainer.py and letter_trainer.py
# Renaming network to be more descriptive
# ------------- Shape Network ---------------------
network_shape = input_data(shape=[None, 64, 64, 1],
                     data_preprocessing=img_preprocessor,
                     data_augmentation=img_distortion)

# convolution 2
network_shape = conv_2d(network_shape, 32, 5, activation='relu')
# max pooling 2
network_shape = max_pool_2d(network_shape, 2)
# convolution 2
network_shape = conv_2d(network_shape, 48, 3, activation='relu')
# max pooling 2
network_shape = max_pool_2d(network_shape, 2)
# dropout
# network = dropout(network, 0.3)
# convolution 2
network_shape = conv_2d(network_shape, 64, 3, activation='relu')
# max pooling 2
network_shape = max_pool_2d(network_shape, 2)
# dropout
# network = dropout(network, 0.3)
# fully-connected
network_shape = fully_connected(network_shape, 512, activation='relu')
# fully-connected
network_shape = fully_connected(network_shape, 512, activation='relu')
# dropout
network_shape = dropout(network_shape, 0.75)

network_shape = fully_connected(network_shape, 13, activation='softmax')
network_shape = regression(network_shape, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.01)

# This path is hard coded and will need to be changed
# This is just a junk path right now
model_shape = tflearn.DNN(network_shape, tensorboard_verbose=2,
                    checkpoint_path='/shape_classifier.tfl.ckpt')
model_shape.load('shape_classifier.tfl')

# ------------- Letter Network ---------------------
# **Right now, parameters are not modified
network = input_data(shape=[None, 64, 64, 1],
	data_preprocessing=img_preprocessor,
	data_augmentation=img_distortion)

# convolution
network = conv_2d(network, 64, 4, activation='relu')

# max pooling
network = max_pool_2d(network, 2)

# convolution 2
network = conv_2d(network, 96, 4, activation='relu')

# convolution 3
network = conv_2d(network, 128, 4, activation='relu')

# max pooling 2
network = max_pool_2d(network, 2)

# fully-connected
network = fully_connected(network, 512, activation='relu')

# dropout
network = dropout(network, 0.5)

# fully-connected final
network = fully_connected(network, 26, activation='softmax')


network = regression(network, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.001)

# This path is hard coded and will need to be changed
# This is just a junk path right now
model_letter = tflearn.DNN(network_letter, tensorboard_verbose=2,
                    checkpoint_path='/letter_classifier.tfl.ckpt')
model_letter.load('letter_classifier.tfl')






# ------------- This is where we start predicting and outputting ---------------------
# Our predicted labels for both letter and shape
predicted_shape_label = model_shape.predict([image])
predicted_letter_label = model_letter.predict([image])

letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
shape_list = ['Circle', 'Semicircle', 'Quartercircle', 'Triangle', 'Square', 'Rectangle', 'Trapezoid', 'Pentagon',
              'Hexagon', 'Heptagon', 'Octagon', 'Star', 'Cross']

shape_index = np.argmax(predicted_shape_label)
letter_index = np.argmax(predicted_letter_label)
print("Predicted target shape is a " + shape_list[shape_index])
print("Predicted target letter is a " + letter_list[letter_index])