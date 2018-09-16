import target_gen

num_variations = 1

letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

shape_list = ['Circle', 'Semicircle', 'Quartercircle', 'Triangle', 'Square', 'Rectangle', 'Trapezoid', 'Pentagon', 'Hexagon', 'Heptagon', 'Octagon', 'Star', 'Cross']


counter = 0
for q in range(0, num_variations):
	for i in range(0, 26):
		for a in range(0, 13):
			tmp_img, tmp_label = target_gen.generate_image(requested_letter=letter_list[i], 
				requested_shape=shape_list[a], 
				requested_letter_color="White", 
				requested_shape_color="Black", 
				return_type = "set")
			counter += 1
