#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is to help structuring a good program
# Created in 2013
# ######################################################################

# Below is the area for class definition

class RoadNetwork:
	def __init__(self, roads = None):
		self.roads = roads
	
	def get_size(self):
		return len(self.roads)
	
	def add_road(self, road):
		self.roads.append(road)

class Road:
	def __init__(self, name = ''):
		self.road_segs = []
		self.road_name = name
	
	def set_name(self,name):
		self.road_name = name
	
	def add_seg(self,roadseg):
		self.road_segs.append(roadseg)
	
	def reset(self):
		self.road_segs = []
		self.road_name = ''
	
	def get_size(self):
		return len(self.road_segs)
		
	def get_seg(self,index):
		return self.road_segs[index]

		
class RoadSeg:
	def __init__(self, links = None, urban = True):
		self.links = links
		self.urban = urban
	
	def add_link(self,link):
		self.links.append(link)
	
	def reset(self):
		self.links = []
		self.urban = True
	
	def get_size(self):
		return len(self.links)
		
	def get_link(self,index):
		return self.links[index]

class LinkSet:
	def __init__(self):
		self.link_set = []
	
	def reset(self):
		self.link_set = []
	
	def add_link(self, link):
		self.link_set.append(link)
	
	def get_size(self):
		return len(self.link_set)
	
	def get_link(self,index):
		return self.link_set[index]
	
	def search(self, LCD, direction):
		for link in self.link_set:
			if link.match(LCD,direction):
				return link
		return None

		
class Link:
	def __init__(self, point_a, point_b, direction):
		self.point_a = point_a
		self.point_b = point_b
		self.direction = direction
	
	def match(self, LCD, direction):
		if self.point_a.get_LCD() == LCD and self.direction == direction:
			return True
		return False
	
	def get_data(self):
		return [ self.point_a.LCD, self.point_b.LCD,
					self.point_a.longitude, self.point_a.latitude, 
					self.point_b.longitude, self.point_b.latitude, 
					self.direction] 

class PointSet:
	def __init__(self):
		self.point_set = []
	
	def reset(self):
		self.point_set = []
	
	def add_point(self, point):
		self.point_set.append(point)
	
	def get_size(self):
		return len(self.point_set)
	
	def get_point(self,index):
		return self.point_set[index]
	
	def search(self, LCD):
		for point in self.point_set:
			if point.LCD == LCD:
				return point
		
class Point:
	def __init__(self, LCD, longitude, latitude):
		self.longitude = longitude
		self.latitude = latitude
		self.LCD = LCD

	def get_longitude(self):
		return self.longitude

	def get_latitude(self):
		return self.latitude
	
	def get_LCD(self):
		return self.LCD

	
		
		
def main():

	# Here, your unit test code or main program
		pass
		
if __name__=='__main__':
	main()