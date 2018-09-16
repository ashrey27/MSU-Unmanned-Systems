# This is the script that runs image_gen
## THIS FILE MUST BE RUN IN PYTHON 2 BECAUSE OF IMAGE_GEN##
import image_gen
import sys

# Number of items to generate
num_testing_images = 50

# The next two lines error in PyCharm, but not in command line
# if sys.argv[1]:
# if len(sys.argv) > 0:
# 	num_testing_images = int(sys.argv[1])

tmp_label_list = []
for i in range(0, num_testing_images):
	#tmp_img, tmp_label = image_gen.generate_image(return_type = "shape") ## STABLE LINE

	tmp_img, tmp_label = image_gen.generate_image(file_save=True, save_path='E:/US/US_Images/', return_type="shape")
	tmp_label_list.append(tmp_label)
	sys.stdout.write("Generating image %d/%d	 \r" % (i, num_testing_images) )
	sys.stdout.flush()	# Clears the output
print(tmp_label_list)
sys.stdout.write("Generating image %d/%d \n" % (i+1, num_testing_images) )
sys.stdout.write("Finished generating images\n")
