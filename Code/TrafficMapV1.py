#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is one of traffic map utility component files
# Created in 2013
# ######################################################################
from Tkinter import *
from BaseMap import *
from TrafficData import *
import tkFileDialog


MAP_SIZE = (1024, 768)
MARGIN_SIZE = 10
CONTROL_AREA_WIDTH = 200
	
SURFACE_SIZE = (MAP_SIZE[0] + 2 * MARGIN_SIZE + CONTROL_AREA_WIDTH, MAP_SIZE[1] + 2 * MARGIN_SIZE)




# Below is the area for class definition

class App:
	def __init__(self, master):
		self.latitude = 39.76751
		self.longitude = 116.54774
		self.zoom_level = 12

		self.basemap = BaseMap()
		self.traffic_data = TrafficData()
		self.traffic_data.load_dictionary()

		self.traffic_display = False
		
		self.init_controls(master)
		self.update()

	def init_controls(self, master):
	
		# initiate areas to add controls
		map_area = LabelFrame(master, text = "Traffic Map", padx=5,pady=5)
		map_area.grid(row=0, column=0)
		
		control_area = LabelFrame(master, text = "Map Control", padx=5,pady=5, width = CONTROL_AREA_WIDTH, height = MAP_SIZE[1])
		control_area.grid(row=0, column=1)

		traffic_file_area = LabelFrame(master, text = "Traffic Resources", padx=5,pady=5, width = MAP_SIZE[0])
		traffic_file_area.grid(row=1)

		# add controls of map canvas area
		self.map_canvas = Canvas(map_area, width = MAP_SIZE[0], height = MAP_SIZE[1])
		self.map_canvas.bind("<Button-1>", self.set_move_from)
		self.map_canvas.bind("<B1-Motion>", self.set_moved_on)
		self.map_canvas.bind("<ButtonRelease-1>", self.move_map)
		
		# add controls in control area
		self.coords_x_label = Label(control_area, text = "Longitude:")
		self.coords_x_input = Entry(control_area)
		self.coords_x_input.insert(0,str(self.longitude))
		
		self.coords_y_label = Label(control_area, text = "Latitude:")
		self.coords_y_input = Entry(control_area)
		self.coords_y_input.insert(0,str(self.latitude))

		self.zoom_level_label = Label(control_area, text = "Zoom Level:")
		
		self.zoom_level_slider = Scale(control_area, from_ = 2, to = 20, orient = HORIZONTAL, sliderlength=10, width = 20, resolution = 1)
		self.zoom_level_slider.set(self.zoom_level)
		
		self.update_button = Button(control_area, text = "Update", command = self.update)

		# add controls in traffic file status area
		self.traffic_file_label = Label(traffic_file_area, text = "Load traffic file:")
		self.traffic_file_input = Entry(traffic_file_area, width = 100)
		self.traffic_file_button = Button(traffic_file_area,text = "load", width = 10, command = self.load_file)
		self.traffic_display_button = Button(traffic_file_area,text = "show", width = 10, command = self.change_traffic_display)

	def update(self):
		self.longitude = float(self.coords_x_input.get())
		self.latitude = float(self.coords_y_input.get())
		self.zoom_level = int(self.zoom_level_slider.get())
		self.basemap.config([self.longitude, self.latitude] , self.zoom_level, 3, 4)
		self.draw()
	
	def set_move_from(self,event):
		self.moved = False
		self.moving_from = [event.x,event.y]
	
	def draw(self):
		self.map_canvas.pack()
		self.coords_x_label.pack(side = TOP)
		self.coords_x_input.pack(side = TOP)
		self.coords_y_label.pack(side = TOP)
		self.coords_y_input.pack(side = TOP)
		self.zoom_level_label.pack(side = TOP)
		self.zoom_level_slider.pack(side = TOP)
		self.update_button.pack(side = TOP)
		self.traffic_file_label.pack(side = LEFT, padx=5)
		self.traffic_file_input.pack(side = LEFT, padx=5)
		self.traffic_file_button.pack(side = LEFT, padx=5)
		self.traffic_display_button.pack(side = LEFT, padx=5)

		self.basemap.draw(self.map_canvas)
		
		if self.traffic_display:
			self.draw_traffic()

	def reverse_update(self):
		self.coords_x_input.delete(0,END)
		self.coords_x_input.insert(0,str(self.longitude))
		self.coords_y_input.delete(0,END)
		self.coords_y_input.insert(0,str(self.latitude))
		self.zoom_level_slider.set(self.zoom_level)

		
	def move_map(self,event):
		movement = [event.x - self.moving_from[0], event.y - self.moving_from[1]]
		self.longitude,self.latitude = self.basemap.move_center( movement)
		self.reverse_update()
		self.draw()
	
	def set_moved_on(self,event):
		self.moved = True

	def load_file(self):
		filename = tkFileDialog.askopenfilename()
		if filename: 
			self.traffic_file_input.delete(0,END)
			self.traffic_file_input.insert(0,filename)
			self.traffic_data.load_traffic('data.csv')
		else:
			return
		
		
	def draw_traffic(self):
		
		box = self.basemap.get_coords_box()
		data = self.traffic_data.get_data_to_draw(box)

		num_lines = len(data)
		for i in range(0,num_lines):
			line_color = 'black'
			code = data[i][6]
			if code == 2049:
				color = 'green'
			elif code == 2050:
				color = 'yellow'
			elif code == 2051:
				color = 'red'
			
			direction = data[i][4]
			
			pos_a = self.get_canvas_pos((data[i][0],data[i][1]))
			pos_b = self.get_canvas_pos((data[i][2],data[i][3]))

			if direction == 0:
				direction_mult = -1
			else:
				direction_mult = 1
			
			step = self.zoom_level - 10
			if step <= 0:
				step = 1

			if (pos_a[0] - pos_b[0]) ** 2 > (pos_a[1] - pos_b[1]) ** 2:
				pos_a[1] = pos_a[1] + step * direction_mult
				pos_b[1] = pos_b[1] + step * direction_mult
			else:
				pos_a[0] = pos_a[0] + step * direction_mult
				pos_b[0] = pos_b[0] + step * direction_mult

			self.map_canvas.create_line(pos_a[0],pos_a[1],pos_b[0],pos_b[1],fill=color,width = step)
	
	def get_canvas_pos(self, coords):
		pos = geocoordinates_to_pixels(coords, self.zoom_level)	# image_size=256
		center_pos = geocoordinates_to_pixels((self.longitude,self.latitude), self.zoom_level)	# image_size=256
		return [1024/2 + pos[0]-center_pos[0], 768/2 + pos[1]-center_pos[1]]
	
	def change_traffic_display(self):
		if self.traffic_display:
			self.traffic_display = False
			self.traffic_display_button.config(text='Show')
		else:
			self.traffic_display = True
			self.traffic_display_button.config(text='Hide')
		self.update()
		
# Below is for helper functions
	

	
# sample url
# http://1.maps.nlp.nokia.com.cn/maptile/2.1/maptile/newest/normal.day.grey/13/6748/3108/256/png8?app_id=demo_qCG24t50dHOwrLQ&token=NYKC67ShPhQwqaydGIW4yg&lg=chi

# unit test code

def main():

	# Here, your unit test code or main program

	# init Tkinter
	root_widget = Tk()
	
	root_widget.title('Traffic Map V1.0')

	# initiate basemap to canvas and keep it live
	app_control_instance = App(root_widget)

	# draw(root_widget, basemap_instance)
	
	root_widget.mainloop()

			
if __name__=='__main__':
	main()