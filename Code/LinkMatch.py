#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is to help structuring a good program
# Created in 2013
# ######################################################################

# Below is the area for class definition
import math
from RoadNetworkV2 import *

class LinkMatch:
	def __init__(self):
		self.link_match_table = []
		self.load()
	
	def load(self):
		file_name = '../Res/LinkMatch.dict'
		
		file_stream = open(file_name,'r')
		for line in file_stream:
			direction_sign, latitude_str, longitude_str, link_name = line.split(';')
			latitude = float(latitude_str)
			longitude = float(longitude_str)
			self.link_match_table.append((direction_sign, latitude, longitude, link_name))
		file_stream.close()
		
		
		
	# para of geo_a/b should be in the format of latitude/longitude
	def match(self,geo_a, geo_b):
		direction_sign = get_direction_sign_with_geo(geo_a, geo_b)
		geo = [(geo_a[0] + geo_b[0]) / 2, (geo_a[1] + geo_b[1]) / 2]
		min_dis = 10**2 + 10**2
		link_name = None
		for link in self.link_match_table:
			dis = (geo[0] - link[1]) **2 + (geo[1] - link[2])**2 
			if direction_sign == link[0] and dis < min_dis:
				link_name = link[3]
				min_dis = dis
		return link_name
	
def main():

	# Here, your unit test code or main program
	geo_a = [39.9515592744,116.41934259]
	geo_b = [39.9527, 116.4287]
	print 'from:',geo_a,'to:', geo_b
	lm = LinkMatch()
	
	print 'match result is:', 	lm.match(geo_a,geo_b)

	
if __name__=='__main__':
	main()