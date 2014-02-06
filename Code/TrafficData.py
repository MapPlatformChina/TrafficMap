#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is to help structuring a good program
# Created in 2013
# ######################################################################

from RoadNetwork import *
from CSVData import *

# Below is the area for class definition

class TrafficLink(Link):
	def __init__(self, link):
		Link.__init__(self, link.point_a, link.point_b, link.direction)
		self.traffic_speed = 50
		self.traffic_code = 2049			# 2049:Fast 2050:Slow 2051: Jam 
	
	def get_speed(self):
		return self.traffic_speed
	
	def get_code(self):
		return self.traffic_code
	
	def set_speed(self, speed):
		self.traffic_speed = speed
	
	def set_code(self,code):
		self.traffic_code = code
	
	def get_data(self):
		return [ self.point_a.longitude, self.point_a.latitude, 
					self.point_b.longitude, self.point_b.latitude, 
					self.direction, self.traffic_speed, self.traffic_code] 

class TrafficData:
	def __init__(self):
		self.traffic_link_set = LinkSet()
		self.dict_link_set = LinkSet()
	
	def reset(self):
		self.dict_link_set = LinkSet()
	
	def load_dictionary(self):
		self.dict_link_set.reset()

		# load from below file
		fn_point = '../Res/POINTS.DAT'			# get coordinates and LCD from this file
		fn_poffset = '../Res/POFFSETS.DAT'		# get connection and direction from this file
		seperator = ';'
		
		# load data into point_data and poffset_data
		print 'load',fn_point,'...',
		point_data = CSVData(fn_point,seperator)
		print 'done!'
		print 'load',fn_poffset,'...',
		poffset_data = CSVData(fn_poffset,seperator)
		print 'done!'

		self.form_dictionary(point_data, poffset_data)
		

	def form_dictionary(self,point_data, poffset_data):
		# filter data
		indexes = ('LCD', 'XCOORD', 'YCOORD')
		point_data_filtered = point_data.get_data(indexes)

		indexes = ('LCD', 'NEG_OFF_LCD', 'POS_OFF_LCD')
		poffset_data_filtered = poffset_data.get_data(indexes)

		# build point dictionary
		point_set = self.convert_csvdata_to_point_array(point_data_filtered)

		for data in poffset_data_filtered:
			point_a = point_set.search(data[0])
			if len(data[1]) > 0:
				point_b = point_set.search(data[1])
				self.dict_link_set.add_link(Link(point_a,point_b, 0))
			if len(data[2]) > 0:
				point_b = point_set.search(data[2])
				self.dict_link_set.add_link(Link(point_a,point_b, 1))
		

	def convert_csvdata_to_point_array(self,point_data_filtered):
		point_set = PointSet()
		
		for data in point_data_filtered:
			point_set.add_point(Point(data[0],float(data[1])/100000,float(data[2])/100000))
		return point_set

	def load_traffic(self, traffic_file_name):
		
		print 'load data from:',traffic_file_name,'...',
	
		self.traffic_link_set.reset()
		
		seperator = ','
		csv = CSVData(traffic_file_name, seperator)
		indexes = ('primary_location', 'direction', 'speed_limit_advice', 'event_code')
		data_set = csv.get_data(indexes)
		
		for data in data_set:
			link = self.dict_link_set.search(data[0],int(data[1]))
			if link == None:
				pass
			else:
				tl = TrafficLink(link)
				tl.set_speed(float(data[2]))
				tl.set_code(int(data[3]))
				self.traffic_link_set.add_link(tl)
		
		print 'done!'
	
	def get_size(self):
		return self.traffic_link_set.get_size()
	
	def get_traffic(self,index):
		return self.traffic_link_set.get_link(index)
	
	def get_data_to_draw(self, coords_box):
		num = self.traffic_link_set.get_size()
		data_to_draw = []
		for i in range(0,num):
			link = self.traffic_link_set.get_link(i)
			if self.point_in_box(link.point_a, coords_box) or self.point_in_box(link.point_b, coords_box):
				data_to_draw.append(link.get_data())
		return data_to_draw
	
	def point_in_box(self, point, box):
		if point.longitude >= box[0] and point.longitude <= box[2] and point.latitude >= box[3] and point.latitude <= box[1]:
			return True
		return False
		
def main():

	# Here, your unit test code or main program
	traffic_data = TrafficData()
	traffic_data.load_dictionary()
	print traffic_data.dict_link_set.get_size()
	print traffic_data.dict_link_set.get_link(0).get_data()

	traffic_data.load_traffic('data.csv')
	print traffic_data.traffic_link_set.get_size()
	print traffic_data.traffic_link_set.get_link(0).get_data()
		
if __name__=='__main__':
	main()