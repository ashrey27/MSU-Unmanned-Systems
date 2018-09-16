from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import target_gen
import random

from six.moves import xrange	# pylint: disable=redefined-builtin
import tensorflow as tf

# Process images of this size. Note that this differs from the original CIFAR
# image size of 32 x 32. If one alters this number, then the entire model
# architecture will change and any model would need to be retrained.
IMAGE_SIZE = 64

num_classes = 40
NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = 5000
NUM_EXAMPLES_PER_EPOCH_FOR_EVAL = 10000


def get_mynet_input(key):

	class mynetRecord(object):
		pass
	result = mynetRecord()

	label_bytes = 4
	result.height = 64
	result.width = 64
	result.depth = 4

	print(key)
	if (key[0] == 'shape'):
		target = target_gen.generate_image(requested_shape=key[1],requested_label=key[0])
	elif (key[0] == 'letter'):
		target = target_gen.generate_image(requested_letter=key[1],requested_label=key[0])
	result.label = target.label
	print("label: " + str(result.label))
	record_bytes = tf.decode_raw(target.image, tf.uint8)

	depth_major = tf.reshape(record_bytes,[result.depth, result.height, result.width])
	result.uint8image = tf.transpose(depth_major, [1, 2, 0])

	return result


def _generate_image_and_label_batch(image, label, min_queue_examples, batch_size, shuffle):
	num_preprocess_threads = 16
	if shuffle:
		images, label_batch = tf.train.shuffle_batch(
				[image, label],
				batch_size=batch_size,
				num_threads=num_preprocess_threads,
				capacity=min_queue_examples + 3 * batch_size,
				min_after_dequeue=min_queue_examples)
	else:
		images, label_batch = tf.train.batch(
				[image, label],
				batch_size=batch_size,
				num_threads=num_preprocess_threads,
				capacity=min_queue_examples + 3 * batch_size)

	# Display the training images in the visualizer.
	tf.image_summary('images', images)

	return images, tf.reshape(label_batch, [batch_size])


def distorted_inputs(data_dir, batch_size):
	letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        shape_list = ['Circle', 'Semicircle', 'Quartercircle', 'Triangle', 'Square', 'Rectangle', 'Trapezoid', 'Pentagon', 'Hexagon', 'Heptagon', 'Octagon', 'Star', 'Cross']
	key_list = ['letter','shape']
	key_index = random.randint(0,1)
	if (key_index == 0):
		key = [key_list[key_index],letter_list[random.randint(0,25)]]
	elif (key_index == 1):
		key = [key_list[key_index],shape_list[random.randint(0,13)]]
	
	read_input = get_mynet_input(key)
	reshaped_image = tf.cast(read_input.uint8image, tf.float32)

	height = IMAGE_SIZE
	width = IMAGE_SIZE

	# Image processing for training the network. Note the many random
	# distortions applied to the image.

	# Randomly crop a [height, width] section of the image.
	distorted_image = tf.random_crop(reshaped_image, [height, width, 3])

	# Randomly flip the image horizontally.
	distorted_image = tf.image.random_flip_left_right(distorted_image)

	# Because these operations are not commutative, consider randomizing
	# the order their operation.
	distorted_image = tf.image.random_brightness(distorted_image,
																							 max_delta=63)
	distorted_image = tf.image.random_contrast(distorted_image,
																						 lower=0.2, upper=1.8)

	# Subtract off the mean and divide by the variance of the pixels.
	float_image = tf.image.per_image_whitening(distorted_image)

	# Ensure that the random shuffling has good mixing properties.
	min_fraction_of_examples_in_queue = 0.4
	min_queue_examples = int(NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN *
													 min_fraction_of_examples_in_queue)
	print ('Filling queue with %d CIFAR images before starting to train. '
				 'This will take a few minutes.' % min_queue_examples)

	# Generate a batch of images and labels by building up a queue of examples.
	return _generate_image_and_label_batch(float_image, read_input.label,
																				 min_queue_examples, batch_size,
																				 shuffle=True)


def inputs(eval_data, data_dir, batch_size):
	"""Construct input for CIFAR evaluation using the Reader ops.
	Args:
		eval_data: bool, indicating if one should use the train or eval data set.
		data_dir: Path to the CIFAR-10 data directory.
		batch_size: Number of images per batch.
	Returns:
		images: Images. 4D tensor of [batch_size, IMAGE_SIZE, IMAGE_SIZE, 3] size.
		labels: Labels. 1D tensor of [batch_size] size.
	"""
	if not eval_data:
		num_examples_per_epoch = NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN
	else:
		num_examples_per_epoch = NUM_EXAMPLES_PER_EPOCH_FOR_EVAL
	key = ["shape", "Star"]
	read_input = get_mynet_input(key)
	reshaped_image = tf.cast(read_input.uint8image, tf.float32)

	height = IMAGE_SIZE
	width = IMAGE_SIZE

	# Image processing for evaluation.
	# Crop the central [height, width] of the image.
	resized_image = tf.image.resize_image_with_crop_or_pad(reshaped_image, width, height)

	# Subtract off the mean and divide by the variance of the pixels.
	float_image = tf.image.per_image_whitening(resized_image)

	# Ensure that the random shuffling has good mixing properties.
	min_fraction_of_examples_in_queue = 0.4
	min_queue_examples = int(num_examples_per_epoch * min_fraction_of_examples_in_queue)

	# Generate a batch of images and labels by building up a queue of examples.
	return _generate_image_and_label_batch(float_image, read_input.label, min_queue_examples, batch_size, shuffle=False)
