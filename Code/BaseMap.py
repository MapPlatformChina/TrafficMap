#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is one of traffic map utility component files
# Created in 2013
# ######################################################################
from pos_vs_coords import *
from Tkinter import *
from PIL import Image, ImageTk
from StringIO import StringIO
import urllib2


# Below is the area for class definition
class BaseMap:
	def __init__(self):
		self.rows = 3
		self.cols = 4
		self.image_size = 256
		self.photo_array = []
		self.default_image = None
		self.zoom_level = 7
		self.center_coords = [116,39]
		self.tile_shift = [0,0]
		self.reset_tiles()
		self.cached_tiles = []

	def draw(self, canvas):
		self.set_tile_position()
		for i in range(0,self.rows + 1):
			for j in range(0,self.cols + 1):
				index = i * (self.cols + 1) + j
				x = self.image_size/2 + 256 * j - self.tile_shift[0]
				y = self.image_size/2 + 256 * i - self.tile_shift[1]
				if self.photo_array[index] != None:
					canvas.create_image(x,y,image = self.photo_array[index])
				else:
					canvas.create_image(x,y,image = self.default_image)
		canvas.create_rectangle(0,0,1024,768)

	def move_center(self, movement):
		pos = geocoordinates_to_pixels(self.center_coords, self.zoom_level, self.image_size)
		new_pos = [pos[0] - movement[0], pos[1] - movement[1]]
		print pos, new_pos, self.center_coords,
		self.center_coords = pixels_to_geocoordinates(new_pos, self.zoom_level, self.image_size)
		print self.center_coords
		self.update_tiles(movement)
		return self.center_coords
	
	def set_tile_position(self):
		# calculate shifting of the whole picture
		pos = geocoordinates_to_pixels(self.center_coords, self.zoom_level, self.image_size)
		left_top_pos = [ pos[0] - self.cols/2.0 * self.image_size , pos[1] - self.rows/2.0 * self.image_size]
		self.tile_shift = [left_top_pos[0] % self.image_size, left_top_pos[1] % self.image_size]
	
	def update_tiles(self,movement):
		grids = get_conner_grid(self.center_coords, self.zoom_level, self.image_size)
		left_top_grid = grids[0]

		temp_photo_array = []
		temp_cached_tiles = []
		for i in range(0, self.rows + 1):
			for j in range(0, self.cols + 1):
				x = left_top_grid[0] + j
				y = left_top_grid[1] + i
				
				# fetch new tile only in case not cached
				tk_photo = self.get_from_cache(x,y)
				if tk_photo == None:
					tk_photo = self.get_image_from_server((x,y))
				
				temp_photo_array.append(tk_photo)
				temp_cached_tiles.append((x,y))
		
		self.photo_array = temp_photo_array
		self.cached_tiles = temp_cached_tiles
	
	def get_from_cache(self,x,y):
		for i in range(0,len(self.cached_tiles)):
			if self.cached_tiles[i][0] ==  x and self.cached_tiles[i][1] == y:
				return self.photo_array[i]
		return None
	
	def reset_tiles(self):
		grids = get_conner_grid(self.center_coords, self.zoom_level, self.image_size)
		left_top_grid = grids[0]
		self.photo_array = []
		self.cached_tiles = []
		print 'Start to fetching map tiles ...',
		for i in range(0,self.rows + 1):		# cache one more photo to display
			for j in range(0,self.cols + 1):	# cache one more photo to display
				index = i * (self.cols + 1) + j
				x = left_top_grid[0] + j
				y = left_top_grid[1] + i
				self.photo_array.append(self.get_image_from_server((x,y)))
				self.cached_tiles.append((x,y))
		print 'Done!'		
					
			
	def get_center_coords(self):
		return self.center_coords
		
	def get_image_from_server(self, grid):
		# format request string
		request_part1 = 'http://maps.nlp.nokia.com.cn/maptile/2.1/maptile/newest/normal.day.grey'
		request_part2 = '/%d/%d/%d/256/png8' % (self.zoom_level, grid[0], grid[1])
		request_part3 = '?app_id=demo_qCG24t50dHOwrLQ&token=NYKC67ShPhQwqaydGIW4yg&lg=chi'
		request_string = request_part1 + request_part2 + request_part3
		print request_string
		
		# generate request for the image
		req = urllib2.Request(request_string)
		response = urllib2.urlopen(req)
		image_data = response.read()
		
		# generate photo instance from the data and convert into image that Tkinter can use
		pil_image = Image.open(StringIO(image_data))
		tk_photo = ImageTk.PhotoImage(pil_image)
		return tk_photo
	
	def config(self, center_coords, zoom_level, rows=3, cols=4):
		self.center_coords = center_coords
		self.zoom_level = zoom_level
		self.rows = rows
		self.cols = cols
		self.reset_tiles()
	
	def get_coords_box(self):
		pos = geocoordinates_to_pixels(self.center_coords, self.zoom_level, self.image_size)
		left_top_pos = [ pos[0] - self.cols/2.0 * self.image_size , pos[1] - self.rows/2.0 * self.image_size]
		right_bottom_pos = [ pos[0] + self.cols/2.0 * self.image_size , pos[1] + self.rows/2.0 * self.image_size]
		left_top_coords = pixels_to_geocoordinates(left_top_pos, self.zoom_level, self.image_size)
		right_bottom_coords = pixels_to_geocoordinates(right_bottom_pos, self.zoom_level, self.image_size)
		return (left_top_coords[0],left_top_coords[1],right_bottom_coords[0],right_bottom_coords[1])
		
		
	
#	def update(self):

#		grids = get_conner_grid(self.center_coords, self.zoom_level, self.image_size)
#		left_top_grid = grids[0]
#		self.photo_array = []
#		print 'Start to fetching map tiles ...',
#		for i in range(0,self.rows + 1):		# cache one more photo to display
#			for j in range(0,self.cols + 1):	# cache one more photo to display
#				index = i * (self.cols + 1) + j
#				x = left_top_grid[0] + j
#				y = left_top_grid[1] + i
#				self.photo_array.append(self.get_image_from_server((x,y)))
#		print 'Done!'
		
		# calculate shifting of the whole picture
#		pos = geocoordinates_to_pixels(self.center_coords, self.zoom_level, self.image_size)
#		left_top_pos = [ pos[0] - self.cols/2.0 * self.image_size , pos[1] - self.rows/2.0 * self.image_size]
		
#		self.tile_shift = [left_top_pos[0] % self.image_size, left_top_pos[1] % self.image_size]
		
		
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
	
	basemap_instance = BaseMap()
	basemap_instance.draw(map_canvas)
	
	root_widget.mainloop()

			
if __name__=='__main__':
	main()