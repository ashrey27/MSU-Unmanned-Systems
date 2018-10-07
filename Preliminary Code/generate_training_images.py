# This is the script that runs image_gen
import image_gen
import sys

# Number of items to generate
num_testing_images = 100

# The next two lines error in PyCharm, but not in command line
if sys.argv[1]:
	num_testing_images = int(sys.argv[1])


for i in range(0, num_testing_images):
	tmp_img, tmp_label = image_gen.generate_image(return_type = "shape")
	sys.stdout.write("Generating image %d/%d	 \r" % (i, num_testing_images) )
	sys.stdout.flush()
sys.stdout.write("Generating image %d/%d \n" % (i+1, num_testing_images) )
sys.stdout.write("Finished generating images\n")
