import tflearn
import numpy as np
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import pickle
import target_gen
from PIL import Image
from PIL import ImageFilter
# load dataset of auvsi targets
# or generate them on demand here??
num_variations = 1
num_training_images = int(26*13)*num_variations
num_testing_images = 32*num_variations
images = [None] * num_training_images
labels = [None] * num_training_images
images_test = [None] * num_testing_images
labels_test = [None] * num_testing_images


letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

shape_list = ['Circle', 'Semicircle', 'Quartercircle', 'Triangle', 'Square', 'Rectangle', 'Trapezoid', 'Pentagon', 'Hexagon', 'Heptagon', 'Octagon', 'Star', 'Cross']


counter = 0
for i in range(0, 26):
	for a in range(0, 13):
		tmp_img, tmp_label = target_gen.generate_image(requested_letter=letter_list[i], 
			requested_shape=shape_list[a], 
			requested_letter_color="White", 
			requested_shape_color="Black", 
			return_type = "set")
		
		for q in range(0, num_variations):
			tmp_img_2 = tmp_img
			tmp_img_2 = tmp_img_2.filter(ImageFilter.FIND_EDGES)
			tmp_img_2 = tmp_img_2.filter(ImageFilter.SMOOTH)
			tmp_img_2 = tmp_img_2.filter(ImageFilter.SMOOTH_MORE)
			tmp_img_2 = tmp_img_2.filter(ImageFilter.FIND_EDGES)
			tmp_img_2 = tmp_img_2.convert('L')
			tmp_img_2 = tmp_img_2.filter(ImageFilter.EDGE_ENHANCE_MORE)
			images[counter] = np.reshape(tmp_img_2.getdata(), (64, 64, -1))
			#labels[counter] = np.reshape(tmp_label, (-1))
			#labels[counter] = tflearn.data_utils.to_categorical(tmp_label,338)
			labels[counter] = tmp_label			
			#print(str(labels[counter]))
			ls_str = 'letter ' + letter_list[i]
			print(ls_str + ", shape " + shape_list[a] + ' variation ' + str(q))

			counter += 1
		#tmp_img_2.show()
labels_test = 
for i in range(0, num_testing_images):
	tmp_img, tmp_label = target_gen.generate_image(return_type = "set")
	tmp_img = tmp_img.filter(ImageFilter.FIND_EDGES)
	tmp_img = tmp_img.filter(ImageFilter.SMOOTH)
	tmp_img = tmp_img.filter(ImageFilter.SMOOTH_MORE)
	tmp_img = tmp_img.filter(ImageFilter.FIND_EDGES)
	tmp_img = tmp_img.convert('L')
	tmp_img = tmp_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
	images_test[i] = np.reshape(tmp_img.getdata(), (64, 64, -1))
	#labels_test[i] = tflearn.data_utils.to_categorical([tmp_label],338)
	#labels_test[i] = np.reshape(tmp_label, (-1))
	labels_test[i] = tmp_label
	print("generating testing image " + str(i+1) + "/" + str(num_testing_images))
#tmp_img.show()
#np.reshape(labels, (338,338))
#np.reshape(labels_test, (num_testing_images,338))

print(labels)

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

img_distortion.add_random_rotation(max_angle=360)
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
network = fully_connected(network, 338, activation='softmax')


network = regression(network, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.001)


model = tflearn.DNN(network, tensorboard_verbose=2, checkpoint_path='/media/salvi/E4D81381D81350E2/checkpoints/msuus-target-classifier.tfl.ckpt')

# if previously trained model is available use that
#model.load('msuus-target-classifier.tfl')

model.fit(images, labels, n_epoch=100, shuffle=True, validation_set=(images_test, labels_test), show_metric=True, batch_size=32, snapshot_epoch=True, run_id='msuus-target-classifier')

model.save("msuus-target-classifier.tfl")
print("Network trained and saved as msuus-target-classifier.tfl")

