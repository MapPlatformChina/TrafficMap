#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is to help structuring a good program
# Created in 2013
# ######################################################################

# Below is the area for class definition
from CSVData import *
import math

direction_sign_dict = {'E': 1, 'W': 3, 'N': 2, 'S': 4}
# geo should be in [latitude, longitude] format
def get_direction_sign_with_geo(geo_a, geo_b):
	diff = [geo_b[0] - geo_a[0], geo_b[1] - geo_b[1]]
	direction_sign = '?'
	if abs(diff[1]) >= abs(diff[0]):
		if diff[1] >= 0:
			direction_sign = 'E'	#EAST
		else:
			direction_sign = 'W'	#WEST
	else:
		if diff[0] >= 0:
			direction_sign = 'N'	#NORTH
		else:
			direction_sign = 'S'	#SOUTH
	return direction_sign

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
	def __init__(self, LCD, name = None, TCD = None, STCD = None):
		self.segs = []
		self.links = []
		self.name = name
		self.LCD = LCD
		self.TCD = TCD
		self.STCD = STCD
	
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
	def __init__(self, LCD, urban = True):
		self.links = []
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
	
	def get_direction_sign(self):
		return get_direction_sign_with_geo((self.point_a.latitude, self.point_a.longitude),
									(self.point_b.latitude, self.point_b.longitude))

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

class TypeDict:
	def __init__(self):
		self.types = [];
	
	def add_type(self,type_CD,subtype_CD,type_name):
		self.types.append((type_CD, subtype_CD, type_name))
	
	def get_type_name(self, type_CD, subtype_CD):
		for type in self.types:
			if type[0] == type_CD and type[1] == subtype_CD:
				return type[2]
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
		self.type_data_file = '../Res/SUBTYPES.DAT'
		
		# initiate var used for CSVData
		self.seperator = ';'

		# initiate type dict and load it
		self.type_dict = TypeDict()
		self.load_type_dict()

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
		
	def load_type_dict(self):
		print 'Load',self.type_data_file,'...',
		type_data = CSVData(self.type_data_file, self.seperator);
		indexes = ('TCD','STCD','SDESC')
		type_data_filtered = type_data.get_data(indexes)
		for type in type_data_filtered:
			self.type_dict.add_type(type[0],type[1],type[2])
		print 'Done!'

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

	# before calling this function, seg_dict should be loaded
	def load_point_dict(self):
		print 'Load',self.point_data_file,'...',
		point_data = CSVData(self.point_data_file, self.seperator)
		indexes = ('LCD', 'XCOORD', 'YCOORD','SEG_LCD', 'ROA_LCD', 'RNID')
		point_data_filtered = point_data.get_data(indexes)
		for point_data_item in point_data_filtered:
			seg_lcd = point_data_item[3]
			roa_lcd = point_data_item[4]
			if seg_lcd == '':
				seg_lcd = None
			else:
				roa_lcd = self.seg_dict.get_road_lcd(seg_lcd)
			if roa_lcd == '':
				roa_lcd = None
			point_obj = Point(point_data_item[0], 
					float(point_data_item[1])/100000,float(point_data_item[2])/100000,
					seg_lcd, roa_lcd, self.name_dict.get_name(point_data_item[5]))
			self.point_dict.add_point(point_obj)
		print 'Done!'
		
	def load_road_data(self):
		print 'Load',self.road_data_file,'...',
		road_data = CSVData(self.road_data_file, self.seperator)
		indexes = ('LCD', 'RNID', 'TCD', 'STCD')
		road_data_filtered = road_data.get_data(indexes)
		for road in road_data_filtered:
			road_id = road[0]
			road_name = self.name_dict.get_name(road[1])
			road_obj = Road(road_id,road_name,road[2],road[3])
			self.road_network.add_road(road_obj)
		print 'Done!'
		
	def load_link_data(self):
		print 'Load',self.point_off_data_file,'...',
		point_off_data = CSVData(self.point_off_data_file, self.seperator)
		indexes = ('LCD', 'NEG_OFF_LCD', 'POS_OFF_LCD')
		point_off_data_filtered = point_off_data.get_data(indexes)
		print 'Done!'

		count = 0
		print 'Parsing data ...',
		for off_data in point_off_data_filtered:
			point_a = self.point_dict.get_point(off_data[0])
			# fill road_lcd if not present
			if len(off_data[1]) > 0:
				point_b = self.point_dict.get_point(off_data[1])
				link_obj = Link(point_a,point_b, 0)
				self.road_network.add_link(link_obj);
				count += 1
			if len(off_data[2]) > 0:
				point_b = self.point_dict.get_point(off_data[2])
				link_obj = Link(point_a,point_b, 1)
				self.road_network.add_link(link_obj);
				count += 1
		print 'Done!'
		print count, 'links loaded!'

