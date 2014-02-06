#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is one of traffic map utility component files
# Created in 2013
# ######################################################################
import math

# Below is the area for class definition

# Below is for helper functions

def geocoordinates_to_pixels(coords, zoom_level, image_size = 256):
	pic_size = 2 ** zoom_level * image_size
	x = coords[0] / 360.0 + 0.5						# convert longitude into pos x
	y = (coords[1] / 90.0 + 1) * math.pi / 4.0;		
	y = 1 - (math.log(math.tan(y)) / math.pi + 1) / 2.0		# convert Latitude into pos y
	return [round(x * pic_size), round(y * pic_size)]

def pixels_to_geocoordinates(pos, zoom_level, image_size=256):
	pic_size = 2 ** zoom_level * image_size
	longitude = (pos[0] / pic_size - 0.5) * 360.0
	latitude = math.pi * (1 - 2 * pos[1] / pic_size)
	latitude = math.atan(math.exp(latitude)) * 360 / math.pi - 90
	return [longitude,latitude]

def pixels_to_grid(pos, zoom_level, image_size = 256):
	pic_size = 2 ** zoom_level * image_size
	col = int(math.floor(pos[0] / image_size))
	row = int(math.floor(pos[1] / image_size))
	return [col,row]

def geocoordinates_to_grid(coords, zoom_level, image_size = 256):
	pos = geocoordinates_to_pixels(coords, zoom_level, image_size)
	return pixels_to_grid(pos, zoom_level, image_size)

#def get_right_center_pixels(grid, image_size = 256):
#	right_x = (grid[0] + 1) * image_size
#	center_y = grid[1] * image_size + image_size / 2
#	return [right_x, center_y]

def get_conner_grid( center_coords, zoom_level, image_size = 256 ):
	pic_size = [2 ** zoom_level * image_size, 2 ** zoom_level * image_size]
	center_pos = geocoordinates_to_pixels(center_coords, zoom_level, image_size)
	left_top_pos = [center_pos[0] - 1024/2 , center_pos[1] - 768/2]
	right_bottom_pos = [center_pos[0] + 1024/2 , center_pos[1] + 768/2]
	left_top_grid = pixels_to_grid(left_top_pos, zoom_level, image_size)
	right_bottom_grid = pixels_to_grid(right_bottom_pos, zoom_level, image_size)
	return (left_top_grid, right_bottom_grid)
	
# unit test code

def main():

	# Here, your unit test code or main program

	# Check parameters
	# argc = len(sys.argv)
	# if argc <= 2:
	#	print_help()
	#	exit()

	coords = [ 116.54774, 39.76751 ]
	
	print coords
	
	pos = geocoordinates_to_pixels(coords,13)
	print pos
	
	print pixels_to_grid(pos, 13)
	
	coords = pixels_to_geocoordinates(pos,13)
	print coords
	
			
if __name__=='__main__':
	main()