#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is one of traffic map utility component files
# Created in 2013
# ######################################################################
from PosCoordsUtl import *
from Tkinter import *
from PIL import Image, ImageTk
from StringIO import StringIO
import urllib2


# Below is the area for class definition
class BaseMap:
	def __init__(self, canvas_size, image_size = 256, center = [116,39]):
		self.canvas_size = canvas_size
		self.image_size = image_size
		
		self.rows = int(math.ceil(self.canvas_size[1] / float(self.image_size)))
		self.cols = int(math.ceil(self.canvas_size[0] / float(self.image_size)))
		
		self.zoom_level = 10
		self.pos_coords_utl = PosCoordsUtl(self.zoom_level, self.canvas_size, self.image_size)
		
		self.center_coords = center

		# below are attributes of display
		self.default_tile = None
		self.cached_tiles = []

		self.tile_shift = [0,0]
		
		self.cache_tile()
	
	def set_center(self, center_coords):
		self.center_coords = center_coords
		#self.cache_tile()
		
	def set_zoom_level(self, zoom_level):
		self.zoom_level = zoom_level
		self.pos_coords_utl.set_zoom_level(self.zoom_level)
		#self.cache_tile()

	def cache_tile(self):
		# check out left top and right bottom grid first
		grids = self.pos_coords_utl.get_conner_grid(self.center_coords)
		
		left_top_grid = grids[0]

		temp_photo_array = []
		temp_cached_tiles = []
		for i in range(0, self.rows + 1):	#cache one more tile to make sure the map is fully covered
			for j in range(0, self.cols + 1):	#cache one more tile to make sure the map is fully covered
				x = left_top_grid[0] + j
				y = left_top_grid[1] + i
				
				# fetch new tile only in case not cached
				if not self.is_tile_in_cache(x,y):
					tk_photo = self.get_image_from_server((x,y))
					self.cached_tiles.append((x,y,self.zoom_level,tk_photo))
				
	def is_tile_in_cache(self, x, y):
		for tile_item in self.cached_tiles:
			if tile_item[0] == x and tile_item[1] == y and tile_item[2] == self.zoom_level:
				return True
		return False

	def get_tile(self, x, y):
		for tile_item in self.cached_tiles:
			if tile_item[0] == x and tile_item[1] == y and tile_item[2] == self.zoom_level:
				return tile_item[3]
		return None
		
	def optimize_cache(self):
		pass	#to be added
		
	def draw(self, canvas, mark_point_array = []):
		self.cache_tile()
		canvas.delete(ALL)
		self.tile_shift = self.pos_coords_utl.get_shift(self.center_coords)
		grids = self.pos_coords_utl.get_conner_grid(self.center_coords)
		left_top_grid = grids[0]
		
		for i in range(0,self.rows + 1):
			for j in range(0,self.cols + 1):
				x = left_top_grid[0] + j
				y = left_top_grid[1] + i
				image_obj = self.get_tile(x,y)
				
				pos_x = self.image_size/2 + 256 * j - self.tile_shift[0]
				pos_y = self.image_size/2 + 256 * i - self.tile_shift[1]
				
				if image_obj != None:
					canvas.create_image(pos_x,pos_y, image=image_obj)
				else:
					print x,y, 'is not loaded!'
		
		for mark_point in mark_point_array:
			if not ('last_mark_point' in locals()):
				last_mark_point = mark_point
				last_pos = self.get_pos(last_mark_point)
				continue
			print last_mark_point,mark_point
			pos = self.get_pos(mark_point)
			
			canvas.create_line(last_pos[0], last_pos[1],
								pos[0], pos[1],
								fill = 'blue', width = 3)
			last_mark_point = mark_point
			last_pos = pos
			
	def get_center_coords(self):
		return self.center_coords
		
	def get_image_from_server(self, grid):
		# format request string
		request_part1 = 'http://maps.nlp.nokia.com.cn/maptile/2.1/maptile/newest/normal.day.grey'
		request_part2 = '/%d/%d/%d/256/png8' % (self.zoom_level, grid[0], grid[1])
		request_part3 = '?app_id=demo_qCG24t50dHOwrLQ&token=NYKC67ShPhQwqaydGIW4yg&lg=chi'
		request_string = request_part1 + request_part2 + request_part3
		#print request_string
		
		# generate request for the image
		req = urllib2.Request(request_string)
		response = urllib2.urlopen(req)
		image_data = response.read()
		
		# generate photo instance from the data and convert into image that Tkinter can use
		pil_image = Image.open(StringIO(image_data))
		tk_photo = ImageTk.PhotoImage(pil_image)
		return tk_photo

	def move_center(self, movement):
		pos = self.pos_coords_utl.coords_to_pos(self.center_coords)
		new_pos = [pos[0] - movement[0], pos[1] - movement[1]]
		print pos, new_pos, self.center_coords,
		self.center_coords = self.pos_coords_utl.pos_to_coords(new_pos)
		print self.center_coords
		self.cache_tile()
		return self.center_coords

	def get_pos(self, coords):
		pos = self.pos_coords_utl.coords_to_pos(coords)
		center_pos = self.pos_coords_utl.coords_to_pos(self.center_coords)
		diff = [center_pos[0]-pos[0],center_pos[1]-pos[1]]
		return [self.canvas_size[0]/2 - diff[0], self.canvas_size[1]/2 - diff[1]]

		
# Below is for helper functions

# sample url
# http://1.maps.nlp.nokia.com.cn/maptile/2.1/maptile/newest/normal.day.grey/13/6748/3108/256/png8?app_id=demo_qCG24t50dHOwrLQ&token=NYKC67ShPhQwqaydGIW4yg&lg=chi

# unit test code

def main():

	# Here, your unit test code or main program

	# init Tkinter
	root_widget = Tk()
	
	map_area = LabelFrame(root_widget, text = "Traffic Map", padx=5,pady=5)
	map_area.pack(side = LEFT)

	map_canvas = Canvas(map_area, width = 1024, height = 768)
	map_canvas.pack()
	
	basemap_instance = BaseMap((1024,768))
	basemap_instance.draw(map_canvas)
	
	root_widget.mainloop()

			
if __name__=='__main__':
	main()