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
	
	# if seg_lcd present, road_lcd MUST NOT be None
	# if road_lcd present, seg_lcd can be None
	def add_link(self,link):
		# use point a as reference
		seg_lcd = link.point_a.seg_lcd
		road_lcd = link.point_a.road_lcd
		
		if seg_lcd == None:
			# if link doesn't have seg, add link to road directly
			for road in self.roads:
				if road.LCD == road_lcd:
					road.add_link(link)
					return True
		else:
			for road in self.roads:
				if road.LCD == road_lcd:
					# if seg found, add link
					for seg in road.segs:
						if seg.LCD == seg_lcd:
							seg.add_link(link)
							return True
					# if seg not exist, add seg and link
					seg_obj = RoadSeg(seg_lcd)
					seg_obj.add_link(link)
					road.add_seg(seg_obj)
					return True
		return False
		

class Road:
	def __init__(self, LCD, name = ''):
		self.segs = []
		self.links = []
		self.name = name
		self.LCD = LCD
	
	def set_name(self,name):
		self.name = name

	def add_link(self,link):
		self.links.append(link)

	def get_link(self,LCD,direction):
		for link in self.links:
			if link.LCD == LCD and link.direction == direction:
				return link
		return None

	def add_seg(self,seg):
		self.segs.append(seg)
		
	def get_seg(self,LCD):
		for seg in self.segs:
			if seg.LCD == LCD:
				return seg
		return None
		
class RoadSeg:
	def __init__(self, LCD, links = [], urban = True):
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
		
	def get_link(self,LCD,direction):
		for link in self.links:
			if link.get_LCD() == LCD and link.direction == direction:
				return link
		return None;

class Link:
	def __init__(self, point_a, point_b, direction, seg = None, road=None):
		self.point_a = point_a
		self.point_b = point_b
		self.direction = direction
		self.seg_lcd = seg
		self.road_lcd = road
	
	def get_LCD(self):
		return self.point_a.LCD
	
	def get_data(self):
		return [ self.point_a.LCD, self.point_b.LCD,
					self.point_a.longitude, self.point_a.latitude, 
					self.point_b.longitude, self.point_b.latitude, 
					self.direction] 

class Point:
	def __init__(self, LCD, longitude, latitude, seg_lcd=None,road_lcd =None, link_name =None):
		self.longitude = longitude
		self.latitude = latitude
		self.LCD = LCD
		self.seg_lcd = seg_lcd
		self.road_lcd = road_lcd
		self.link_name = link_name

		
class PointDict:
	def __init__(self):
		self.points = [];
	
	def add_point(self,point):
		self.points.append(point)
	
	def get_point(self, LCD):
		for point in self.points:
			if point.LCD == LCD:
				return point
		return None
		
class NameDict:
	def __init__(self):
		self.names = [];
	
	def add_name(self,name_id,name):
		self.names.append((name_id,name))
	
	def get_name(self, name_id):
		for name in self.names:
			if name[0] == name_id:
				return name[1]
		return None

class SegDict:
	def __init__(self):
		self.segs = [];
	
	def add_seg(self,LCD, road_LCD):
		self.segs.append((LCD,road_LCD))
	
	def get_road_lcd(self, LCD):
		for seg in self.segs:
			if seg[0] == LCD:
				return seg[1]
		return None
		
