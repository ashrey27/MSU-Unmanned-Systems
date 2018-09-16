import tflearn
import numpy as np
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import pickle
import image_gen
from PIL import Image
from PIL import ImageFilter
# load dataset of auvsi targets
# or generate them on demand here??

# Variables used for looping
num_variations = 1
num_training_images = int(26*13)*num_variations
num_testing_images = 32*num_variations
images = [None] * num_training_images
labels = [None] * num_training_images
images_test = [None] * num_testing_images
labels_test = [None] * num_testing_images


letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

shape_list = ['Circle', 'Semicircle', 'Quartercircle', 'Triangle', 'Square', 'Rectangle', 'Trapezoid', 'Pentagon', 'Hexagon', 'Heptagon', 'Octagon', 'Star', 'Cross']

# Holds onto the actual number of going through the loops
counter = 0

#Loops through a set of variations
for variation in range(0, num_variations):
	# Loops through the letters of the alphabet
	for letter_index in range(0, 26):
		# Loops through the shapes
		for shape_index in range(0, 13):
			# Generating image from target_gen
			# Doesn't request black and white, because converting from colors is more realistic
			tmp_img, tmp_label = image_gen.generate_image(requested_letter=letter_list[letter_index],
				requested_shape=shape_list[shape_index],
				#requested_letter_color="White", 
				#requested_shape_color="Black", 
				return_type = "letter")
		
			tmp_img_2 = tmp_img
			tmp_img_2 = tmp_img_2.filter(ImageFilter.SMOOTH_MORE) # Image processing
			tmp_img_2 = tmp_img_2.convert('L')	# Converts to black and white
			tmp_img_2 = tmp_img_2.filter(ImageFilter.EDGE_ENHANCE_MORE)
			images[counter] = np.reshape(tmp_img_2.getdata(), (64, 64, -1)) # Stores pixel data in 64x64 grid into images[]??
			#labels[counter] = np.reshape(tmp_label, (-1))
			#labels[counter] = tflearn.data_utils.to_categorical(tmp_label,338)
			labels[counter] = np.zeros(26) # np.zeros generates 0's and throws them into labels
			labels[counter][tmp_label] = 1	# Change a value in 2d list to 1
			#print(str(labels[counter]))
			ls_str = 'letter ' + letter_list[letter_index]
			print(ls_str + ", shape " + shape_list[shape_index] + ' variation ' + str(variation))

			counter += 1
#tmp_img_2.show()


for i in range(0, num_testing_images):
	tmp_img, tmp_label = image_gen.generate_image(return_type = "letter")
	tmp_img = tmp_img.filter(ImageFilter.SMOOTH_MORE)
	tmp_img = tmp_img.convert('L')
	tmp_img = tmp_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
	images_test[i] = np.reshape(tmp_img.getdata(), (64, 64, -1))
	#labels_test[i] = tflearn.data_utils.to_categorical([tmp_label],338)
	#labels_test[i] = np.reshape(tmp_label, (-1))
	labels_test[i] = np.zeros(26)
	labels_test[i][tmp_label] = 1
	print("generating testing image " + str(i+1) + "/" + str(num_testing_images))
#tmp_img.show()
#np.reshape(labels, (338,338))
#np.reshape(labels_test, (num_testing_images,338))

#print(labels)

# shuffle images
images, labels = shuffle(images, labels)
images_test, labels_test = shuffle(images_test, labels_test)

# create preprocessor to normalize images
img_preprocessor = ImagePreprocessing()
img_preprocessor.add_featurewise_zero_center()
img_preprocessor.add_featurewise_stdnorm()

# distort images
img_distortion = ImageAugmentation()

# only flip left/right for shape training
#img_distortion.add_random_flip_leftright()

img_distortion.add_random_rotation(max_angle=20)
img_distortion.add_random_blur(sigma_max=1.)



###
### network architecture
###

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

# This line is going to need to be changed, since it's locally set up
model = tflearn.DNN(network, tensorboard_verbose=2, checkpoint_path='/media/salvi/E4D81381D81350E2/checkpoints/letter_classifier.tfl.ckpt')

# if previously trained model is available use that
#model.load('msuus-target-classifier.tfl')

# Figure out this line of code
model.fit(images, labels, n_epoch=100, shuffle=True, validation_set=(images_test, labels_test), show_metric=True, batch_size=32, snapshot_epoch=True, run_id='letter_classifier')

model.save("letter_classifier.tfl")
print("Network trained and saved as letter_classifier.tfl")

