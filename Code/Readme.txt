Name: Traffic Map
Version: 1.0
Purpose: load history traffic data into a map view for inspection

Environment: 
Python 2.7 
PIL 1.1.7 for Python 2.7

Description:
Program is easy to use, you can do the following:
	drag the map to another place
	set new coordinates and press update to move map
	set zoom level and press update to zoom the map
	you can press load button to load history traffic data
	you can press show/hide button to show/hide traffic display

Attention:
	this program doesn't handle cache well yet, so, it may generate big network traffic
	this program doesn't handle cities well yet.
	get it work with city other than beijing, you need to:
		replace point.dat and poffset.dat file manually
		then, restart the program
	this program has not smooth the line along the road yet.