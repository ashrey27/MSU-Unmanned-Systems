import target_gen
import sys
import argparse

parser = argparse.ArgumentParser(description='request specific shape,letter,colors')
parser.add_argument('-s', help='generate a specific shape')
parser.add_argument('-l', help='generate a specific letter')
parser.add_argument('-sc', help='generate a specific shape color')
parser.add_argument('-lc', help='generate a specific letter color')

args = parser.parse_args()

s = l = sc = lc = None

if (args.s):
	s = args.s
if (args.l):
	l = args.l
if (args.sc):
	sc = args.sc
if (args.lc):
	lc = args.lc

print(target_gen.generate_image(requested_shape=s, requested_letter=l, requested_shape_color=sc, requested_letter_color=lc))

