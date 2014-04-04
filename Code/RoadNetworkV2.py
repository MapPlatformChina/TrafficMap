#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is to help structuring a good program
# Created in 2013
# ######################################################################

# Below is the area for class definition
from CSVData import *

class RoadNetwork:
	def __init__(self, roads = []):
		self.roads = roads
	
	def get_size(self):
		return len(self.roads)
	
	def add_road(self, road):
		self.roads.append(road)
	
	def get_road(self, LCD):
		for road in self.roads:
			if road.LCD == LCD:
				return road
		return None;

class Road:
	def __init__(self, LCD, name = ''):
		self.road_segs = RoadSegSet()
		self.links = LinkSet()
		self.road_name = name
		self.LCD = LCD
	
	def set_name(self,name):
		self.road_name = name

	def add_link(self,link):
		self.links.add_link(link)

	def get_link(self,LCD,direction):
		return self.links.get_link(LCD,direction)

	def add_seg(self,seg):
		self.road_segs.add_seg(seg)
		
	def get_seg(self,LCD):
		return self.road_segs.get_seg(LCD)
		
class RoadSegSet:
	def __init__(self):
		self.road_seg_set = []
	
	def reset(self):
		self.road_seg_set = []
	
	def add_seg(self, seg):
		self.road_seg_set.append(seg)
	
	def get_size(self):
		return len(self.road_seg_set)
	
	def get_seg(self, LCD):
		for seg in self.road_seg_set:
			if seg.LCD == LCD:
				return seg
		return None
	
class RoadSeg:
	def __init__(self, LCD, links = None, urban = True):
		self.links = links
		self.urban = urban
		self.LCD = LCD
	
	def add_link(self,link):
		self.links.append(link)
	
	def reset(self):
		self.links = []
		self.urban = True
	
	def get_size(self):
		return len(self.links)
		
	def get_link(self,LCD):
		for link in self.links:
			if link.LCD == LCD:
				return link
		return None;

class LinkSet:
	def __init__(self):
		self.link_set = []
	
	def reset(self):
		self.link_set = []
	
	def add_link(self, link):
		self.link_set.append(link)
	
	def get_size(self):
		return len(self.link_set)
	
	def get_link(self, LCD, direction):
		for link in self.link_set:
			if link.match(LCD,direction):
				return link
		return None
	
	def get_link_by_seg(self, seg_lcd):
		link_set = LinkSet()
		for link in self.link_set:
			if link.point_a.seg_lcd == seg_lcd:
				link_set.add_link(link)
		return link_set

	def get_link_by_road(self, road_lcd):
		link_set = LinkSet()
		for link in self.link_set:
			if link.point_a.road_lcd == road_lcd:
				link_set.add_link(link)
		return link_set

		
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
	def __init__(self, LCD, longitude, latitude, seg_lcd='',road_lcd =''):
		self.longitude = longitude
		self.latitude = latitude
		self.LCD = LCD
		self.seg_lcd = seg_lcd
		self.road_lcd = road_lcd

	def get_longitude(self):
		return self.longitude

	def get_latitude(self):
		return self.latitude
	
	def get_LCD(self):
		return self.LCD

class NameDictionary:
	def __init__(self):
		self.names = [];
	
	def add_name(self,name_id,name):
		self.names.append((name_id,name))
	
	def search(self, name_id):
		for name in self.names:
			if name[0] == name_id:
				return name[1]
		return ''

