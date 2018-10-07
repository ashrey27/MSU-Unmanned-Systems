import tflearn
import numpy as np
from tflearn.data_utils import shuffle
from tflearn.data_utils import *
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import pickle
import target_gen
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import sys
np.set_printoptions(threshold=np.inf)
# load dataset of auvsi targets
# or generate them on demand here??
num_variations = 2
num_training_images = int(26*13)*num_variations
num_testing_images = 1000
#images = [None] * num_training_images
#labels = [None] * num_training_images
images_test = [None] * num_testing_images
labels_test = [None] * num_testing_images


letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

shape_list = ['Circle', 'Semicircle', 'Quartercircle', 'Triangle', 'Square', 'Rectangle', 'Trapezoid', 'Pentagon', 'Hexagon', 'Heptagon', 'Octagon', 'Star', 'Cross']


counter = 0
# load images
dataset_file = 'composites/shapes/'

print("loading image dataset")
x, label_set = image_preloader(dataset_file, image_shape=(64, 64), mode='folder', categorical_labels=True, normalize=False)

#images = [None] * len(x)

images = []
labels = []
images_test = []
labels_test = []

for i in range(0, len(x)):
	temp = x[i]
	temp = np.uint8(temp) 
	temp = Image.fromarray(temp)
	temp = temp.convert('L')
	enh_c = ImageEnhance.Contrast(temp)
	temp = enh_c.enhance(12.0)
	temp = temp.filter(ImageFilter.SMOOTH_MORE)
	temp = temp.filter(ImageFilter.SMOOTH_MORE)
	temp = temp.filter(ImageFilter.EDGE_ENHANCE_MORE)
	temp = temp.filter(ImageFilter.SMOOTH_MORE)
	temp = temp.filter(ImageFilter.EDGE_ENHANCE_MORE)
	tmp_arr = np.fromstring(temp.tobytes(), np.uint8)
	temp = tmp_arr.reshape(64,64,1)
	
	if not random.randrange(0,2):
		images_test.append( temp )
		labels_test.append( label_set[i] )
	else:
		images.append( temp )
		labels.append( label_set[i] )

# shuffle images
print("shuffling images")
images, labels = shuffle(images, labels)
images_test, labels_test = shuffle(images_test, labels_test)

# create preprocessor to normalize images
print("creating preprocessor")
img_preprocessor = ImagePreprocessing()
img_preprocessor.add_featurewise_zero_center()
img_preprocessor.add_featurewise_stdnorm()

# distort images
print("adding distortion")
img_distortion = ImageAugmentation()

# only flip left/right for shape training
img_distortion.add_random_flip_leftright()
img_distortion.add_random_blur(sigma_max=1.5)



###
### network architecture
###
print("setting up network")
network = input_data(shape=[None, 64, 64, 1], 
	data_preprocessing=img_preprocessor,
	data_augmentation=img_distortion)


# convolution 2
network = conv_2d(network, 32, 5, activation='relu')
# max pooling 2
network = max_pool_2d(network, 2)
# convolution 2
network = conv_2d(network, 48, 3, activation='relu')
# max pooling 2
network = max_pool_2d(network, 2)
# convolution 2
network = conv_2d(network, 64, 3, activation='relu')
# max pooling 2
network = max_pool_2d(network, 2)
# fully-connected
network = fully_connected(network, 512, activation='relu')
# fully-connected
network = fully_connected(network, 512, activation='relu')
# dropout
network = dropout(network, 0.75)

# fully-connected final
network = fully_connected(network, 13, activation='softmax')


network = regression(network, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.0001)


model = tflearn.DNN(network, tensorboard_verbose=2, checkpoint_path='/media/salvi/SSD480/checkpoints/shape_classifier.tfl.ckpt')

# if previously trained model is available use that
#model.load('shape_classifier.tfl')

model.fit(images, labels, n_epoch=300, shuffle=True, validation_set=(images_test, labels_test), show_metric=True, batch_size=256, snapshot_epoch=True, run_id='shape_classifier')

model.save("shape_classifier.tfl")
print("Network trained and saved as shape_classifier.tfl")

