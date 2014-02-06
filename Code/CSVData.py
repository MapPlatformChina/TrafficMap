#!/usr/bin/python
# -*- coding: utf-8 -*-

# ######################################################################
# This file is to help structuring a good program
# Created in 2013
# ######################################################################

# Below is the area for class definition

class CSVData:
	def __init__(self, fn=None, seperator = ','):
		self.index_list = []
		self.data = []
		if fn is not None:
			self.load(fn, seperator)

	def load(self, fn, seperator):
		self.index_list = []
		self.data = []
		file_csv = open(fn,'r')
		line = file_csv.readline()
		indexes = line.split(seperator)
		
		# Remove BOM from the beginning of utf-8 file
		if indexes[0][0:3] == '\xef\xbb\xbf':	
			indexes[0] = indexes[0][3:]
			
		for i in range(len(indexes)):
			indexes[i] = indexes[i].strip(' ')
			indexes[i] = indexes[i].strip('\n')
		self.index_list = indexes
		while True:
			data = file_csv.readline()
			if not data:
				break;
			split_array = data.split(seperator)
			for i in range(len(split_array)):
				split_array[i] = split_array[i].strip()
			self.data.append(split_array)
		file_csv.close()
	
	def get_index(self):
		return self.index_list
	
	def get_data(self, index_list):
		result = []
		for data_index in range(len(self.data)):
			data_item = []
			for index_name in index_list:
				index = self.index_list.index(index_name)	
				data_item.append(self.data[data_index][index])
			result.append(data_item)
		return result
			
# Below is for helper functions

def main():

	# Here, your unit test code or main program
	
	# you can change below paras to define another unit test case
	fn = 'NAMES.DAT'
	seperator = ';'
	index_name = ('NID', 'NAME')
	
	# test class with upper defined paras
	csv = CSVData(fn, seperator)
	indexes = csv.get_index()
	for index in indexes:
		print index.decode('utf-8').encode('gb2312'),
	print
	data = csv.get_data(index_name)
	for i in range(10):
		for x in range(len(index_name)):
			print data[i][x].decode('utf-8').encode('gb2312'),
		print

if __name__=='__main__':
	main()