def parse_direction(link, TCD, STCD):
	msg = ''
	if TCD == '2':		# ring road
		if link.direction == 1:
			msg = 'CLOCK'
		else:
			msg = 'C-CLOCK'
	else:
		msg = 'LINE'

	diff_longitude = link.point_b.longitude-link.point_a.longitude
	diff_latitude = link.point_b.latitude -link.point_a.latitude
	if abs(diff_longitude) >= abs(diff_latitude):
		if diff_longitude >= 0:
			msg = ('%s;%d;%s' % (msg, 1,'EAST'))
		else:
			msg = ('%s;%d;%s' % (msg, 3,'WEST'))
	else:
		if diff_latitude >= 0:
			msg = ('%s;%d;%s' % (msg, 2,'NORTH'))
		else:
			msg = ('%s;%d;%s' % (msg, 4,'SOUTH'))
	return msg
	
def get_shift(link, shift_dis):

	diff_longitude = link.point_b.longitude-link.point_a.longitude
	diff_latitude = link.point_b.latitude -link.point_a.latitude
	if abs(diff_longitude) >= abs(diff_latitude):
		if diff_longitude >= 0:
			return (0, -shift_dis)	#EAST
		else:
			return (0, shift_dis)	#WEST
	else:
		if diff_latitude >= 0:
			return (shift_dis,0)	#NORTH
		else:
			return (-shift_dis,0)	#SOUTH
	return (0,0)