class RoadNetworkDictionary:
	def __init__(self):
		self.road_network = RoadNetwork()
		self.road_data_file = '../Res/ROADS.DAT'
		self.seg_data_file = '../Res/SEGMENTS.DAT'
		self.seg_off_data_file = '../Res/SOFFSETS.DAT'
		self.point_data_file = '../Res/POINTS.DAT'
		self.point_off_data_file = '../Res/POFFSETS.DAT'
		self.name_data_file = '../Res/NAMES.DAT'
		self.name_dict = NameDictionary()
		self.link_set = LinkSet();
		
		self.seperator = ';'
		
		self.load_name_dict()
		self.load_link_dict()
	
	def load_name_dict(self):
		print 'Load',self.name_data_file,'...',
		name_data = CSVData(self.name_data_file, self.seperator);
		indexes = ('NID', 'NAME')
		name_data_filtered = name_data.get_data(indexes)
		print 'Done!'
		for name in name_data_filtered:
			self.name_dict.add_name(name[0],name[1])
	
	def load_road_data(self):
		print 'Load',self.road_data_file,'...',
		road_data = CSVData(self.road_data_file, self.seperator)
		indexes = ('LCD', 'RNID')
		road_data_filtered = road_data.get_data(indexes)
		print 'Done!'
		
		print 'Parsing data ...',
		for road in road_data_filtered:
			road_id = road[0]
			road_name = self.name_dict.search(road[1])
			road_obj = Road(road_id,road_name)
			links = self.link_set.get_link_by_road(road_id);
			road_obj.links = links
			self.road_network.add_road(road_obj)
		print 'Done!'
		

	def load_segment_data(self):
		print 'Load',self.seg_data_file,'...',
		seg_data = CSVData(self.seg_data_file, self.seperator)
		indexes = ('LCD', 'ROA_LCD')
		seg_data_filtered = seg_data.get_data(indexes)
		print 'Done!'
		
		print 'Parsing data ...',
		for seg in seg_data_filtered:
			seg_id = seg[0]
			road_id = seg[1]
			road_seg_obj = RoadSeg(seg_id)
			link_set = self.link_set.get_link_by_seg(seg_id)
			for link in link_set.link_set:
				road_seg_obj.add_link(link)
			self.road_network.get_road(road_id).add_seg(road_seg_obj);
		print 'Done!'

	def load_link_dict(self):
		print 'Load',self.point_data_file,'...',
		point_data = CSVData(self.point_data_file, self.seperator)
		indexes = ('LCD', 'XCOORD', 'YCOORD','SEG_LCD', 'ROA_LCD')
		point_data_filtered = point_data.get_data(indexes)
		print 'Done!'

		print 'Parsing data ...',
		point_set = PointSet()
		for point_data_item in point_data_filtered:
			point_obj = Point(point_data_item[0], float(point_data_item[1])/100000,
								float(point_data_item[2])/100000,point_data_item[3], point_data_item[4])
			point_set.add_point(point_obj)
		print 'Done!'

		print 'Load',self.point_off_data_file,'...',
		point_off_data = CSVData(self.point_off_data_file, self.seperator)
		indexes = ('LCD', 'NEG_OFF_LCD', 'POS_OFF_LCD')
		point_off_data_filtered = point_off_data.get_data(indexes)
		print 'Done!'

		print 'Parsing data ...',
		for off_data in point_off_data_filtered:
			point_a = point_set.search(off_data[0])
			if len(off_data[1]) > 0:
				point_b = point_set.search(off_data[1])
				link_obj = Link(point_a,point_b, 0)
				self.link_set.add_link(link_obj);
			if len(off_data[2]) > 0:
				point_b = point_set.search(off_data[2])
				link_obj = Link(point_a,point_b, 1)
				self.link_set.add_link(link_obj);
		print 'Done!'
		
		
def main():

	# Here, your unit test code or main program
	road_dict = RoadNetworkDictionary()
	road_dict.load_road_data()
	road_dict.load_segment_data()
	print road_dict.road_network.get_size(),'roads loaded'
	
	#file_handle = open("LinkList.txt", "wb")

	for road in road_dict.road_network.roads:
		for seg in road.road_segs.road_seg_set:
			for link in seg.links.link_set:
				outputstr = ('%s;%s;%s;%s;%d;%s;%f;%f;%f;%f\n' % (road.LCD, seg.LCD, 
									link.point_a.LCD, link.point_b.LCD, link.direction, road.road_name,
						link.point_a.longitude, link.point_a.latitude, 
						link.point_b.longitude, link.point_b.latitude) )
				print outputstr
				#file_handle.write(outputstr)
						
	#file_handle.close()
	
	print 'List is writen into LinkList.txt!\nFeel free to check out'
	
if __name__=='__main__':
	main()