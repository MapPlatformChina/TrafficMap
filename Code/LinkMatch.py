#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is to help structuring a good program
# Created in 2013
# ######################################################################

# Below is the area for class definition
import math
from RoadNetworkV2 import *
from PosCoordsUtl import *

MAX_DIS = 10**2 + 10**2

class LinkMatch:

	def __init__(self):
		# { grid: [[direction_sign, latitude, longitude, LCD, direction] ...] }
		# grid is in format of GRID_GRID, zoom level 
		self.link_match_table = {}
		self.zoom_level_of_grids = 15

		self.load()
	
	def load(self):
		file_name = '../Res/LinkMatch.dict'
		
		file_stream = open(file_name,'r')
		for line in file_stream:
			direction_sign, latitude_str, longitude_str, link_name = line.split(';')
			latitude = float(latitude_str)
			longitude = float(longitude_str)
			if link_name[-1] == '\n':
				link_name = link_name[0:-1]
			LCD = link_name[0:-2]
			direction = int(link_name[-1:])
			
			# PosCoordsUtl is longitude first
			grid = geocoordinates_to_grid((longitude,latitude), self.zoom_level_of_grids)
			
			key = ('%d_%d' % (grid[0],grid[1]))
			self.link_match_table[key] = [direction_sign, latitude, longitude, LCD, direction]
			
		file_stream.close()
		
		
		
	# para of geo_a/b should be in the format of latitude/longitude
	def match(self,geo_a, geo_b):
		direction_sign = get_direction_sign_with_geo(geo_a, geo_b)
		#geo = [(geo_a[0] + geo_b[0]) / 2, (geo_a[1] + geo_b[1]) / 2]
		geo = geo_b
		
		# PosCoordsUtl is longitude first
		grid = geocoordinates_to_grid((geo[1],geo[0]), self.zoom_level_of_grids)

		grid_start = grid
		grid_end = grid
		min_dis = MAX_DIS
		link_matched = ['?','?']
		while True:
			grid_start = [grid_start[0] - 1, grid_start[1] - 1]
			grid_end = [grid_end[0] + 1, grid_end[1] + 1]
			for index_lat in range(grid_start[0],grid_end[0] + 1):
				for index_lon in range(grid_start[1],grid_end[1] + 1):
					key = ('%d_%d' % (index_lat,index_lon))
					if not self.link_match_table.has_key(key):
						continue
					lat = self.link_match_table[key][1]
					lon = self.link_match_table[key][2]
					# calculate distance with latitude zoomed
					dis = ((geo[0] - lat)*2) **2 + (geo[1] - lon)**2 
					if direction_sign == self.link_match_table[key][0] and dis < min_dis:
						link_matched[0] = self.link_match_table[key][3]
						link_matched[1] = str(self.link_match_table[key][4])
						min_dis = dis
			if min_dis < MAX_DIS:
				return link_matched

def main():

	# Here, your unit test code or main program
	geo_a = [39.9515592744,116.41934259]
	geo_b = [39.9527, 116.4287]
	print 'from:',geo_a,'to:', geo_b
	lm = LinkMatch()
	
	print 'match result is:', 	lm.match(geo_a,geo_b)

	
if __name__=='__main__':
	main()