def sample_helper_break_link_into_dict(link):
	GRANULARITY = 0.00001
	link_name = ('%s_%d' % (link.point_b.LCD, link.direction))
	dict_array = []
	zero_point = [link.point_a.latitude,link.point_a.longitude]
	diff = [link.point_b.latitude - link.point_a.latitude, 
				link.point_b.longitude - link.point_a.longitude]

	num_segment = int(math.ceil(max(abs(diff[0]),abs(diff[1])) / 0.0001))
	seg_diff = [diff[0] / float(num_segment), diff[1] / float(num_segment)]
	for i in range(0,num_segment):
		pa = [zero_point[0] + seg_diff[0] * i,zero_point[1] + seg_diff[1] * i] 
		pb = [zero_point[0] + seg_diff[0] * (i+1),zero_point[1] + seg_diff[1] * (i+1)] 
		pc = [(pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2]
		dict_array.append((pc[0],pc[1],link_name))
	return dict_array
			
def sample_helper_write_link(link, handle_of_file):
	count = 0
	dict_array = sample_helper_break_link_into_dict(link)
	direction_sign = link.get_direction_sign()
	for item in dict_array:
		outputstr = ('%s;%f;%f;%s\n' % (direction_sign,item[0],item[1],item[2]))
		handle_of_file.write(outputstr)
		count += 1
	return count

def sample_func_generate_link_dictionanry():

	# Here, your unit test code or main program
	road_dict = RoadNetworkDict()
	print road_dict.road_network.get_size(),'roads loaded'
	
	output_filename = 'LinkMatch.dict'
	file_handle = open(output_filename, "wb")
	
	count = 0

	for road in road_dict.road_network.roads:

		for seg in road.segs:
			for link in seg.links:
				count += sample_helper_write_link(link, file_handle)
			for link in road.links:
				count += sample_helper_write_link(link, file_handle)
						
	file_handle.close()
	
	print 'Link dictionary is writen into ', output_filename
	print count, 'links are written!\nFeel free to check out\n'

def sample_generate_link_list():
	road_dict = RoadNetworkDict()
	print road_dict.road_network.get_size(),'roads loaded'
	
	is_shifted = True
	
	if is_shifted:
		output_filename = "LinkListShifted.txt"
		shift_dis = 0.00002
	else:
		output_filename = "LinkList.txt"
		shift_dis = 0
	
	file_handle = open(output_filename, "wb")
	
	count = 0

	for road in road_dict.road_network.roads:
		if road.TCD == '7' and road.STCD =='0':		#匝道
			shift_factor = shift_dis * 1
		elif road.TCD == '1' and road.STCD =='1':	#高速
			shift_factor = shift_dis * 4
		elif road.TCD == '1' and road.STCD =='2':	#一级公路
			shift_factor = shift_dis * 2.5
		elif road.TCD == '1' and road.STCD =='3':	#二级公路
			shift_factor = shift_dis * 6 # 1.5
		elif road.TCD == '1' and road.STCD =='4':	#三级公路
			shift_factor = shift_dis * 6 # 1
		elif road.TCD == '2' and road.STCD =='1':	#高速环路
			shift_factor = shift_dis * 2.5
		elif road.TCD == '2' and road.STCD =='2':	#其它环路
			shift_factor = shift_dis * 1.5
		elif road.TCD == '3' and road.STCD =='0':	#一级路段
			shift_factor = shift_dis * 1
		else:
			shift_factor = shift_dis

		for seg in road.segs:
			for link in seg.links:
				direction_msg = parse_direction(link,road.TCD, road.STCD)
				shift = get_shift(link, shift_factor)
				outputstr = ('%s;%s;%s;%s;%d;%s;%f;%f;%f;%f;%s;%s\n' %  
									(road.LCD, link.point_a.link_name,
									link.point_a.LCD, link.point_b.LCD, link.direction, direction_msg,
									link.point_a.latitude+shift[1], link.point_a.longitude+shift[0],
									link.point_b.latitude+shift[1], link.point_b.longitude+shift[0],
									link.point_a.seg_lcd, link.point_b.seg_lcd) )

				outputstr = ('%s;%s;%s;%s;%d;%s;%f;%f;%f;%f;%s;%s\n' %  
									(road.LCD, link.point_a.link_name,
									link.point_a.LCD, link.point_b.LCD, link.direction, direction_msg,
									link.point_a.latitude+shift[1], link.point_a.longitude+shift[0],
									link.point_b.latitude+shift[1], link.point_b.longitude+shift[0],
									link.point_a.seg_lcd, link.point_b.seg_lcd) )
				#print outputstr
				file_handle.write(outputstr)
				count += 1
		for link in road.links:
			direction_msg = parse_direction(link,road.TCD, road.STCD)
			shift = get_shift(link, shift_factor)
			outputstr = ('%s;%s;%s;%s;%d;%s;%f;%f;%f;%f;%s;%s\n' %  
							(road.LCD, link.point_a.link_name,
							link.point_a.LCD, link.point_b.LCD, link.direction, direction_msg,
							link.point_a.latitude+shift[1], link.point_a.longitude+shift[0],
							link.point_b.latitude+shift[1], link.point_b.longitude+shift[0],
							link.point_a.seg_lcd, link.point_b.seg_lcd) )
			#print outputstr
			file_handle.write(outputstr)
			count += 1
	
						
	file_handle.close()
	
	print 'List is writen into ', output_filename
	print count, 'links are written!\nFeel free to check out\n'
	
def main():

	# Here, your unit test code or main program
	sample_func_generate_link_dictionanry()
	#sample_generate_link_list()
	
if __name__=='__main__':
	main()