class RoadNetworkDict:
	def __init__(self):
		# define resources files
		self.road_data_file = '../Res/ROADS.DAT'
		self.seg_data_file = '../Res/SEGMENTS.DAT'
		self.seg_off_data_file = '../Res/SOFFSETS.DAT'
		self.point_data_file = '../Res/POINTS.DAT'
		self.point_off_data_file = '../Res/POFFSETS.DAT'
		self.name_data_file = '../Res/NAMES.DAT'
		
		# initiate var used for CSVData
		self.seperator = ';'

		# initiate name dict and load it
		self.name_dict = NameDict()
		self.load_name_dict()

		# initiate seg dict and load it
		self.seg_dict = SegDict()
		self.load_seg_dict()
		
		# initiate point dict and load it
		self.point_dict = PointDict()
		self.load_point_dict()

		# initiate road network and load roads
		self.road_network = RoadNetwork()		
		self.load_road_data()
		
		self.load_link_data()
		

	def load_name_dict(self):
		print 'Load',self.name_data_file,'...',
		name_data = CSVData(self.name_data_file, self.seperator);
		indexes = ('NID', 'NAME')
		name_data_filtered = name_data.get_data(indexes)
		for name in name_data_filtered:
			self.name_dict.add_name(name[0],name[1])
		print 'Done!'

	def load_seg_dict(self):
		print 'Load',self.seg_data_file,'...',
		seg_data = CSVData(self.seg_data_file, self.seperator)
		indexes = ('LCD', 'ROA_LCD')
		seg_data_filtered = seg_data.get_data(indexes)
		for seg in seg_data_filtered:
			self.seg_dict.add_seg(seg[0],seg[1])
		print 'Done!'

	def load_point_dict(self):
		print 'Load',self.point_data_file,'...',
		point_data = CSVData(self.point_data_file, self.seperator)
		indexes = ('LCD', 'XCOORD', 'YCOORD','SEG_LCD', 'ROA_LCD', 'RNID')
		point_data_filtered = point_data.get_data(indexes)
		for point_data_item in point_data_filtered:
			point_obj = Point(point_data_item[0], 
					float(point_data_item[1])/100000,float(point_data_item[2])/100000,
					point_data_item[3], point_data_item[4], self.name_dict.get_name(point_data_item[5]))
			self.point_dict.add_point(point_obj)
		print 'Done!'
		
	def load_road_data(self):
		print 'Load',self.road_data_file,'...',
		road_data = CSVData(self.road_data_file, self.seperator)
		indexes = ('LCD', 'RNID')
		road_data_filtered = road_data.get_data(indexes)
		for road in road_data_filtered:
			road_id = road[0]
			road_name = self.name_dict.get_name(road[1])
			road_obj = Road(road_id,road_name)
			self.road_network.add_road(road_obj)
		print 'Done!'
		
	def load_link_data(self):
		print 'Load',self.point_off_data_file,'...',
		point_off_data = CSVData(self.point_off_data_file, self.seperator)
		indexes = ('LCD', 'NEG_OFF_LCD', 'POS_OFF_LCD')
		point_off_data_filtered = point_off_data.get_data(indexes)
		print 'Done!'

		print 'Parsing data ...',
		for off_data in point_off_data_filtered:
			point_a = self.point_dict.get_point(off_data[0])
			# fill road_lcd if not present
			if point_a.seg_lcd != '':
				point_a.road_lcd = self.seg_dict.get_road_lcd(point_a.seg_lcd)
			if len(off_data[1]) > 0:
				point_b = self.point_dict.get_point(off_data[1])
				link_obj = Link(point_a,point_b, 0)
				# fill point b road_lcd if not present
				if point_b.seg_lcd != '':
					point_b.road_lcd = self.seg_dict.get_road_lcd(point_b.seg_lcd)
				self.road_network.add_link(link_obj);
			if len(off_data[2]) > 0:
				point_b = self.point_dict.get_point(off_data[2])
				link_obj = Link(point_a,point_b, 1)
				# fill point b road_lcd if not present
				if point_b.seg_lcd != '':
					point_b.road_lcd = self.seg_dict.get_road_lcd(point_b.seg_lcd)
				self.road_network.add_link(link_obj);
		print 'Done!'


def main():

	# Here, your unit test code or main program
	road_dict = RoadNetworkDict()
	print road_dict.road_network.get_size(),'roads loaded'
	
	file_handle = open("LinkList.txt", "wb")
	
	count = 0

	for road in road_dict.road_network.roads:
		for seg in road.segs:
			for link in seg.links:
				outputstr = ('%s;%s;%s;%s;%s;%s;%d;%f;%f;%f;%f;%s;%s\n' %  
									(road.LCD, road.name,
									link.point_a.LCD, link.point_a.link_name, link.point_b.LCD, link.point_b.link_name, link.direction, 
									link.point_a.longitude, link.point_a.latitude,  
									link.point_b.longitude, link.point_b.latitude,
									link.point_a.seg_lcd, link.point_b.seg_lcd) )
				#print outputstr
				file_handle.write(outputstr)
				count += 1
		for link in road.links:
			outputstr = ('%s;%s;%s;%s;%s;%s;%d;%f;%f;%f;%f;%s;%s\n' %  
							(road.LCD, road.name,
							link.point_a.LCD, link.point_a.link_name, link.point_b.LCD, link.point_b.link_name, link.direction, 
							link.point_a.longitude, link.point_a.latitude,  
							link.point_b.longitude, link.point_b.latitude,
							link.point_a.seg_lcd, link.point_b.seg_lcd) )
			#print outputstr
			file_handle.write(outputstr)
			count += 1
	
						
	file_handle.close()
	
	print 'List is writen into LinkList.txt!'
	print count, 'links are written!\nFeel free to check out\n'
	
if __name__=='__main__':
	main()